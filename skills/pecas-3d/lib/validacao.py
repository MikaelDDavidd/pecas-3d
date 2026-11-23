"""Todas as checagens de uma peça em árvore, num lugar só. Usado pelo peca.py (no fim) e
pelo `p3d validar` (depois de editar na tela).

Checa: objetos sem erro de recálculo, esboços com 0 grau de liberdade, cada peça um sólido
válido, check(False) do OCC, teste de mudar medidas da planilha e recalcular, STL fechado
e sem non-manifold nem auto-interseção. Imprime uma linha por item e termina com
VALIDACAO_OK ou VALIDACAO_FALHOU.

O check(True) do OCC aborta (BOPAlgo OperationAborted) em sólidos com perfil de engrenagem
evolvente e às vezes em B-spline de texto; nesse caso vale o check(False) + o STL limpo.
"""

import os

import FreeCAD as App
import Part

import arvore as av
import pecas3d as p3


class Relatorio:
    def __init__(self):
        self.falhas = []

    def item(self, nome, ok, info=""):
        print(f"[{'ok' if ok else 'FALHOU'}] {nome}{(' - ' + info) if info else ''}")
        if not ok:
            self.falhas.append(nome)
        return ok


def pecas_do_documento(doc):
    """Peças para imprimir = objetos com a propriedade `Cor` (posta por arvore.cor)."""
    return [o for o in doc.Objects if "Cor" in o.PropertiesList and hasattr(o, "Shape")]


def _erros(doc):
    return [f"{o.Label}: {o.getStatusString()}" for o in doc.Objects if "Invalid" in o.State or "Error" in o.State]


def entradas_da_planilha(doc, maximo=5):
    """Medidas da seção de entradas da planilha `Medidas` com unidade de comprimento ou ângulo."""
    m = doc.getObject("Medidas")
    if m is None:
        return []
    saida, linha, na_entrada = [], 2, False
    while linha < 500:
        chave = m.getContents(f"A{linha}").lstrip("'")
        if not chave:
            if not m.getContents(f"A{linha + 1}"):
                break
            linha += 1
            continue
        valor = m.getContents(f"B{linha}")
        if not valor:  # título de seção
            na_entrada = chave.strip().upper().startswith("ENTRADA")
        elif na_entrada:  # getContents devolve "'texto" e "=60 mm"; a seção é que separa
            alias = m.getAlias(f"B{linha}")
            v = m.get(f"B{linha}")
            un = getattr(v, "Unit", None)
            if alias and un is not None and un in (App.Units.Length, App.Units.Angle) and v.Value > 0:
                saida.append((alias, v))
        linha += 1
    return saida[:maximo]


def teste_da_planilha(doc, pecas, rel, mudancas=None):
    """Muda medidas (+5% por padrão), recalcula, confere e volta os valores originais."""
    m = doc.getObject("Medidas")
    if m is None:
        return rel.item("planilha Medidas existe", False)
    if mudancas is None:
        mudancas = []
        for alias, v in entradas_da_planilha(doc):
            un = "mm" if v.Unit == App.Units.Length else "deg"
            mudancas.append((alias, f"{v.Value * 1.05:.6g} {un}"))
    if not mudancas:
        return rel.item("teste de mudar medidas", False, "nenhuma medida de entrada achada na planilha")
    originais = {k: m.getContents(m.getCellFromAlias(k)) for k, _ in mudancas}
    for k, novo in mudancas:
        m.set(m.getCellFromAlias(k), novo)
    doc.recompute()
    erros = _erros(doc)
    ok = not erros and all(p.Shape.isValid() and len(p.Shape.Solids) == 1 for p in pecas)
    resumo = ", ".join(f"{k}={n}" for k, n in mudancas)
    rel.item("mudar medidas e recalcular", ok, resumo + ("" if ok else " -> " + "; ".join(erros)))
    for k, v in originais.items():
        m.set(m.getCellFromAlias(k), v)
    doc.recompute()
    return rel.item("medidas originais de volta", not _erros(doc))


def conferir(doc, pecas=None, mudancas=None, pasta_saida=None, nome=None, linear=0.02, angular=0.1,
             salvar=True, problemas=(), stl_por_peca=True):
    """Roda todas as checagens. Com `pasta_saida`, salva o .FCStd e exporta STEP e STL (um
    arquivo com tudo e, se `stl_por_peca`, um por peça). `problemas` = falhas já achadas
    pelas checagens próprias da peça. Devolve True se passou."""
    rel = Relatorio()
    for p in problemas:
        rel.item(p, False)
    pecas = pecas or pecas_do_documento(doc)
    doc.recompute()
    erros = _erros(doc)
    rel.item("recálculo sem erro", not erros, "; ".join(erros))
    rel.item("peças para imprimir achadas", bool(pecas), ", ".join(p.Label for p in pecas))

    soltos = [o.Label for o in doc.Objects if o.TypeId == "Sketcher::SketchObject" and not av.esboco_restrito(o)]
    n_esbocos = sum(1 for o in doc.Objects if o.TypeId == "Sketcher::SketchObject")
    rel.item(f"{n_esbocos} esboços com 0 grau de liberdade", not soltos, ", ".join(soltos))

    for p in pecas:
        s = p.Shape
        rel.item(f"{p.Label}: sólido válido", s.isValid() and not s.isNull())
        rel.item(f"{p.Label}: 1 sólido", len(s.Solids) == 1, f"{len(s.Solids)} sólidos")
        try:
            s.check(False)
            ok_geo, msg = True, ""
        except Exception as exc:
            ok_geo, msg = False, str(exc).strip()[:200]
        rel.item(f"{p.Label}: geometria (check do OCC)", ok_geo, msg)
        bb = s.BoundBox
        rel.item(f"{p.Label}: apoiada na mesa (Z mínimo 0)", abs(bb.ZMin) < 1e-3, f"Z mínimo {bb.ZMin:.3f}")
        print(f"     {p.Label}: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm, "
              f"{s.Volume / 1000:.1f} cm3")
    for i, a in enumerate(pecas):
        for b in pecas[i + 1:]:
            vol = a.Shape.common(b.Shape).Volume
            rel.item(f"{a.Label} não invade {b.Label}", vol < 1e-6, f"{vol:.4f} mm3")

    teste_da_planilha(doc, pecas, rel, mudancas)

    if pasta_saida:
        nome = nome or doc.Name
        if salvar:
            av.salvar(doc, os.path.join(pasta_saida, f"{nome}.FCStd"))
        out = av.exportar_pecas(pecas, pasta_saida, nome, linear=linear, angular=angular)
        rel.item("STL fechado, sem non-manifold e sem auto-interseção", out["stl_check"]["ok"])
        if stl_por_peca and len(pecas) > 1:
            for p in pecas:
                o = av.exportar_pecas([p], pasta_saida, _kebab(p.Label), linear=linear, angular=angular)
                rel.item(f"STL de {p.Label}", o["stl_check"]["ok"])

    if rel.falhas:
        print("VALIDACAO_FALHOU: " + "; ".join(rel.falhas))
        return False
    print("VALIDACAO_OK")
    return True


def _kebab(texto):
    import re
    import unicodedata
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", t)
    return re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
