# __NOME__: <para que serve a peça, em uma ou duas linhas>.
# Projeto nativo do FreeCAD: corpo do PartDesign, esboços restritos e toda medida na
# planilha "Medidas" (mudar lá e recalcular com Ctrl+R).
#
# Gerar:  p3d gerar __NOME__/peca.py [param=valor ...]
# Abrir:  p3d abrir __NOME__/saida/__NOME__.FCStd
#
# Modelo de partida: placa com cantos arredondados, chanfro anti elephant foot na base e um
# furo passante M3. Troque a geometria do passo 1 em diante pela da sua peça.
import os
import sys

import FreeCAD as App

import arvore as av
import validacao
from arvore import M

NOME = "__NOME__"
P = dict(
    comprimento=60.0,   # X da placa
    largura=30.0,       # Y da placa
    espessura=4.0,      # Z da placa (parede funcional: 4 perímetros ~1,7 mm no mínimo)
    raio_canto=4.0,     # cantos verticais
    chanfro_base=0.4,   # anti elephant foot
    furo_d=3.4,         # furo passante M3 vertical (docs/fixacao.md)
    comp_furo=0.15,     # compensação de furo vertical (docs/tolerancias-encaixes.md)
)
av.ler_parametros(P, sys.argv[1:])

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "saida")
COR = "2F5D8C"

coment = av.comentarios(__file__, P)
MEDIDAS = [("Entradas", None, "mude aqui e recalcule")]
MEDIDAS += [(k, f"{v:g} mm", coment.get(k, "")) for k, v in P.items()]
MEDIDAS += [
    ("Calculadas", None, "não editar"),
    ("furo_cad", "=furo_d + comp_furo", "diâmetro do furo no desenho"),
]

doc = App.newDocument(NOME.replace("-", "_"))
av.planilha(doc, MEDIDAS)

# 1. Placa: base chanfrada (loft reto) + corpo
corpo = doc.addObject("PartDesign::Body", "Placa")
xy = av.plano(corpo, "XY")
ch = f"{M}chanfro_base"
s0 = av.esboco(corpo, "BaseChanfro", xy)
av.retangulo(s0, doc, f"{M}comprimento - 2 * {ch}", f"{M}largura - 2 * {ch}", 0, 0, f"{M}raio_canto - {ch}")
s1 = av.esboco(corpo, "ContornoChanfro", xy, z=ch)
av.retangulo(s1, doc, f"{M}comprimento", f"{M}largura", 0, 0, f"{M}raio_canto")
chanfro = corpo.newObject("PartDesign::AdditiveLoft", "Chanfro")
chanfro.Profile = s0
chanfro.Sections = [s1]
chanfro.Ruled = True
s2 = av.esboco(corpo, "Contorno", xy, z=ch)
av.retangulo(s2, doc, f"{M}comprimento", f"{M}largura", 0, 0, f"{M}raio_canto")
pad = corpo.newObject("PartDesign::Pad", "CorpoDaPlaca")
pad.Profile = s2
pad.setExpression("Length", f"{M}espessura - {ch}")
av.recomputar(doc, "placa")

# 2. Furo passante
sf = av.esboco(corpo, "EsbocoFuro", xy, z=f"{M}espessura")
av.circulo(sf, doc, f"{M}furo_cad", 0, 0)
furo = corpo.newObject("PartDesign::Pocket", "FuroM3")
furo.Profile = sf
furo.Type = "ThroughAll"
av.recomputar(doc, "furo")

av.cor(corpo, COR)
av.esconder_auxiliares(doc)

ok = validacao.conferir(doc, pasta_saida=SAIDA, nome=NOME)
if not ok:
    raise SystemExit("peça inválida: ver as linhas FALHOU acima")
