# Par de engrenagens para abrir e fechar por motor um registro de esfera de PVC de 100 mm
# (alavanca em T, laranja). Duas peças, montadas como projeto nativo do FreeCAD:
# - Coroa: senta em cima da alavanca do registro. O rasgo de baixo abraça o braço da
#   alavanca e quatro canais verticais levam abraçadeiras de nylon que prendem a coroa
#   no braço. Furo no centro para alinhar com o eixo do registro.
# - Pinhão: vai no eixo do motor (eixo com chato em D, parafuso M3 de trava com porca).
# Relação 48:12 = 4:1. O registro gira 90 graus, então o motor dá 1 volta por manobra.
#
# Impressão: as duas peças com os dentes na mesa. A coroa vai virada ao contrário na
# alavanca (rasgo para baixo). O arquivo mostra as duas engrenadas, do jeito que imprimem.
#
# Gerar: p3d gerar engrenagem-registro/peca.py [param=valor ...]
# Abrir: p3d abrir engrenagem-registro/saida/engrenagem-registro.FCStd
import math
import os
import sys

import FreeCAD as App
import Part
import Sketcher
from InvoluteGearFeature import _InvoluteGear

import arvore as av
import pecas3d as p3
import validacao
from arvore import M

P = dict(
    modulo=2.5,             # módulo dos dentes (mm); maior = dente mais forte e mais grosso
    dentes_coroa=48,        # dentes da coroa (vai no registro)
    dentes_pinhao=12,       # dentes do pinhão (vai no motor); relação = coroa / pinhão
    angulo_pressao=20,      # ângulo de pressão dos dentes (graus)
    desloc_pinhao=0.3,      # deslocamento de perfil do pinhão (evita dente fino na raiz com 12 dentes)
    largura_dente=22.0,     # largura de face dos dentes (altura da faixa dentada), igual nas duas
    folga_engrenamento=0.6, # somada à distância entre centros: ~0,2 por flanco (0,6 x sen 20), deslizante
    alavanca_larg=40.0,     # MEDIR: largura do braço da alavanca perto do centro (estimada da foto)
    alavanca_esp=13.0,      # MEDIR: espessura do braço da alavanca (estimada do desenho)
    saliencia_braco=4.0,    # quanto do braço fica abaixo da saia (o rasgo pega o resto)
    folga_encaixe=0.3,      # folga por lado no rasgo (deslizante 0,2 + 0,1 de encaixe grande)
    saia_d=100.0,           # diâmetro da saia que abraça o braço
    furo_centro_d=20.0,     # MEDIR: furo do centro (alinhar com o eixo e o que houver no topo da alavanca)
    abrac_larg=5.4,         # canal da abraçadeira: largura (abraçadeira 4,8 + folga 0,6)
    abrac_esp=2.0,          # canal da abraçadeira: espessura (abraçadeira ~1,3 + folga)
    abrac_x=32.0,           # distância do centro até os canais, ao longo do braço
    parede_abrac=1.7,       # parede entre o rasgo e o canal (4 perímetros)
    eixo_d=6.0,             # MEDIR: diâmetro do eixo do motor (JGB37-520 / JGY370 = 6 mm)
    eixo_plano=5.5,         # MEDIR: medida do chato do eixo D até o lado redondo oposto
    folga_eixo=0.2,         # folga diametral no eixo do motor (justo)
    comp_furo=0.15,         # compensação de furo vertical (docs/tolerancias-encaixes.md)
    eixo_comp=14.0,         # MEDIR: comprimento útil do eixo do motor (entra pela face de cima do pinhão)
    trava_d=3.6,            # furo horizontal do prisioneiro M3 de trava (série grossa)
    porca_s=5.8,            # alojamento da porca M3: entre faces (5,5 + 0,3)
    porca_m=2.7,            # alojamento da porca M3: espessura (2,4 + 0,3)
    porca_r=4.0,            # raio da face interna do alojamento da porca
    folga_fundo_porca=0.5,  # alojamento da porca desce isso abaixo da porca
    sobra_corte=1.0,        # quanto os cortadores passam da face
    sigma_adm=14.0,         # tensão admissível no pé do dente (MPa): flexão do ASA 65 / 4,5 (sol e umidade)
    stl_linear=0.02,        # desvio da malha do STL (mm)
    stl_angular=0.1,        # desvio angular da malha do STL (rad)
)
av.ler_parametros(P, sys.argv[1:])

COR_COROA, COR_PINHAO = "2F5D8C", "E07A2F"
AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "saida")
NAO_MM = {"dentes_coroa", "dentes_pinhao", "desloc_pinhao", "angulo_pressao", "sigma_adm", "stl_linear", "stl_angular"}

