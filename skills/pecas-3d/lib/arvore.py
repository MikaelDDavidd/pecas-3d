"""Ajudantes para montar peças como projeto nativo do FreeCAD (árvore editável).

Toda medida mora numa planilha `Medidas`; os esboços são totalmente restritos e as
cotas são expressões ligadas à planilha; a geometria sai de features do PartDesign
(Pad, Pocket, Loft, Revolution, Groove). Abrir o resultado com `p3d abrir`.

Pegadinhas do FreeCAD 1.1 que valem aqui:
- `SideType = "Symmetric"` em vez de `Midplane = True` (obsoleto, gera aviso ao abrir).
- O freecadcmd não grava cor: a cor vai na propriedade `Cor` (hex) de cada peça e o
  lib/aparencia.py pinta ao abrir com janela.
- Alias da planilha não pode ser nome de unidade (`h`, `w`, `r`, `m`, `s`, `g`...):
  dá "Invalid alias". Usar nomes por extenso.
- Plano XZ do corpo: x local = X global, y local = Z global, normal = -Y. Então o
  AttachmentOffset.Base.z de um esboço no XZ vale -Y global.
"""

import os

import FreeCAD as App
import Part
import Sketcher

V = App.Vector
M = "Medidas."


# ---------------------------------------------------------------- parâmetros

def ler_parametros(P, argv):
    """Aplica `nome=valor` da linha de comando sobre o dicionário P (aceita vírgula decimal)."""
    for arg in argv:
        k, _, v = arg.partition("=")
        if k not in P or not v:
            raise SystemExit(f"parâmetro inválido: {arg!r}. Válidos: {', '.join(P)}")
        try:
            P[k] = float(v.replace(",", "."))
        except ValueError:
            raise SystemExit(f"valor inválido para {k}: {v!r} (use número, ex. {k}=4.5)")
    return P


def comentarios(caminho, P):
    """Comentário de cada linha `nome=valor,  # comentário` do dicionário P no script."""
    saida = {}
    for linha in open(caminho, encoding="utf-8"):
        k, sep, c = linha.strip().partition("=")
        if sep and k.strip() in P and "#" in c:
            saida[k.strip()] = c.split("#", 1)[1].strip()
    return saida


# ---------------------------------------------------------------- planilha

def planilha(doc, medidas, nome="Medidas"):
    """Cria a planilha. `medidas` = lista de (nome, valor ou "=fórmula", observação);
    valor None vira título de seção. Cada valor ganha o alias `nome`."""
    m = doc.addObject("Spreadsheet::Sheet", nome)
    m.set("A1", "Medida"); m.set("B1", "Valor"); m.set("C1", "Observação")
    for linha, (chave, valor, obs) in enumerate(medidas, start=2):
        if valor is None:
            m.set(f"A{linha}", chave.upper())
            continue
        m.set(f"A{linha}", chave)
        texto = str(valor)
        if texto.startswith("-"):
            texto = "=" + texto  # sem "=", valor negativo vira texto na planilha
        m.set(f"B{linha}", texto)
        m.setAlias(f"B{linha}", chave)
        if obs:
            m.set(f"C{linha}", obs)
    m.setColumnWidth("A", 140)
    m.setColumnWidth("C", 380)
    doc.recompute()
    return m


def valor(doc, expressao):
    """Valor numérico (mm, graus ou puro) de uma expressão, avaliada na planilha."""
    if isinstance(expressao, (int, float)):
        return float(expressao)
    q = doc.getObject("Medidas").evalExpression(str(expressao))
    return float(q.Value) if hasattr(q, "Value") else float(q)


# ---------------------------------------------------------------- esboços

def plano(corpo, papel):
    """Plano de origem do corpo: "XY", "XZ" ou "YZ"."""
    return next(f for f in corpo.Origin.OriginFeatures if getattr(f, "Role", f.Name).startswith(papel))


def esboco(corpo, nome, suporte, modo="FlatFace", x=None, y=None, z=None):
    """Esboço preso a um plano. x, y, z = expressões do AttachmentOffset (local do plano;
    z é o afastamento ao longo da normal)."""
    sk = corpo.newObject("Sketcher::SketchObject", nome)
    sk.AttachmentSupport = [(suporte, "")]
    sk.MapMode = modo
    for eixo, e in (("x", x), ("y", y), ("z", z)):
        if e is not None:
            sk.setExpression(f".AttachmentOffset.Base.{eixo}", str(e))
    return sk


