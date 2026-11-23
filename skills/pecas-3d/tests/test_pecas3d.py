# Testes da lib Part. Rodar: p3d gerar tests/test_pecas3d.py   (exit != 0 se algo falhar)
import math
import os
import shutil
import tempfile

import FreeCAD as App
import Part

import pecas3d as p3

V = App.Vector
falhas = []


def check(nome, cond, info=""):
    print(f"[{'ok' if cond else 'FALHOU'}] {nome} {info}")
    if not cond:
        falhas.append(nome)


def perto(a, b, tol=1e-3):
    return abs(a - b) <= tol * max(1.0, abs(b))


# caixa simples e com fillet vertical
c = p3.caixa(20, 10, 5)
check("caixa volume", perto(c.Volume, 1000), c.Volume)
cr = p3.caixa(20, 10, 5, raio=2)
esperado = 1000 - 4 * (4 - math.pi) * 5  # 4 cantos de (r^2 - pi r^2/4) * h
check("caixa raio vertical", perto(cr.Volume, esperado) and cr.isValid(), f"{cr.Volume:.3f} vs {esperado:.3f}")
crt = p3.caixa(20, 10, 5, raio=2, raio_topo=1)
check("caixa raio topo", crt.isValid() and crt.Volume < cr.Volume and crt.BoundBox.ZLength == 5)
cc = p3.caixa(20, 10, 5, centro_xy=True, chanfro=0.5)
check("caixa centrada+chanfro", perto(cc.BoundBox.XMin, -10) and cc.isValid())

# cilindro em eixo arbitrário
cy = p3.cilindro(10, 20, (0, 0, 0), (1, 0, 0))
check("cilindro eixo X", perto(cy.Volume, math.pi * 25 * 20) and perto(cy.BoundBox.XLength, 20))

# furo passante
bloco = p3.caixa(20, 20, 10)
f = p3.cortar(bloco, p3.furo_passante(5, 10, (10, 10, 10)))
check("furo passante", perto(f.Volume, 4000 - math.pi * 6.25 * 10) and len(f.Solids) == 1)

# furo escareado M3: volume removido = cilindro + cone (90 graus)
t = p3.PARAFUSOS["M3"]
fe = p3.cortar(bloco, p3.furo_parafuso("M3", 10, (10, 10, 10)))
dk, dp = t["cab_esc"] + 0.3, t["passagem"]
h = (dk - dp) / 2
cone = math.pi * h / 3 * ((dk / 2) ** 2 + (dk / 2) * (dp / 2) + (dp / 2) ** 2)
rem = math.pi * (dp / 2) ** 2 * (10 - h) + cone
check("furo escareado M3", perto(4000 - fe.Volume, rem, 1e-3) and fe.isValid(), f"removido {4000 - fe.Volume:.3f} vs {rem:.3f}")
fc = p3.cortar(bloco, p3.furo_parafuso("M3", 10, (10, 10, 10), cabeca="cilindrica"))
fsimples = p3.cortar(bloco, p3.furo_parafuso("M3", 10, (10, 10, 10), cabeca=None))
check("furo cabeça cilíndrica", fc.isValid() and fc.Volume < fsimples.Volume)

# porca: hexágono s=5.5+0.3, área = (sqrt3/2) s^2
fp = p3.cortar(bloco, p3.alojamento_porca("M3", (10, 10, 0), (0, 0, 1)))
s = 5.8
hh = t["m"] + 0.3
check("alojamento porca M3", perto(4000 - fp.Volume, math.sqrt(3) / 2 * s * s * hh, 1e-3), f"{4000 - fp.Volume:.3f}")
fp2 = p3.cortar(bloco, p3.alojamento_porca("M3", (10, 10, 0), (0, 0, 1), com_furo=10, rot=30))
check("porca + furo", fp2.isValid() and len(fp2.Solids) == 1)
# porca por medida custom (s em mm) e em eixo horizontal
fp3 = p3.cortar(bloco, p3.alojamento_porca(s=6.0, altura=3, pos=(0, 10, 5), eixo=(1, 0, 0), m="M3"))
check("porca s custom eixo X", fp3.isValid() and perto(fp3.BoundBox.XLength, 20))

# inserto térmico
fi = p3.cortar(bloco, p3.furo_inserto("M3", (10, 10, 10)))
check("furo inserto M3", fi.isValid() and fi.Volume < 4000)

# teardrop horizontal ao longo de X, ponta para +Z
gt = p3.furo_gota(6, 20, (0, 10, 5), eixo=(1, 0, 0))
bb = gt.BoundBox
check("gota: ponta para cima", perto(bb.ZMax - 5, 3 * math.sqrt(2), 1e-3) and perto(5 - bb.ZMin, 3), f"zmax-5={bb.ZMax - 5:.3f}")
fg = p3.cortar(bloco, gt)
check("gota corta passante", fg.isValid() and len(fg.Solids) == 1)
gtt = p3.furo_gota(6, 20, (0, 10, 5), eixo=(1, 0, 0), truncar=True)
check("gota truncada", perto(gtt.BoundBox.ZMax - 5, 3, 1e-3))

# chanfro de base
cb = p3.chanfro_base(p3.cortar(bloco, p3.furo_passante(5, 10, (10, 10, 10))), 0.5)
removido = f.Volume - cb.Volume
check("chanfro base só externo", cb.isValid() and perto(removido, 0.5 * 0.5 / 2 * 80, 0.02), f"removido {removido:.3f}")
cbf = p3.chanfro_base(p3.cortar(bloco, p3.furo_passante(5, 10, (10, 10, 10))), 0.5, incluir_furos=True)
check("chanfro base com furos", cbf.Volume < cb.Volume)

# seletores
check("arestas verticais caixa", len(p3.arestas_paralelas(bloco, (0, 0, 1))) == 4)
check("arestas plano z=10", len(p3.arestas_no_plano_z(bloco, 10)) == 4)
check("faces normal -Z", len(p3.faces_normal(bloco, (0, 0, -1))) == 1)

# relatório e exportação
r = p3.relatorio(fe, "teste-escareado")
check("relatorio", r["valido"] and r["solidos"] == 1 and perto(r["massa_g"]["PLA"], fe.Volume / 1000 * 1.24, 1e-2))
tmp = tempfile.mkdtemp()
out = p3.exportar(fe, tmp, "teste")
check("export arquivos", all(os.path.getsize(out[k]) > 0 for k in ("fcstd", "step", "stl")))
check("STL fechado/manifold", out["stl_check"]["ok"])
check("STL volume ~ sólido", perto(out["stl_check"]["volume_cm3"], fe.Volume / 1000, 5e-3))
re = Part.Shape()
re.read(out["step"])
check("STEP relido", perto(re.Volume, fe.Volume, 1e-4) and len(re.Solids) == 1, f"{re.Volume:.3f}")
doc = App.openDocument(out["fcstd"])
check("FCStd relido", perto(doc.Objects[0].Shape.Volume, fe.Volume, 1e-6))
App.closeDocument(doc.Name)
shutil.rmtree(tmp, ignore_errors=True)

print(f"\n{len(falhas)} falha(s)" + (f": {falhas}" if falhas else ""))
if falhas:
    raise SystemExit(1)