coment = av.comentarios(__file__, P)
MEDIDAS = [("Entradas", None, "mude aqui e recalcule")]
MEDIDAS += [(k, f"{v:g} deg" if k == "angulo_pressao" else f"{v:g}" if k in NAO_MM else f"{v:g} mm", coment.get(k, "")) for k, v in P.items()
            if k not in ("sigma_adm", "stl_linear", "stl_angular")]
MEDIDAS += [
    ("Calculadas", None, "não editar"),
    ("desloc_coroa", "=-desloc_pinhao", "deslocamento da coroa (soma zero: distância entre centros padrão)"),
    ("relacao", "=dentes_coroa / dentes_pinhao", "voltas do motor por volta do registro"),
    ("distancia_centros", "=modulo * (dentes_coroa + dentes_pinhao) / 2 + folga_engrenamento",
     "distância entre o eixo do registro e o eixo do motor (usar no suporte do motor)"),
    ("encaixe_larg", "=alavanca_larg + 2 * folga_encaixe", "largura do rasgo"),
    ("abrac_y", "=encaixe_larg / 2 + parede_abrac + abrac_esp / 2", "Y do centro dos canais"),
    ("furo_eixo_d", "=eixo_d + folga_eixo + comp_furo", "furo do eixo do motor"),
    ("furo_plano", "=eixo_plano - eixo_d / 2 + folga_eixo / 2", "do centro do furo até o chato"),
    ("encaixe_prof", "=alavanca_esp - saliencia_braco", "quanto do braço entra no rasgo"),
    ("trava_z", "=largura_dente - eixo_comp / 2", "altura do prisioneiro: meio do trecho com eixo"),
    ("altura_coroa", "=largura_dente + encaixe_prof", ""),
    ("giro_pinhao", "0 deg", "só visual: gira o pinhão para os dentes engrenarem na vista"),
]


def perfil_engrenagem(corpo, nome, dentes, desloc):
    g = corpo.newObject("Part::Part2DObjectPython", nome)
    _InvoluteGear(g)
    g.AttachmentSupport = [(av.plano(corpo, "XY"), "")]
    g.MapMode = "FlatFace"
    g.setExpression("NumberOfTeeth", f"{M}{dentes}")
    g.setExpression("Modules", f"{M}modulo")
    g.setExpression("ProfileShiftCoefficient", f"{M}{desloc}")
    g.setExpression("PressureAngle", f"{M}angulo_pressao")
    return g


def furo_d(sk, doc, d, plano_dist):
    """Furo em D com centro na origem: arco + reta vertical em x = plano_dist; restrito."""
    R, X = av.valor(doc, d) / 2, av.valor(doc, plano_dist)
    a = math.acos(X / R)
    arco = sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(0, 0, 0), App.Vector(0, 0, 1), R), a, 2 * math.pi - a))
    reta = sk.addGeometry(Part.LineSegment(App.Vector(X, -R * math.sin(a), 0), App.Vector(X, R * math.sin(a), 0)))
    sk.addConstraint(Sketcher.Constraint("Coincident", arco, 2, reta, 1))
    sk.addConstraint(Sketcher.Constraint("Coincident", reta, 2, arco, 1))
    sk.addConstraint(Sketcher.Constraint("Vertical", reta))
    sk.addConstraint(Sketcher.Constraint("Coincident", arco, 3, -1, 1))
    sk.setExpression(f"Constraints[{sk.addConstraint(Sketcher.Constraint('Diameter', arco, 2 * R))}]", d)
    sk.setExpression(f"Constraints[{sk.addConstraint(Sketcher.Constraint('DistanceX', arco, 3, reta, 1, X))}]", plano_dist)