def _cota(sk, indice, expressao):
    if isinstance(expressao, str):
        sk.setExpression(f"Constraints[{indice}]", expressao)


def _fixar_ponto(sk, doc, geo, pos, ex, ey):
    """Prende o vértice (geo, pos) às coordenadas ex, ey (expressões) a partir da origem."""
    for e, tipo, eixo in ((ex, "DistanceX", -2), (ey, "DistanceY", -1)):
        v = valor(doc, e)
        if isinstance(e, (int, float)) and v == 0:
            sk.addConstraint(Sketcher.Constraint("PointOnObject", geo, pos, eixo))
        else:
            _cota(sk, sk.addConstraint(Sketcher.Constraint(tipo, -1, 1, geo, pos, v)), e)


def poligono(sk, doc, pontos):
    """Polígono fechado totalmente restrito. `pontos` = [(x, y), ...] em coordenadas do
    esboço; cada coordenada é número ou expressão da planilha. Use 0 (número) para
    prender o ponto no eixo."""
    n = len(pontos)
    xy = [V(valor(doc, x), valor(doc, y), 0) for x, y in pontos]
    li = [sk.addGeometry(Part.LineSegment(xy[i], xy[(i + 1) % n])) for i in range(n)]
    for i in range(n):
        sk.addConstraint(Sketcher.Constraint("Coincident", li[i], 2, li[(i + 1) % n], 1))
    for i, (x, y) in enumerate(pontos):
        _fixar_ponto(sk, doc, li[i], 1, x, y)
    return li


def _ponto_central(sk, doc, cx, cy):
    p = sk.addGeometry(Part.Point(V(valor(doc, cx), valor(doc, cy), 0)), True)
    _fixar_ponto(sk, doc, p, 1, cx, cy)
    return p


def retangulo(sk, doc, w, h, cx=0, cy=0, r=None):
    """Retângulo centrado em (cx, cy), arredondado se `r`; totalmente restrito."""
    W, H, X, Y = (valor(doc, e) for e in (w, h, cx, cy))
    if not r:
        pts = [V(X - W / 2, Y - H / 2, 0), V(X + W / 2, Y - H / 2, 0), V(X + W / 2, Y + H / 2, 0), V(X - W / 2, Y + H / 2, 0)]
        li = [sk.addGeometry(Part.LineSegment(pts[i], pts[(i + 1) % 4])) for i in range(4)]
        for i in range(4):
            sk.addConstraint(Sketcher.Constraint("Coincident", li[i], 2, li[(i + 1) % 4], 1))
        sk.addConstraint(Sketcher.Constraint("Horizontal", li[0]))
        sk.addConstraint(Sketcher.Constraint("Horizontal", li[2]))
        sk.addConstraint(Sketcher.Constraint("Vertical", li[1]))
        sk.addConstraint(Sketcher.Constraint("Vertical", li[3]))
        _cota(sk, sk.addConstraint(Sketcher.Constraint("DistanceX", li[0], 1, li[0], 2, W)), w)
        _cota(sk, sk.addConstraint(Sketcher.Constraint("DistanceY", li[1], 1, li[1], 2, H)), h)
        p = _ponto_central(sk, doc, cx, cy)
        sk.addConstraint(Sketcher.Constraint("Symmetric", li[0], 1, li[1], 2, p, 1))
        return
    R = valor(doc, r)
    a, b = W / 2, H / 2
    linhas = [
        (V(X - a + R, Y - b, 0), V(X + a - R, Y - b, 0)),
        (V(X + a, Y - b + R, 0), V(X + a, Y + b - R, 0)),
        (V(X + a - R, Y + b, 0), V(X - a + R, Y + b, 0)),
        (V(X - a, Y + b - R, 0), V(X - a, Y - b + R, 0)),
    ]
    centros = [V(X + a - R, Y - b + R, 0), V(X + a - R, Y + b - R, 0), V(X - a + R, Y + b - R, 0), V(X - a + R, Y - b + R, 0)]
    meio_pi = 1.5707963267948966
    angulos = [(-meio_pi, 0.0), (0.0, meio_pi), (meio_pi, 2 * meio_pi), (2 * meio_pi, 3 * meio_pi)]
    li = [sk.addGeometry(Part.LineSegment(*l)) for l in linhas]
    ar = [sk.addGeometry(Part.ArcOfCircle(Part.Circle(c, V(0, 0, 1), R), *ang)) for c, ang in zip(centros, angulos)]
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint("Tangent", li[i], 2, ar[i], 1))
        sk.addConstraint(Sketcher.Constraint("Tangent", ar[i], 2, li[(i + 1) % 4], 1))
    sk.addConstraint(Sketcher.Constraint("Horizontal", li[0]))
    sk.addConstraint(Sketcher.Constraint("Horizontal", li[2]))
    sk.addConstraint(Sketcher.Constraint("Vertical", li[1]))
    sk.addConstraint(Sketcher.Constraint("Vertical", li[3]))
    for i in (1, 2, 3):
        sk.addConstraint(Sketcher.Constraint("Equal", ar[0], ar[i]))
    _cota(sk, sk.addConstraint(Sketcher.Constraint("Radius", ar[0], R)), r)
    _cota(sk, sk.addConstraint(Sketcher.Constraint("DistanceX", li[3], 1, li[1], 1, W)), w)
    _cota(sk, sk.addConstraint(Sketcher.Constraint("DistanceY", li[0], 1, li[2], 1, H)), h)
    p = _ponto_central(sk, doc, cx, cy)
    sk.addConstraint(Sketcher.Constraint("Symmetric", ar[3], 3, ar[1], 3, p, 1))


