"""pecas3d - biblioteca de peças para impressão 3D FDM com FreeCAD (Part/CSG).

Unidade: mm. Ângulos: graus. Roda dentro do freecadcmd (`p3d gerar`).

Convenção dos "cortadores" (furos, alojamentos): `pos` é o ponto na superfície
por onde o furo entra e `eixo` é a direção para DENTRO do material.
Ex.: furo de cima para baixo numa face no topo z=10 -> pos=(x, y, 10), eixo=(0, 0, -1).
Todo cortador já sai com uma folga `EPS` para fora da superfície (evita face coplanar).
"""
import contextlib
import math
import os
import sys

import FreeCAD as App
import Part

V = App.Vector
EPS = 0.01   # folga para não deixar faces coincidentes no boolean
TOL = 1e-6

DENSIDADE = {"PLA": 1.24, "PETG": 1.27}  # g/cm3

# Valores para impressão (mm). Furo de passagem = "normal" ISO 273 arredondado.
# Escareado: diâmetro da cabeça DIN 7991 / ISO 10642 (90 graus).
# Cabeça cilíndrica: ISO 4762 (Allen), altura da cabeça = d.
# Porca: ISO 4032, s = medida entre faces, m = altura.
# Inserto térmico: valores típicos (Ruthex/CNC Kitchen) - conferir o datasheet do lote.
# Folgas padrão do projeto em mm (docs/tolerancias-encaixes.md). Diametral = furo - eixo.
# Valores iniciais: calibrar com peça de teste na impressora real.
FOLGAS = dict(
    deslizante=0.4,      # diametral (0,2 por lado)
    justo=0.2,           # diametral
    press_fit=0.0,       # nominal: furo impresso já sai menor
    print_in_place=0.3,  # por lado, XY e Z
    furo_vertical=0.15,  # somar ao diâmetro de furo vertical no CAD (fatiador sem compensação)
)

PARAFUSOS = {
    "M2":   dict(d=2.0, passagem=2.4, cab_esc=4.0,  cab_cil=3.8, h_cil=2.0, s=4.0, m=1.6, ins_d=3.2, ins_l=4.0),
    "M2.5": dict(d=2.5, passagem=2.9, cab_esc=5.0,  cab_cil=4.5, h_cil=2.5, s=5.0, m=2.0, ins_d=3.6, ins_l=5.0),
    "M3":   dict(d=3.0, passagem=3.4, cab_esc=6.0,  cab_cil=5.5, h_cil=3.0, s=5.5, m=2.4, ins_d=4.0, ins_l=5.7),
    "M4":   dict(d=4.0, passagem=4.5, cab_esc=8.0,  cab_cil=7.0, h_cil=4.0, s=7.0, m=3.2, ins_d=5.6, ins_l=8.1),
    "M5":   dict(d=5.0, passagem=5.5, cab_esc=10.0, cab_cil=8.5, h_cil=5.0, s=8.0, m=4.7, ins_d=6.4, ins_l=9.5),
}


def _v(p):
    return p if isinstance(p, App.Vector) else V(*p)


def _unit(p):
    v = V(_v(p))
    if v.Length < TOL:
        raise ValueError("vetor nulo")
    return v.normalize()


def _sistema(pos, eixo, cima=None):
    """Matrix que leva o sistema local (Z = eixo, Y = cima) para o global."""
    z = _unit(eixo)
    if cima is None:
        cima = V(0, 0, 1) if abs(z.z) < 0.9 else V(0, 1, 0)
    y = _v(cima) - z * (_v(cima).dot(z))
    if y.Length < TOL:
        raise ValueError("'cima' não pode ser paralelo ao eixo")
    y.normalize()
    x = y.cross(z)
    p = _v(pos)
    return App.Matrix(x.x, y.x, z.x, p.x,
                      x.y, y.y, z.y, p.y,
                      x.z, y.z, z.z, p.z,
                      0, 0, 0, 1)


def _no_sistema(shape, pos, eixo, cima=None):
    s = shape.copy()
    s.transformShape(_sistema(pos, eixo, cima))
    return s


def _parafuso(m):
    if m not in PARAFUSOS:
        raise ValueError(f"parafuso {m!r} desconhecido; use um de {list(PARAFUSOS)}")
    return PARAFUSOS[m]


# ---------------------------------------------------------------- seleção de arestas

def _dir_aresta(e):
    if not isinstance(e.Curve, (Part.Line, Part.LineSegment)):
        return None
    d = e.Vertexes[-1].Point - e.Vertexes[0].Point
    return d.normalize() if d.Length > TOL else None


def arestas(shape, filtro):
    """Lista de arestas de `shape` para as quais filtro(aresta) é True."""
    return [e for e in shape.Edges if filtro(e)]


