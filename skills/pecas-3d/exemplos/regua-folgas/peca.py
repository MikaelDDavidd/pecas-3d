# Régua de folgas print-in-place, montada como projeto nativo do FreeCAD (árvore
# editável): placa com 6 pinos impressos já montados, cada um com uma folga diferente.
# O pino tem um bulbo de cone duplo (45 graus) preso num alojamento igual, então não
# sai da placa e imprime sem suporte. Girar cada pino (moeda ou chave de fenda na
# fenda do topo): o menor número que gira solto é a folga print-in-place da impressora.
#
# Gerar: p3d gerar regua-folgas/peca.py [param=valor ...]
# Abrir: p3d abrir regua-folgas/saida/regua-folgas.FCStd
# No FreeCAD, toda medida está na planilha "Medidas": mudar lá e recalcular (Ctrl+R).
# A quantidade de pinos é fixa na árvore (6); para mudar, rodar o script de novo.
import os
import sys

import FreeCAD as App
import Part

import arvore as av
import pecas3d as p3
import validacao
from arvore import M

P = dict(
    folga_ini=0.15,      # folga por lado do 1º pino (mm), medida na normal da superfície
    folga_passo=0.05,    # aumento da folga de um pino para o próximo
    pino_d=8.0,          # diâmetro do pino
    bulbo=1.5,           # quanto o bulbo sai do pino (radial); com 45 graus, também é a meia altura
    bulbo_z=2.0,         # altura onde o bulbo começa a abrir
    espessura=8.0,       # espessura da placa
    pino_acima=4.0,      # quanto o pino sai acima da placa
    fenda_larg=2.4,      # fenda do topo do pino (moeda ou chave de fenda)
    fenda_prof=2.4,      # profundidade da fenda
    passo=15.0,          # distância entre centros dos pinos
    margem=9.0,          # do centro do pino da ponta até a borda da placa
    largura=24.0,        # Y da placa
    pino_y=8.0,          # Y do centro dos pinos
    texto_y=18.0,        # Y do centro dos números
    texto_alt=5.5,       # altura da fonte (o dígito sai com ~5,3 mm; mínimo do doc: 5)
    texto_prof=1.0,      # profundidade da gravação (design-fdm.md, seção 12)
    raio_canto=3.0,      # cantos verticais da placa
    chanfro_base=0.4,    # anti elephant foot (placa, pinos e boca dos alojamentos)
    sobra_corte=1.0,     # quanto os cortadores passam da face (sem face coincidente)
    tol_dist=0.01,       # tolerância da checagem pino x placa
    stl_linear=0.01,     # desvio da malha do STL (mm): come no máximo isso de cada lado da folga
    stl_angular=0.1,     # desvio angular da malha do STL (rad)
)
av.ler_parametros(P, sys.argv[1:])

N = 6
COR_PLACA, COR_PINO = "2F5D8C", "E07A2F"
AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "saida")
FONTE = next((f for f in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                          "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf") if os.path.exists(f)), None)

mm = {"folga_ini", "folga_passo", "pino_d", "bulbo", "bulbo_z", "espessura", "pino_acima", "fenda_larg",
      "fenda_prof", "passo", "margem", "largura", "pino_y", "texto_y", "texto_alt", "texto_prof",
      "raio_canto", "chanfro_base", "sobra_corte"}
coment = av.comentarios(__file__, P)
MEDIDAS = [("Entradas", None, "mude aqui e recalcule")]
MEDIDAS += [(k, f"{v:g} mm" if k in mm else f"{v:g}", coment.get(k, "")) for k, v in P.items()
            if k not in ("tol_dist", "stl_linear", "stl_angular")]
MEDIDAS += [
    ("Calculadas", None, "não editar"),
    ("raio", "=pino_d / 2", "raio do pino"),
    ("altura_pino", "=espessura + pino_acima", ""),
    ("comprimento", f"={N - 1} * passo + 2 * margem", "X da placa"),
]
for i in range(1, N + 1):
    MEDIDAS += [(f"folga{i}", f"=folga_ini + {i - 1} * folga_passo", f"folga por lado do pino {i}"),
                (f"x{i}", f"=margem + {i - 1} * passo", f"X do centro do pino {i}")]