def circulo(sk, doc, d, cx, cy):
    """Círculo de diâmetro d com centro em (cx, cy); totalmente restrito."""
    c = sk.addGeometry(Part.Circle(V(valor(doc, cx), valor(doc, cy), 0), V(0, 0, 1), valor(doc, d) / 2))
    _cota(sk, sk.addConstraint(Sketcher.Constraint("Diameter", c, valor(doc, d))), d)
    _fixar_ponto(sk, doc, c, 3, cx, cy)


# ---------------------------------------------------------------- montagem e saída

def recomputar(doc, etapa):
    """Recalcula e falha com o nome do objeto se algo ficou inválido."""
    doc.recompute()
    ruins = [f"{o.Label}: {o.getStatusString()}" for o in doc.Objects if "Invalid" in o.State or "Error" in o.State]
    if ruins:
        raise RuntimeError(f"{etapa} falhou -> " + "; ".join(ruins))
    print(f"ok  {etapa}")


def esboco_restrito(sk):
    """True se o esboço não tem grau de liberdade sobrando."""
    return sk.solve() == 0 and sk.DoF == 0


def cor(obj, hexa):
    """Grava a cor (hex "RRGGBB") numa propriedade do objeto; o lib/aparencia.py pinta."""
    if "Cor" not in obj.PropertiesList:
        obj.addProperty("App::PropertyString", "Cor", "Aparencia", "Cor no FreeCAD (hex)")
    obj.Cor = hexa


def esconder_auxiliares(doc):
    """Esconde esboços, sistemas de eixos e textos; deixa visível o que tem `Cor`."""
    for o in doc.Objects:
        auxiliar = ("Sketch" in o.TypeId or o.TypeId in ("PartDesign::CoordinateSystem", "Part::Part2DObjectPython")
                    or o.TypeId.startswith("Draft"))
        if auxiliar:
            o.Visibility = False
        if "Cor" in o.PropertiesList:
            o.Visibility = True


def salvar(doc, caminho):
    """saveAs sem deixar .FCBak ao lado."""
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    if os.path.exists(caminho):
        os.remove(caminho)
    import pecas3d as p3
    with p3.silencio():
        doc.saveAs(caminho)
    print(f"ok  salvo {caminho}")


def exportar_pecas(objs, pasta, nome, linear=0.02, angular=0.1):
    """STEP e STL (um arquivo com todas as peças) a partir dos objetos da árvore."""
    import Import
    import MeshPart
    import pecas3d as p3
    os.makedirs(pasta, exist_ok=True)
    base = os.path.join(os.path.abspath(pasta), nome)
    forma = Part.Compound([o.Shape for o in objs])
    with p3.silencio():
        Import.export(objs, base + ".step")
        MeshPart.meshFromShape(Shape=forma, LinearDeflection=linear, AngularDeflection=angular,
                               Relative=False).write(base + ".stl")
    print(f"== exportado: {base}.step\n               {base}.stl")
    return dict(step=base + ".step", stl=base + ".stl", forma=forma, stl_check=p3.verificar_stl(base + ".stl"))