def arestas_paralelas(shape, direcao):
    """Arestas retas paralelas a `direcao` (ex.: (0,0,1) = arestas verticais)."""
    d = _unit(direcao)
    return arestas(shape, lambda e: (_dir_aresta(e) is not None
                                      and abs(abs(_dir_aresta(e).dot(d)) - 1) < 1e-6))


def arestas_no_plano_z(shape, z, tol=1e-4):
    """Arestas inteiramente contidas no plano Z = z (retas ou curvas)."""
    return arestas(shape, lambda e: abs(e.BoundBox.ZMin - z) < tol and abs(e.BoundBox.ZMax - z) < tol)


def faces_normal(shape, normal, tol=1e-6):
    """Faces planas cuja normal (para fora) é `normal`."""
    n = _unit(normal)
    out = []
    for f in shape.Faces:
        if isinstance(f.Surface, Part.Plane):
            u0, u1, v0, v1 = f.ParameterRange
            fn = f.normalAt((u0 + u1) / 2, (v0 + v1) / 2)
            if abs(fn.dot(n) - 1) < tol:
                out.append(f)
    return out


def arredondar(shape, raio, lista_arestas):
    return shape.makeFillet(raio, lista_arestas) if (raio > 0 and lista_arestas) else shape


def chanfrar(shape, c, lista_arestas):
    return shape.makeChamfer(c, lista_arestas) if (c > 0 and lista_arestas) else shape


# ---------------------------------------------------------------- primitivas

def caixa(x, y, z, pos=(0, 0, 0), raio=0.0, raio_topo=0.0, chanfro=0.0, centro_xy=False):
    """Bloco x*y*z com canto em `pos` (ou centrado em XY se centro_xy).
    raio: fillet das arestas verticais. raio_topo: fillet das arestas do topo
    (aplicado depois do raio vertical). chanfro: chanfro de todas as arestas
    (alternativa aos fillets)."""
    p = _v(pos)
    if centro_xy:
        p = p - V(x / 2, y / 2, 0)
    s = Part.makeBox(x, y, z, p)
    if chanfro > 0:
        return s.makeChamfer(chanfro, s.Edges)
    s = arredondar(s, raio, arestas_paralelas(s, (0, 0, 1)))
    if raio_topo > 0:
        s = arredondar(s, raio_topo, arestas_no_plano_z(s, p.z + z))
    return s


def cilindro(d, h, pos=(0, 0, 0), eixo=(0, 0, 1)):
    """Cilindro de diâmetro d e altura h, base em pos, crescendo ao longo de eixo."""
    return Part.makeCylinder(d / 2, h, _v(pos), _unit(eixo))


def furo_passante(d, prof, pos, eixo=(0, 0, -1)):
    """Cortador cilíndrico: entra em pos, segue `eixo` por `prof` mm (+ folgas)."""
    e = _unit(eixo)
    return Part.makeCylinder(d / 2, prof + 2 * EPS, _v(pos) - e * EPS, e)


def furo_parafuso(m, prof, pos, eixo=(0, 0, -1), cabeca="escareado", folga_cabeca=0.3,
                  prof_cabeca=None, d_passagem=None):
    """Furo de passagem para parafuso métrico com cabeça.
    cabeca: "escareado" (cone 90 graus, DIN 7991), "cilindrica" (rebaixo para Allen ISO 4762)
    ou None (só passagem). folga_cabeca soma ao diâmetro da cabeça."""
    t = _parafuso(m)
    dp = d_passagem or t["passagem"]
    corte = furo_passante(dp, prof, pos, eixo)
    e = _unit(eixo)
    p = _v(pos)
    if cabeca == "escareado":
        dk = t["cab_esc"] + folga_cabeca
        h = (dk - dp) / 2  # 90 graus: altura = diferença de raio
        cone = Part.makeCone(dk / 2, dp / 2, h, p, e)
        # colar de EPS acima da superfície para o cone não ficar rente
        corte = corte.fuse([cone, Part.makeCylinder(dk / 2, EPS * 2, p - e * EPS * 2, e)])
    elif cabeca == "cilindrica":
        dk = t["cab_cil"] + folga_cabeca
        hk = prof_cabeca if prof_cabeca is not None else t["h_cil"] + 0.2
        corte = corte.fuse(Part.makeCylinder(dk / 2, hk + EPS, p - e * EPS, e))
    elif cabeca is not None:
        raise ValueError("cabeca deve ser 'escareado', 'cilindrica' ou None")
    return corte.removeSplitter()


def prisma_sextavado(s, h, pos=(0, 0, 0), eixo=(0, 0, 1), rot=0.0):
    """Prisma hexagonal com medida entre faces `s`. rot gira em torno do eixo (graus);
    rot=0 deixa duas faces paralelas ao eixo X local."""
    r = s / math.sqrt(3)  # raio circunscrito
    pts = [V(r * math.cos(math.radians(60 * i + rot)), r * math.sin(math.radians(60 * i + rot)), 0)
           for i in range(6)]
    face = Part.Face(Part.makePolygon(pts + [pts[0]]))
    return _no_sistema(face.extrude(V(0, 0, h)), pos, eixo)


