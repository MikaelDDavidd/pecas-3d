# Testes da lib/arvore.py (modo árvore editável). Rodar: p3d gerar tests/test_arvore.py
import math

import FreeCAD as App
import Part

import arvore as av
from arvore import M

falhas = []


def check(nome, cond, info=""):
    print(f"[{'ok' if cond else 'FALHOU'}] {nome} {info}")
    if not cond:
        falhas.append(nome)


def perto(a, b, tol=1e-4):
    return abs(a - b) <= tol * max(1.0, abs(b))


doc = App.newDocument("TesteArvore")
m = av.planilha(doc, [("Teste", None, None), ("larg", "40 mm", ""), ("prof", "20 mm", ""), ("raio", "4 mm", ""),
                      ("alt", "5 mm", ""), ("dobro", "=2 * larg", "fórmula"), ("negativo", "-30 mm", "")])
check("planilha valor negativo", perto(av.valor(doc, M + "negativo"), -30))
check("planilha fórmula", perto(av.valor(doc, M + "dobro"), 80))

corpo = doc.addObject("PartDesign::Body", "Corpo")
sk = av.esboco(corpo, "Ret", av.plano(corpo, "XY"))
av.retangulo(sk, doc, M + "larg", M + "prof", 0, 0, M + "raio")
pad = corpo.newObject("PartDesign::Pad", "Pad")
pad.Profile = sk
pad.setExpression("Length", M + "alt")
av.recomputar(doc, "retângulo arredondado")
esperado = (40 * 20 - 4 * (16 - math.pi * 16 / 4)) * 5
check("retângulo arredondado volume", perto(corpo.Shape.Volume, esperado), f"{corpo.Shape.Volume:.3f} vs {esperado:.3f}")
check("retângulo restrito", av.esboco_restrito(sk))

# polígono no XZ deslocado em X e Y, girado no eixo do esboço: cilindro r=5, h=10 em (30, 7)
c2 = doc.addObject("PartDesign::Body", "Rev")
sp = av.esboco(c2, "Perfil", av.plano(c2, "XZ"), x="30 mm", z="-7 mm")
av.poligono(sp, doc, [(0, 0), ("5 mm", 0), ("5 mm", "10 mm"), (0, "10 mm")])
rv = c2.newObject("PartDesign::Revolution", "Rev")
rv.Profile = sp
rv.ReferenceAxis = (sp, ["V_Axis"])
rv.Angle = 360
av.recomputar(doc, "polígono + revolução")
bb = c2.Shape.BoundBox
check("polígono revolução volume", perto(c2.Shape.Volume, math.pi * 25 * 10), f"{c2.Shape.Volume:.3f}")
check("plano XZ: offset z = -Y global", perto(bb.Center.x, 30) and perto(bb.Center.y, 7), f"centro {bb.Center}")
check("polígono restrito", av.esboco_restrito(sp))

# círculo e mudança na planilha propagando
c3 = doc.addObject("PartDesign::Body", "Cil")
sc = av.esboco(c3, "Circ", av.plano(c3, "XY"))
av.circulo(sc, doc, M + "prof", M + "larg", 0)
pc = c3.newObject("PartDesign::Pad", "Pad")
pc.Profile = sc
pc.setExpression("Length", M + "alt")
av.recomputar(doc, "círculo")
check("círculo volume", perto(c3.Shape.Volume, math.pi * 100 * 5) and perto(c3.Shape.BoundBox.Center.x, 40))
m.set(m.getCellFromAlias("alt"), "7 mm")
av.recomputar(doc, "planilha mudou")
check("planilha propaga", perto(c3.Shape.Volume, math.pi * 100 * 7) and perto(corpo.Shape.BoundBox.ZLength, 7))

solto = av.esboco(c3, "Solto", av.plano(c3, "XY"))
solto.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(5, 1, 0)))
doc.recompute()
check("esboço solto detectado", not av.esboco_restrito(solto), f"DoF={solto.DoF}")
c3.removeObject(solto)
doc.removeObject(solto.Name)

av.cor(c3, "FF0000")
check("cor gravada", c3.Cor == "FF0000")

App.closeDocument(doc.Name)
print(f"\n{len(falhas)} falha(s)")
raise SystemExit(1 if falhas else 0)