def montar():
    doc = App.newDocument("EngrenagemRegistro")
    av.planilha(doc, MEDIDAS)
    s = f"{M}sobra_corte"

    # 1. Coroa: faixa dentada na mesa, saia em cima com o rasgo do braço da alavanca
    coroa = doc.addObject("PartDesign::Body", "Coroa")
    coroa.Origin.Label = "OrigemCoroa"
    xy = av.plano(coroa, "XY")
    pc = perfil_engrenagem(coroa, "PerfilCoroa", "dentes_coroa", "desloc_coroa")
    dentes = coroa.newObject("PartDesign::Pad", "DentesCoroa")
    dentes.Profile = pc
    dentes.setExpression("Length", f"{M}largura_dente")
    sk = av.esboco(coroa, "EsbocoSaia", xy, z=f"{M}largura_dente")
    av.circulo(sk, doc, f"{M}saia_d", 0, 0)
    saia = coroa.newObject("PartDesign::Pad", "Saia")
    saia.Profile = sk
    saia.setExpression("Length", f"{M}encaixe_prof")
    av.recomputar(doc, "coroa: dentes e saia")

    topo = f"{M}altura_coroa"
    sk = av.esboco(coroa, "EsbocoRasgo", xy, z=topo)
    av.retangulo(sk, doc, f"{M}saia_d + 2 * {s}", f"{M}encaixe_larg", 0, 0)
    rasgo = coroa.newObject("PartDesign::Pocket", "RasgoDaAlavanca")
    rasgo.Profile = sk
    rasgo.setExpression("Length", f"{M}encaixe_prof")
    sk = av.esboco(coroa, "EsbocoFuroCentro", xy, z=topo)
    av.circulo(sk, doc, f"{M}furo_centro_d", 0, 0)
    furo = coroa.newObject("PartDesign::Pocket", "FuroDoCentro")
    furo.Profile = sk
    furo.Type = "ThroughAll"
    sk = av.esboco(coroa, "EsbocoAbracadeiras", xy, z=topo)
    for sx in ("", "-"):
        for sy in ("", "-"):
            av.retangulo(sk, doc, f"{M}abrac_larg", f"{M}abrac_esp", f"{sx}{M}abrac_x", f"{sy}{M}abrac_y")
    canais = coroa.newObject("PartDesign::Pocket", "CanaisDasAbracadeiras")
    canais.Profile = sk
    canais.Type = "ThroughAll"
    av.cor(coroa, COR_COROA)
    av.recomputar(doc, "coroa: rasgo, furo e canais")

    # 2. Pinhão: só a faixa dentada. O eixo entra pela face de cima (encostada no motor),
    #    o prisioneiro M3 sai num vão entre dentes e a porca fica presa pela face do motor.
    pinhao = doc.addObject("PartDesign::Body", "Pinhao")
    pinhao.Origin.Label = "OrigemPinhao"
    pinhao.setExpression(".Placement.Base.x", f"{M}distancia_centros")
    pinhao.setExpression(".Placement.Rotation.Angle", f"{M}giro_pinhao")
    xy = av.plano(pinhao, "XY")
    pp = perfil_engrenagem(pinhao, "PerfilPinhao", "dentes_pinhao", "desloc_pinhao")
    pp.setExpression(".AttachmentOffset.Rotation.Angle", f"180 deg / {M}dentes_pinhao")
    dp = pinhao.newObject("PartDesign::Pad", "DentesPinhao")
    dp.Profile = pp
    dp.setExpression("Length", f"{M}largura_dente")
    av.recomputar(doc, "pinhão: dentes")

    topo = f"{M}largura_dente"
    sk = av.esboco(pinhao, "EsbocoFuroEixo", xy, z=topo)
    furo_d(sk, doc, f"{M}furo_eixo_d", f"{M}furo_plano")
    fe = pinhao.newObject("PartDesign::Pocket", "FuroDoEixoD")
    fe.Profile = sk
    fe.Type = "ThroughAll"
    sk = av.esboco(pinhao, "EsbocoTrava", av.plano(pinhao, "YZ"), z=f"{M}modulo * (2 + {M}dentes_pinhao) / 2 + {s}")
    av.circulo(sk, doc, f"{M}trava_d", 0, f"{M}trava_z")
    trava = pinhao.newObject("PartDesign::Pocket", "FuroDoPrisioneiroM3")
    trava.Profile = sk
    trava.setExpression("Length", f"{M}modulo * (2 + {M}dentes_pinhao) / 2 + {s}")
    sk = av.esboco(pinhao, "EsbocoPorca", xy, z=topo)
    av.retangulo(sk, doc, f"{M}porca_m", f"{M}porca_s", f"{M}porca_r + {M}porca_m / 2", 0)
    porca = pinhao.newObject("PartDesign::Pocket", "AlojamentoDaPorcaM3")
    porca.Profile = sk
    porca.setExpression("Length", f"{M}eixo_comp / 2 + {M}porca_s / 2 + {M}folga_fundo_porca")
    av.cor(pinhao, COR_PINHAO)
    av.recomputar(doc, "pinhão: furo em D e trava")

    grupo = doc.addObject("App::DocumentObjectGroup", "PecasParaImprimir")
    for o in (coroa, pinhao):
        grupo.addObject(o)
    av.esconder_auxiliares(doc)
    return doc, coroa, pinhao