def alojamento_porca(m="M3", pos=(0, 0, 0), eixo=(0, 0, -1), altura=None, s=None, folga=0.3,
                     rot=0.0, com_furo=0.0):
    """Cortador sextavado para porca. s (entre faces) e altura saem da tabela se None.
    folga soma ao s (0,3 = 0,15 por lado, docs/fixacao.md); a altura ganha +0.3. com_furo>0 adiciona o furo de passagem com
    essa profundidade total, a partir de pos."""
    t = _parafuso(m)
    s_ = (s if s is not None else t["s"]) + folga
    h = (altura if altura is not None else t["m"] + 0.3)
    e = _unit(eixo)
    corte = prisma_sextavado(s_, h + EPS, _v(pos) - e * EPS, e, rot)
    if com_furo > 0:
        corte = corte.fuse(furo_passante(t["passagem"], com_furo, pos, e)).removeSplitter()
    return corte


def furo_inserto(m="M3", pos=(0, 0, 0), eixo=(0, 0, -1), prof=None, d=None, chanfro=0.4,
                 alivio=1.0):
    """Furo para inserto roscado de fixação a quente. prof padrão = comprimento do inserto
    + alivio (espaço para o plástico deslocado). chanfro de entrada facilita centralizar."""
    t = _parafuso(m)
    d_ = d or t["ins_d"]
    pr = prof if prof is not None else t["ins_l"] + alivio
    e = _unit(eixo)
    p = _v(pos)
    corte = furo_passante(d_, pr, p, e)
    if chanfro > 0:
        cone = Part.makeCone(d_ / 2 + chanfro + EPS, d_ / 2, chanfro + EPS, p - e * EPS, e)
        corte = corte.fuse(cone).removeSplitter()
    return corte


def furo_gota(d, comprimento, pos, eixo=(1, 0, 0), cima=(0, 0, 1), angulo=45.0, truncar=False):
    """Furo horizontal em gota (teardrop): a ponta aponta para `cima` e as paredes
    do topo têm `angulo` graus da horizontal, imprimível sem suporte.
    truncar=True corta a ponta na altura do raio (topo plano, ponte curta)."""
    r = d / 2
    a = math.radians(angulo)
    # pontos de tangência e ponta, no plano local XY (Y = cima)
    tx, ty = r * math.sin(a), r * math.cos(a)
    ponta = r / math.cos(a)
    perfil_circ = Part.Face(Part.Wire(Part.makeCircle(r)))
    tri = Part.Face(Part.makePolygon([V(tx, ty, 0), V(0, ponta, 0), V(-tx, ty, 0), V(0, 0, 0),
                                      V(tx, ty, 0)]))
    perfil = perfil_circ.fuse(tri).removeSplitter().Faces[0]
    solido = perfil.extrude(V(0, 0, comprimento + 2 * EPS))
    if truncar:
        solido = solido.cut(Part.makeBox(4 * r, 4 * r, comprimento + 4 * EPS, V(-2 * r, r, -EPS)))
    e = _unit(eixo)
    return _no_sistema(solido, _v(pos) - e * EPS, e, cima)


def chanfro_base(shape, c=0.4, incluir_furos=False):
    """Chanfra as arestas da face de apoio (Z mínimo) contra elephant foot.
    Por padrão só o contorno externo da face."""
    zmin = shape.BoundBox.ZMin
    sel = []
    for f in faces_normal(shape, (0, 0, -1)):
        if abs(f.BoundBox.ZMax - zmin) > 1e-4:
            continue
        sel += f.Edges if incluir_furos else f.OuterWire.Edges
    return chanfrar(shape, c, sel)


def unir(*shapes):
    """Fuse de várias peças + removeSplitter (limpa faces coplanares)."""
    base, resto = shapes[0], list(shapes[1:])
    return base.fuse(resto).removeSplitter() if resto else base


def cortar(base, *cortadores):
    """Cut de vários cortadores de uma vez + removeSplitter."""
    return base.cut(list(cortadores)).removeSplitter() if cortadores else base


def solido_unico(shape):
    """Garante que o resultado é um Part.Solid (extrai de Compound de 1 sólido)."""
    if shape.ShapeType == "Solid":
        return shape
    if len(shape.Solids) == 1:
        return shape.Solids[0]
    raise ValueError(f"esperava 1 sólido, encontrei {len(shape.Solids)}")


# ---------------------------------------------------------------- saída