def montar():
    doc = App.newDocument("ReguaFolgas")
    av.planilha(doc, MEDIDAS)

    # 1. Placa: base chanfrada (loft de 45 graus) + corpo reto
    placa = doc.addObject("PartDesign::Body", "Placa")
    placa.Origin.Label = "OrigemPlaca"
    xy = av.plano(placa, "XY")
    cx, cy = f"{M}comprimento / 2", f"{M}largura / 2"
    s0 = av.esboco(placa, "BaseChanfro", xy)
    av.retangulo(s0, doc, f"{M}comprimento - 2 * {M}chanfro_base", f"{M}largura - 2 * {M}chanfro_base",
                 cx, cy, f"{M}raio_canto - {M}chanfro_base")
    s1 = av.esboco(placa, "Contorno", xy, z=f"{M}chanfro_base")
    av.retangulo(s1, doc, f"{M}comprimento", f"{M}largura", cx, cy, f"{M}raio_canto")
    base = placa.newObject("PartDesign::AdditiveLoft", "Chanfro")
    base.Profile = s0
    base.Sections = [s1]
    base.Ruled = True
    s2 = av.esboco(placa, "Topo", xy, z=f"{M}chanfro_base")
    av.retangulo(s2, doc, f"{M}comprimento", f"{M}largura", cx, cy, f"{M}raio_canto")
    corpo = placa.newObject("PartDesign::Pad", "Corpo")
    corpo.Profile = s2
    corpo.setExpression("Length", f"{M}espessura - {M}chanfro_base")
    av.recomputar(doc, "placa")

    # 2. Alojamentos: o perfil do pino afastado da folga na normal de cada face.
    #    Nas faces de 45 graus o afastamento normal c vira c*sqrt(2) no raio e as
    #    quinas se deslocam c*(sqrt(2) - 1) na altura.
    xz = av.plano(placa, "XZ")
    r, b, z1, t, ch, s = (f"{M}raio", f"{M}bulbo", f"{M}bulbo_z", f"{M}espessura", f"{M}chanfro_base", f"{M}sobra_corte")
    for i in range(1, N + 1):
        c = f"{M}folga{i}"
        sk = av.esboco(placa, f"PerfilAlojamento{i}", xz, x=f"{M}x{i}", z=f"-{M}pino_y")
        av.poligono(sk, doc, [
            (0, f"-{s}"),
            (f"{r} + {c} + {ch} + {s}", f"-{s}"),
            (f"{r} + {c}", ch),
            (f"{r} + {c}", f"{z1} - {c} * (sqrt(2) - 1)"),
            (f"{r} + {b} + {c} * sqrt(2)", f"{z1} + {b}"),
            (f"{r} + {c}", f"{z1} + 2 * {b} + {c} * (sqrt(2) - 1)"),
            (f"{r} + {c}", f"{t} + {s}"),
            (0, f"{t} + {s}"),
        ])
        g = placa.newObject("PartDesign::Groove", f"Alojamento{i}")
        g.Profile = sk
        g.ReferenceAxis = (sk, ["V_Axis"])
        g.Angle = 360
    av.recomputar(doc, "alojamentos dos pinos")

    # 3. Números gravados no topo (texto do Draft, recortado da placa)
    final = placa
    if FONTE:
        import Draft
        textos = []
        for i in range(1, N + 1):
            f = av.valor(doc, f"{M}folga{i}")
            txt = Draft.make_shapestring(f"{round(f * 100):d}", FONTE, P["texto_alt"])
            txt.Label = f"Numero{i}"
            txt.Justification = "Middle-Center"
            txt.setExpression(".Placement.Base.x", f"{M}x{i}")
            txt.setExpression(".Placement.Base.y", f"{M}texto_y")
            txt.setExpression(".Placement.Base.z", f"{M}espessura - {M}texto_prof")
            ext = doc.addObject("Part::Extrusion", f"Gravacao{i}")
            ext.Base = txt
            ext.DirMode = "Custom"
            ext.Dir = App.Vector(0, 0, 1)
            ext.setExpression("LengthFwd", f"{M}texto_prof + {M}sobra_corte")
            ext.Solid = True
            textos.append(ext)
        gravacoes = doc.addObject("Part::MultiFuse", "Gravacoes")
        gravacoes.Shapes = textos
        final = doc.addObject("Part::Cut", "PlacaGravada")
        final.Base, final.Tool = placa, gravacoes
        av.recomputar(doc, "números gravados")
    else:
        print("aviso: fonte não encontrada, números ficaram de fora")

    # 4. Pinos, um corpo para cada
    pinos = []
    for i in range(1, N + 1):
        f = av.valor(doc, f"{M}folga{i}")
        pino = doc.addObject("PartDesign::Body", f"Pino{round(f * 100):d}")
        sk = av.esboco(pino, f"PerfilPino{i}", av.plano(pino, "XZ"), x=f"{M}x{i}", z=f"-{M}pino_y")
        av.poligono(sk, doc, [
            (0, 0),
            (f"{r} - {ch}", 0),
            (r, ch),
            (r, z1),
            (f"{r} + {b}", f"{z1} + {b}"),
            (r, f"{z1} + 2 * {b}"),
            (r, f"{M}altura_pino"),
            (0, f"{M}altura_pino"),
        ])
        rev = pino.newObject("PartDesign::Revolution", f"GiroPino{i}")
        rev.Profile = sk
        rev.ReferenceAxis = (sk, ["V_Axis"])
        rev.Angle = 360
        sf = av.esboco(pino, f"EsbocoFenda{i}", av.plano(pino, "XY"), z=f"{M}altura_pino")
        av.retangulo(sf, doc, f"{M}pino_d + 2 * {s}", f"{M}fenda_larg", f"{M}x{i}", f"{M}pino_y")
        fenda = pino.newObject("PartDesign::Pocket", f"Fenda{i}")
        fenda.Profile = sf
        fenda.setExpression("Length", f"{M}fenda_prof")
        pino.Origin.Label = f"Origem{i}"
        av.cor(pino, COR_PINO)
        pinos.append(pino)
    av.recomputar(doc, "pinos")

    av.cor(final, COR_PLACA)
    grupo = doc.addObject("App::DocumentObjectGroup", "PecasParaImprimir")
    for o in [final] + pinos:
        grupo.addObject(o)
    av.esconder_auxiliares(doc)
    if final is not placa:
        placa.Visibility = False
    return doc, final, pinos