def engrenar(doc, coroa, pinhao):
    """Acha o giro do pinhão que deixa os dentes no meio do vão (só para a vista).
    Gira uma cópia do sólido em vez de recalcular a árvore a cada tentativa."""
    passo = 360.0 / P["dentes_pinhao"]
    centro = App.Vector(av.valor(doc, f"{M}distancia_centros"), 0, 0)
    base, alvo = pinhao.Shape.copy(), coroa.Shape
    melhor = (-1.0, 0.0)
    for i in range(36):
        ang = i * passo / 36
        s = base.copy()
        s.rotate(centro, App.Vector(0, 0, 1), ang)
        d = s.distToShape(alvo)[0]
        if d > melhor[0]:
            melhor = (d, ang)
    m = doc.getObject("Medidas")
    m.set(m.getCellFromAlias("giro_pinhao"), f"{melhor[1]:.3f} deg")
    av.recomputar(doc, f"engrenamento (giro {melhor[1]:.1f} graus, menor folga {melhor[0]:.2f} mm)")
    return melhor[0]


def verificar(doc, coroa, pinhao):
    problemas = []
    soltos = [o.Label for o in doc.Objects if o.TypeId == "Sketcher::SketchObject" and not av.esboco_restrito(o)]
    if soltos:
        problemas.append("esboço com grau de liberdade: " + ", ".join(soltos))
    for b in (coroa, pinhao):
        if not b.Shape.isValid() or len(b.Shape.Solids) != 1:
            problemas.append(f"{b.Label} inválido ou com mais de 1 sólido")
    if pinhao.Shape.common(coroa.Shape).Volume > 1e-6:
        problemas.append("pinhão encosta na coroa")
    if av.valor(doc, f"{M}eixo_comp") > av.valor(doc, f"{M}largura_dente"):
        problemas.append("eixo do motor mais comprido que o pinhão")
    if av.valor(doc, f"{M}encaixe_prof") < av.valor(doc, f"{M}saliencia_braco"):
        problemas.append("rasgo raso demais para o braço")
    # o prisioneiro tem que sair num vão entre dentes, não no meio de um dente
    r_pe = av.valor(doc, f"{M}modulo") * (P["dentes_pinhao"] / 2 - 1.25 + P["desloc_pinhao"])
    gp = av.valor(doc, f"{M}giro_pinhao")
    c = pinhao.Placement.Base
    ang = math.radians(gp)
    ponto = c + App.Vector(math.cos(ang), math.sin(ang), 0) * (r_pe + 0.8)
    ponto.z = av.valor(doc, f"{M}trava_z")
    if pinhao.Shape.isInside(ponto, 1e-3, True):
        problemas.append("prisioneiro sai dentro de um dente")
    return problemas


def resistencia():
    """Lewis no pinhão (dente mais fraco): força no dente e torques que o par aguenta."""
    y = {12: 0.245, 13: 0.261, 14: 0.277, 15: 0.290, 16: 0.296, 17: 0.303, 18: 0.309}.get(int(P["dentes_pinhao"]), 0.245)
    f = P["sigma_adm"] * P["largura_dente"] * P["modulo"] * y
    rp = P["modulo"] * P["dentes_pinhao"] / 2000
    rc = P["modulo"] * P["dentes_coroa"] / 2000
    print(f"   Lewis: força admissível no dente {f:.0f} N -> torque no motor até {f * rp:.1f} N.m, "
          f"no registro até {f * rc:.1f} N.m (sem atrito)")


doc, coroa, pinhao = montar()
folga = engrenar(doc, coroa, pinhao)
problemas = verificar(doc, coroa, pinhao)
if folga < P["folga_engrenamento"] * math.sin(math.radians(P["angulo_pressao"])) * 0.8:
    problemas.append(f"folga entre dentes {folga:.2f} mm menor que a esperada")
resistencia()
print(f"   distância entre centros: {av.valor(doc, M + 'distancia_centros'):.2f} mm")
ok = validacao.conferir(
    doc, pecas=[coroa, pinhao], pasta_saida=SAIDA, nome="engrenagem-registro",
    mudancas=[("modulo", "3 mm"), ("dentes_coroa", "44"), ("alavanca_larg", "44 mm"), ("eixo_d", "8 mm"),
              ("largura_dente", "25 mm"), ("alavanca_esp", "15 mm")],
    problemas=problemas, linear=P["stl_linear"], angular=P["stl_angular"])
if not ok:
    raise SystemExit("peça inválida: ver as linhas FALHOU acima")