@contextlib.contextmanager
def silencio():
    """Cala o stdout/stderr do lado C++ (barra de progresso do FreeCAD, estatísticas
    do OpenCASCADE no STEP) redirecionando os file descriptors 1 e 2 para /dev/null."""
    sys.stdout.flush()
    sys.stderr.flush()
    salvos = [os.dup(1), os.dup(2)]
    nulo = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(nulo, 1)
        os.dup2(nulo, 2)
        yield
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        os.dup2(salvos[0], 1)
        os.dup2(salvos[1], 2)
        for fd in salvos + [nulo]:
            os.close(fd)


def relatorio(shape, nome="peca", imprimir=True):
    """Volume, bounding box, validade e massa estimada. Retorna dict."""
    bb = shape.BoundBox
    vol_cm3 = shape.Volume / 1000.0
    try:
        shape.check(True)
        check_ok, check_msg = True, ""
    except Exception as exc:  # check(True) lança com a lista de problemas
        check_ok, check_msg = False, str(exc).strip()
    r = dict(
        nome=nome,
        volume_cm3=round(vol_cm3, 3),
        bbox_mm=(round(bb.XLength, 3), round(bb.YLength, 3), round(bb.ZLength, 3)),
        bbox_min=(round(bb.XMin, 3), round(bb.YMin, 3), round(bb.ZMin, 3)),
        valido=shape.isValid(),
        check_ok=check_ok,
        solidos=len(shape.Solids),
        faces=len(shape.Faces),
        massa_g={k: round(vol_cm3 * dens, 2) for k, dens in DENSIDADE.items()},
    )
    if imprimir:
        print(f"== relatório: {nome}")
        print(f"   volume      : {r['volume_cm3']} cm3")
        print(f"   bbox (mm)   : {r['bbox_mm'][0]} x {r['bbox_mm'][1]} x {r['bbox_mm'][2]}"
              f"  (min {r['bbox_min']})")
        print(f"   isValid     : {r['valido']}   check(True): {'ok' if check_ok else check_msg}")
        print(f"   sólidos     : {r['solidos']}   faces: {r['faces']}")
        print(f"   massa (100% infill): PLA {r['massa_g']['PLA']} g | PETG {r['massa_g']['PETG']} g")
    return r


def verificar_stl(caminho, imprimir=True):
    """Recarrega o STL com Mesh e checa se é fechado e manifold."""
    import Mesh
    with silencio():
        m = Mesh.Mesh(caminho)
        r = dict(
            facetas=m.CountFacets,
            pontos=m.CountPoints,
            volume_cm3=round(m.Volume / 1000.0, 3),
            fechado=m.isSolid(),
            non_manifold=m.hasNonManifolds(),
            auto_intersecao=m.hasSelfIntersections(),
            normais_ok=not m.hasNonUniformOrientedFacets(),
        )
    r["ok"] = r["fechado"] and not r["non_manifold"] and not r["auto_intersecao"] and r["normais_ok"]
    if imprimir:
        print(f"== STL {os.path.basename(caminho)}: {r['facetas']} facetas, vol {r['volume_cm3']} cm3,"
              f" fechado={r['fechado']} non_manifold={r['non_manifold']}"
              f" auto_intersecao={r['auto_intersecao']} normais_ok={r['normais_ok']}"
              f" -> {'OK' if r['ok'] else 'PROBLEMA'}")
    return r


def exportar(shape, pasta, nome, linear=0.02, angular=0.1, verificar=True):
    """Salva <nome>.FCStd, .step e .stl em `pasta`.
    STL via MeshPart com LinearDeflection (mm) e AngularDeflection (rad) explícitos.
    Retorna dict com os caminhos (e o resultado de verificar_stl se verificar=True)."""
    import Import
    import Mesh
    import MeshPart

    os.makedirs(pasta, exist_ok=True)
    base = os.path.join(os.path.abspath(pasta), nome)
    out = dict(fcstd=base + ".FCStd", step=base + ".step", stl=base + ".stl")

    # saveAs sobre arquivo existente gera <nome>.<data>.FCBak; removendo antes não gera
    if os.path.exists(out["fcstd"]):
        os.remove(out["fcstd"])
    with silencio():
        doc = App.newDocument(nome.replace("-", "_"))
        try:
            obj = doc.addObject("Part::Feature", nome.replace("-", "_"))
            obj.Shape = shape
            doc.recompute()
            doc.saveAs(out["fcstd"])
            Import.export([obj], out["step"])
        finally:
            App.closeDocument(doc.Name)
        malha = MeshPart.meshFromShape(Shape=shape, LinearDeflection=linear,
                                       AngularDeflection=angular, Relative=False)
        malha.write(out["stl"])  # extensão .stl -> STL binário
    print(f"== exportado: {out['fcstd']}\n               {out['step']}\n               {out['stl']}")
    if verificar:
        out["stl_check"] = verificar_stl(out["stl"])
    return out