def verificar(doc, placa, pinos):
    """Esboços sem grau de liberdade, sólidos válidos, nada encostando e a distância
    real entre cada pino e a placa igual à folga pedida."""
    problemas = []
    soltos = [o.Label for o in doc.Objects if "Sketch" in o.TypeId and not av.esboco_restrito(o)]
    if soltos:
        problemas.append("esboço com grau de liberdade: " + ", ".join(soltos))
    for i, pn in enumerate(pinos, start=1):
        f = av.valor(doc, f"{M}folga{i}")
        if not pn.Shape.isValid():
            problemas.append(f"{pn.Label} inválido")
        if pn.Shape.common(placa.Shape).Volume > 1e-6:
            problemas.append(f"{pn.Label} encosta na placa")
        d = pn.Shape.distToShape(placa.Shape)[0]
        print(f"   {pn.Label}: folga pedida {f:.2f} mm, distância medida {d:.3f} mm")
        if d < f - P["tol_dist"]:
            problemas.append(f"{pn.Label}: distância {d:.3f} < folga {f}")
    if not placa.Shape.isValid() or len(placa.Shape.Solids) != 1:
        problemas.append("placa inválida ou com mais de 1 sólido")
    return problemas


doc, placa, pinos = montar()
print("parâmetros:", ", ".join(f"{k}={v:g}" for k, v in P.items()))
ok = validacao.conferir(
    doc, pecas=[placa] + pinos, pasta_saida=SAIDA, nome="regua-folgas",
    mudancas=[("pino_d", "9 mm"), ("espessura", "9 mm"), ("passo", "16 mm"), ("folga_ini", "0.2 mm")],
    problemas=verificar(doc, placa, pinos), stl_por_peca=False,
    linear=P["stl_linear"], angular=P["stl_angular"])
if not ok:
    raise SystemExit("peça inválida: ver as linhas FALHOU acima")
