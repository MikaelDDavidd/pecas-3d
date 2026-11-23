# FreeCAD via Python headless: referência rápida

Testado no FreeCAD **1.1.4** (Python 3.11) no macOS (Apple Silicon) e no Linux (AppImage oficial, x86_64 e ARM).

Unidade: mm. Ângulos de `rotate`/`revolve`/`Rotation(eixo, ang)`: graus. AngularDeflection da malha: radianos.

---

## 1. Rodar sem tela

### Executáveis

| Sistema | `freecadcmd` (sem tela) | Com janela |
|---|---|---|
| macOS | `/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd` | `/Applications/FreeCAD.app/Contents/MacOS/FreeCAD` |
| Linux (AppImage do `p3d setup`) | `~/.local/share/pecas-3d/freecad-1.1.4/app/usr/bin/freecadcmd` | `.../app/AppRun` |

```bash
freecadcmd --version
freecadcmd -c "import Part; print(Part.makeBox(1,2,3).Volume)"   # 6.0; exit 1 se lançar exceção
```

### Use o `p3d gerar`

```bash
p3d gerar script.py arg1 --opcao=2 "com espaço"
```

O que ele resolve (cada item foi um problema real nos testes):

- **Exit code**: com `freecadcmd script.py`, uma exceção imprime `Exception while processing file` e sai com **0**. Pelo `p3d` sai com **1** e traceback completo. `sys.exit(n)` funciona nos dois casos.

- **Script rodando duas vezes**: com `freecadcmd script.py`, quando o script lança exceção o FreeCAD tenta de novo como arquivo e ele **executa 2 vezes**. Pelo `p3d` executa uma vez só.

- **Argumentos**: o `freecadcmd` interpreta tudo da linha de comando. `--x=2` dá `unrecognised option` e exit 1. Um argumento que é um arquivo existente ele tenta abrir como documento. O `p3d` passa os argumentos por variáveis de ambiente (`FCAD_ARGC`, `FCAD_ARG_0..N`), e o script recebe um `sys.argv = [script, args...]` normal.

- **`__name__`**: direto no `freecadcmd` vale o nome do módulo (`"info"` para `info.py`), então `if __name__ == "__main__":` **não executa**. Pelo `p3d` vale `"__main__"`.

- **Acentos**: com `LC_CTYPE=C` o `sys.stdout.encoding` do freecadcmd é `ascii`, e `print("ç")` lança `UnicodeEncodeError`. O runner reconfigura stdout e stderr para UTF-8 com line buffering (sem isso os prints saem fora de ordem em relação à saída C++).

- **Prompt interativo**: depois do script, o `freecadcmd` cai no `>>>` lendo o stdin. O `p3d` usa `</dev/null`.

- **Ruído**: o `p3d` tira a barra de progresso, o banner e o aviso `Failed to open library ... 3DconnexionNavlib` (driver de mouse 3D ausente, inofensivo).

- **Imports**: `lib/` entra na frente do `sys.path`, então `import arvore` funciona e um arquivo com o mesmo nome na pasta da peça não a substitui.

- **Tempo**: cada script tem limite de 30 min (`P3D_TIMEOUT` em segundos muda).

Para usar outro executável: `FREECADCMD=/caminho/freecadcmd p3d gerar script.py`.

### Módulos disponíveis sem GUI (testado)

`FreeCAD`, `Part`, `Mesh`, `MeshPart`, `Import`, `Sketcher`, `PartDesign`, `Spreadsheet`, `Draft`, `numpy` e `matplotlib` importam sem erro. `FreeCADGui` também importa, mas `FreeCAD.GuiUp == 0`, `ViewObject` é `None` e `Part.show()` não tem para onde mostrar. Não use GUI em script.

A primeira execução depois de instalar leva cerca de 7 s, porque o Gatekeeper verifica o bundle. As seguintes levam cerca de 0,8 s.

---

## 2. API essencial do Part

```python
import FreeCAD as App
import Part
V = App.Vector
```

### 2.1 Primitivas

```python
caixa  = Part.makeBox(20, 10, 5)                            # canto em (0,0,0)
caixa2 = Part.makeBox(20, 10, 5, V(-10, -5, 0))             # canto em (-10,-5,0)
cil    = Part.makeCylinder(3, 12, V(10, 5, -1), V(0, 0, 1)) # RAIO, altura, base, direção
cone   = Part.makeCone(4, 1.5, 3, V(0, 0, 0), V(0, 0, 1))   # r1, r2, altura
esf    = Part.makeSphere(5)
```

`makeCylinder` e `makeCone` recebem **raio**, não diâmetro.

### 2.2 Booleanas

```python
furada = caixa.cut(cil)
unidas = caixa.fuse(Part.makeBox(5, 10, 20))
inter  = caixa.common(esf)
varias = caixa.cut([cil, Part.makeCylinder(1, 10, V(3, 3, -1))])  # lista = uma operação só
limpa  = unidas.removeSplitter()   # funde faces coplanares: 14 -> 8 faces neste caso
```

- Todas devolvem um shape **novo**, e o original não muda.

- O resultado é um **`Compound`** com um `Solid` dentro, não um `Solid` (veja a seção 6). Use `resultado.Solids[0]` quando precisar do sólido.

- Faça o cortador passar um pouco das faces (0,01 mm basta), para não deixar face coincidente com a superfície.

### 2.3 Transformações

```python
a = Part.makeBox(10, 10, 10)
b = a.translated(V(5, 0, 0))            # cópia movida
a.translate(V(0, 0, 1))                 # move no lugar (modifica a)
c = Part.makeBox(10, 2, 2).rotated(V(0, 0, 0), V(0, 0, 1), 90)   # centro, eixo, GRAUS
d = Part.makeBox(10, 2, 2)
d.Placement = App.Placement(V(0, 0, 5), App.Rotation(V(0, 0, 1), 90))  # substitui o Placement
e = Part.makeBox(10, 2, 2)
e.transformShape(App.Placement(V(1, 0, 0), App.Rotation()).toMatrix())  # aplica na geometria
```

`rotate`/`translate` alteram o próprio shape. `rotated`/`translated`/`transformed` devolvem uma cópia. Para alinhar um cortador a um eixo qualquer, monte uma `App.Matrix` com os eixos locais (veja `_sistema()` em `lib/pecas3d.py`).

### 2.4 Fillet/chamfer e seleção de arestas

Não existe seleção por clique em script: você filtra `shape.Edges` por geometria.

```python
blk = Part.makeBox(30, 20, 10)
# arestas verticais (direção Z): z dos dois vértices diferente
verticais = [ed for ed in blk.Edges
             if abs(ed.Vertexes[0].Point.z - ed.Vertexes[1].Point.z) > 1e-6]
# arestas inteiras no plano z=10 (topo); funciona para reta e curva
topo = [ed for ed in blk.Edges if abs(ed.BoundBox.ZMin - 10) < 1e-6 and abs(ed.BoundBox.ZMax - 10) < 1e-6]
base = [ed for ed in blk.Edges if abs(ed.BoundBox.ZMax) < 1e-6]

arred = blk.makeFillet(3, verticais)          # raio, lista de arestas
# depois de um fillet as arestas mudam: selecione de novo no shape NOVO
arred = arred.makeFillet(1, [ed for ed in arred.Edges
                             if abs(ed.BoundBox.ZMin - 10) < 1e-6 and abs(ed.BoundBox.ZMax - 10) < 1e-6])
chanf  = blk.makeChamfer(0.5, base)
chanf2 = blk.makeChamfer(1.0, 2.0, base)      # chanfro assimétrico (d1, d2)

# tipo da curva
circ = [ed for ed in furada.Edges if isinstance(ed.Curve, Part.Circle)]
# arestas de uma face: contorno externo sem os furos
face_base = [f for f in blk.Faces if abs(f.BoundBox.ZMax) < 1e-6][0]
face_base.OuterWire.Edges
```

Direção de uma aresta reta: `(ed.Vertexes[-1].Point - ed.Vertexes[0].Point).normalize()`, e compare com `abs(dir.dot(eixo)) ≈ 1`. Normal de face plana: `f.normalAt(u, v)` no meio de `f.ParameterRange`. A lib tem esses filtros prontos: `arestas_paralelas`, `arestas_no_plano_z`, `faces_normal`.

`makeFillet` falha (lança exceção ou gera sólido inválido) se o raio não cabe na geometria vizinha. Rode `isValid()` depois.

### 2.5 Perfil 2D e extrude

```python
pts = [V(0, 0, 0), V(30, 0, 0), V(30, 4, 0), V(4, 30, 0), V(0, 30, 0), V(0, 0, 0)]  # repete o 1º para fechar
perfil = Part.Face(Part.makePolygon(pts))
prisma = perfil.extrude(V(0, 0, 8))                # Solid

# face com furo: use FaceMakerBullseye
ext = Part.Wire(Part.makeCircle(10))
inn = Part.Wire(Part.makeCircle(4))
arruela = Part.makeFace([ext, inn], "Part::FaceMakerBullseye").extrude(V(0, 0, 2))
# Part.Face([ext, inn]) NÃO fura: isValid() == False e área = externo + interno

# arco por 3 pontos + segmento
arco  = Part.Arc(V(10, 0, 0), V(0, 10, 0), V(-10, 0, 0)).toShape()
fecha = Part.LineSegment(V(-10, 0, 0), V(10, 0, 0)).toShape()
meia_lua = Part.Face(Part.Wire([arco, fecha])).extrude(V(0, 0, 1))
```

### 2.6 Revolve

```python
# perfil no plano XZ, girando em torno de Z
perf = Part.Face(Part.makePolygon([V(5, 0, 0), V(8, 0, 0), V(8, 0, 10), V(5, 0, 10), V(5, 0, 0)]))
tubo = perf.revolve(V(0, 0, 0), V(0, 0, 1), 360)   # base, direção, GRAUS -> Solid
```

Uma face fechada gera `Solid`, e um wire gera só a casca. O perfil não pode cruzar o eixo.

### 2.7 Mirror

```python
peca = Part.makeBox(10, 5, 5, V(2, 0, 0))
espelho = peca.mirror(V(0, 0, 0), V(1, 0, 0))      # ponto do plano, NORMAL do plano (plano x=0)
simetrica = peca.fuse(espelho).removeSplitter()
```

---

## 3. Exportar STL e STEP

```python
s.exportStep("a.step")              # STEP direto do shape

import MeshPart
m = MeshPart.meshFromShape(Shape=s, LinearDeflection=0.02, AngularDeflection=0.1, Relative=False)
m.write("fino.stl")                 # extensão .stl -> STL binário

import Import                       # STEP via documento (mantém nome do objeto)
doc = App.newDocument("Exp")
obj = doc.addObject("Part::Feature", "Peca"); obj.Shape = s; doc.recompute()
Import.export([obj], "b.step")
doc.saveAs("b.FCStd")
App.closeDocument("Exp")

rel = Part.read("a.step")           # reler STEP
```

- **`shape.exportStl(arquivo)` não aceita parâmetro de tessellation** no 1.1 (a assinatura é só `exportStl(filename)`). Para controlar a qualidade, use `MeshPart.meshFromShape(Shape, LinearDeflection, AngularDeflection, Relative)`.

- `LinearDeflection` é o erro máximo em mm entre a malha e a superfície. `AngularDeflection` é o ângulo máximo, em **radianos**, entre facetas vizinhas (o padrão é 0,5 rad, cerca de 28,6°, grosseiro).

- Em raio pequeno, quem manda é o ângulo. Em raio grande, quem manda é o linear. Contagem medida num cilindro de r = 4 mm:

  | linear (mm) | angular (rad) | facetas |
  |---|---|---|
  | 0,1 | 0,5 | 100 |
  | 0,02 | 0,5 | 176 |
  | 0,02 | 0,1 | 500 |
  | 1,0 | 0,1 | 500 |
  | 0,05 | 0,05 | 1004 |

- Padrão da lib: **0,02 mm / 0,1 rad**. O suporte de exemplo sai com 4056 facetas e 200 KB.

- Outras assinaturas de `meshFromShape`: `MaxLength=`, `MaxArea=`, `LocalLength=`, `Deflection=`, `MinLength, MaxLength`, e Netgen (`Fineness=`, `SecondOrder=`...). A lista completa sai em `print(MeshPart.meshFromShape.__doc__)`.

- `Import.export`, `doc.saveAs` e o OpenCASCADE imprimem barra de progresso e "Statistics on Transfer" direto no stdout do C++. `print` do Python e `contextlib.redirect_stdout` não pegam isso. A lib usa `pecas3d.silencio()`, que redireciona os file descriptors 1 e 2.

---

## 4. Checagens de validade

```python
s.isValid()                 # topologia OK (rápido)
s.check(True)               # lança exceção com a lista de erros; True inclui o BOPCheck
len(s.Solids) == 1          # um sólido só (peças soltas = 2+)
s.Volume > 0                # face/casca solta tem volume 0
s.fix(1e-7, 1e-7, 1e-7)     # tenta corrigir tolerâncias (in place)

import Mesh
malha = Mesh.Mesh("fino.stl")
malha.isSolid()                     # fechado (watertight)
malha.hasNonManifolds()             # deve ser False
malha.hasSelfIntersections()        # deve ser False
malha.hasNonUniformOrientedFacets() # normais invertidas, deve ser False
malha.Volume                        # compare com shape.Volume (diferença < 0,5%)
```

Rotina recomendada, que é o que `pecas3d.relatorio` e `pecas3d.exportar` fazem:

1. `isValid()` e `check(True)` sem exceção.

2. `len(Solids) == 1`.

3. BoundBox com as medidas esperadas.

4. Exportar o STL, relê-lo e confirmar que é fechado, sem non-manifold, sem auto-interseção, e com volume igual ao do sólido.

---

## 5. Part (CSG) x PartDesign/Sketcher

**Padrão: Part/CSG** (sólidos + booleanas + fillet), com parâmetros em variáveis Python. É curto, determinístico e fácil de testar, e o próprio script já é o modelo paramétrico.

**Use PartDesign + Sketcher quando:**

- a peça vai ser **editada na GUI** depois, por alguém mexendo nas cotas;

- o perfil tem muitas restrições geométricas (tangências, simetrias) que seriam chatas de calcular na mão;

- você quer que o `.FCStd` abra com histórico de features (Pad, Pocket, Fillet) e uma planilha de parâmetros.

**O custo em script**: um retângulo extrudado leva cerca de 20 linhas, contra 1 linha de `makeBox`. Cada linha do sketch precisa de restrições `Coincident` explícitas entre os pontos (índices de geometria e de vértice: 1 = início, 2 = fim). A anexação muda de nome entre versões (`AttachmentSupport` no 1.x, `Support` no 0.21), e o resultado só existe depois de `doc.recompute()`. Problemas de topological naming aparecem quando se referencia face/aresta por nome (`Face6`). Testado e funcionando headless:

```python
import Sketcher
doc = App.newDocument("PD")
sheet = doc.addObject("Spreadsheet::Sheet", "Params")
sheet.set("B1", "40"); sheet.setAlias("B1", "largura")
sheet.set("B2", "8");  sheet.setAlias("B2", "altura")
body = doc.addObject("PartDesign::Body", "Body")
sk = body.newObject("Sketcher::SketchObject", "Sketch")
sk.AttachmentSupport = (doc.getObject("XY_Plane"), [""])
sk.MapMode = "FlatFace"
p = [V(0, 0, 0), V(40, 0, 0), V(40, 20, 0), V(0, 20, 0)]
for i in range(4):
    sk.addGeometry(Part.LineSegment(p[i], p[(i + 1) % 4]), False)
for i in range(4):
    sk.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 4, 1))
sk.addConstraint(Sketcher.Constraint("Horizontal", 0)); sk.addConstraint(Sketcher.Constraint("Horizontal", 2))
sk.addConstraint(Sketcher.Constraint("Vertical", 1));   sk.addConstraint(Sketcher.Constraint("Vertical", 3))
sk.addConstraint(Sketcher.Constraint("Coincident", 0, 1, -1, 1))       # -1 = eixos do sketch (origem)
ci = sk.addConstraint(Sketcher.Constraint("DistanceX", 0, 1, 0, 2, 40))
sk.addConstraint(Sketcher.Constraint("DistanceY", 1, 1, 1, 2, 20))
sk.setExpression(f"Constraints[{ci}]", "Params.largura")              # cota vinda da planilha
pad = body.newObject("PartDesign::Pad", "Pad")
pad.Profile = sk
pad.setExpression("Length", "Params.altura")
doc.recompute()                       # body.Shape.Volume == 6400
sheet.set("B1", "50"); doc.recompute()  # -> 8000: parâmetro propagou
```

Meio-termo útil: gerar com Part/CSG e, se precisar de parâmetros editáveis na GUI, salvar uma `Spreadsheet::Sheet` com os valores usados dentro do `.FCStd`. Com isso o arquivo documenta as medidas, mesmo que a geometria seja um `Part::Feature` estático.

---

## 6. Pegadinhas encontradas nos testes

1. `freecadcmd script.py` sai com **exit code 0 mesmo com exceção**, e o script **roda duas vezes** quando lança exceção. Use `p3d gerar`.

2. `__name__` não é `"__main__"` no `freecadcmd script.py`. Pelo `p3d gerar` é.

3. Argumentos com `-`/`--` quebram o `freecadcmd` (`unrecognised option`, exit 1), e argumentos que são arquivos existentes ele tenta abrir. Use `p3d gerar`, ou `--pass ARG` antes de cada um.

4. stdout em ASCII com `LC_CTYPE=C`: `print` com acento lança `UnicodeEncodeError`. O wrapper resolve.

5. A saída C++ (barra de progresso de `saveAs`/`recompute`, estatísticas do STEP, checagens da `Mesh`) vai direto no fd 1 e fica intercalada com os `print` do Python. Use `pecas3d.silencio()`.

6. Booleanas (`cut`/`fuse`/`common`) devolvem **`Compound`**, não `Solid`. Use `.Solids[0]` ou `pecas3d.solido_unico()`.

7. `Part.Face([wire_externo, wire_interno])` **não faz furo** e devolve uma face inválida com área somada. Use `Part.makeFace([...], "Part::FaceMakerBullseye")`.

8. `shape.exportStl()` não tem controle de tessellation. Use `MeshPart.meshFromShape(...)` + `mesh.write()`.

9. `AngularDeflection` é em **radianos**. `rotate`/`revolve`/`Rotation(eixo, ang)` são em **graus**.

10. `makeCylinder`/`makeCone`/`makeCircle` recebem **raio**.

11. Depois de `makeFillet`/`makeChamfer`/`cut`, os índices de arestas e faces mudam. Selecione sempre por geometria no shape novo, nunca por índice fixo (`Edge5`).

12. Na primeira execução após instalar, o Gatekeeper atrasa cerca de 7 s. Depois roda em menos de 1 s.

13. O aviso `Failed to open library ... 3DconnexionNavlib` aparece em toda execução e é inofensivo.

14. `freecadcmd -c "..."` serve para one-liners e devolve exit 1 em exceção, mas tem o mesmo problema de stdout em ASCII. Para mais de uma linha, prefira um arquivo + `p3d gerar`.

15. `doc.saveAs(caminho)` sobre um `.FCStd` existente cria um backup `<nome>.<data>.FCBak` ao lado. `arvore.salvar` e `pecas3d.exportar` apagam o `.FCStd` antes de salvar para evitar isso.

16. A wiki oficial (wiki.freecad.org) está atrás de uma checagem anti-bot (Anubis), que bloqueia fetch automatizado. Para ler por script, use o espelho oficial em markdown no GitHub (`FreeCAD/FreeCAD-documentation`, pasta `wiki/`). A última atualização dele é de jan/2025, com conteúdo da era 1.0, então confirme assinaturas com `print(func.__doc__)` no 1.1.

---

## 7. Links oficiais

- Python scripting tutorial: https://wiki.freecad.org/Python_scripting_tutorial
- FreeCAD Scripting Basics: https://wiki.freecad.org/FreeCAD_Scripting_Basics
- Topological data scripting (Part): https://wiki.freecad.org/Topological_data_scripting
- Part scripting: https://wiki.freecad.org/Part_scripting
- Part API: https://wiki.freecad.org/Part_API
- Sketcher scripting: https://wiki.freecad.org/Sketcher_scripting
- PartDesign Body: https://wiki.freecad.org/PartDesign_Body
- Mesh scripting: https://wiki.freecad.org/Mesh_Scripting
- Mesh from Part shape (MeshPart, LinearDeflection/AngularDeflection): https://wiki.freecad.org/Mesh_FromPartShape
- Import/Export: https://wiki.freecad.org/Import_Export
- Headless FreeCAD: https://wiki.freecad.org/Headless_FreeCAD
- Start up and Configuration (opções de linha de comando, `--pass`): https://wiki.freecad.org/Start_up_and_Configuration
- Embedding FreeCAD: https://wiki.freecad.org/Embedding_FreeCAD
- Expressions: https://wiki.freecad.org/Expressions
- Spreadsheet: https://wiki.freecad.org/Spreadsheet_Workbench
- Espelho em markdown da wiki: https://github.com/FreeCAD/FreeCAD-documentation/tree/main/wiki
- Código-fonte: https://github.com/FreeCAD/FreeCAD

---

## 8. Modo árvore (PartDesign) por script: pegadinhas testadas em 23/11/2026

Ajudantes em `lib/arvore.py`, testes em `tests/test_arvore.py`.

1. **Alias da planilha não pode ser nome de unidade** (`h`, `w`, `r`, `m`, `s`, `g`...): `setAlias` lança `ValueError: Invalid alias`.
2. **Plano XZ do corpo**: x local = X global, y local = Z global, normal = -Y. O `AttachmentOffset.Base.z` de um esboço no XZ vale **-Y** global.
3. **Avaliar uma expressão da planilha no script**: `doc.getObject("Medidas").evalExpression("Medidas.x * 2")` devolve Quantity (`.Value` em mm).
4. **Grau de liberdade do esboço**: depois de `recompute`, `sk.solve() == 0 and sk.DoF == 0`. Não existe `getDoF()` no 1.1.
5. **Revolution e Groove** pegam o eixo do próprio esboço: `feat.ReferenceAxis = (sk, ["V_Axis"])`.
6. **Corpo do PartDesign mostra só a feature da ponta (Tip)**. Num arquivo feito sem tela, a ponta pode abrir escondida; o `lib/aparencia.py` liga a ponta e desliga o resto.
7. **Abrir com janela no macOS**: `open -n -a FreeCAD --args arquivo.FCStd script.py`. Chamar `Contents/MacOS/FreeCAD` direto abre, mas o macOS não registra como app. Sem `-n`, com o FreeCAD já aberto, os argumentos são ignorados.
8. **A página Iniciar abre por cima do documento** depois que o script de abertura roda. Trazer a vista para a frente com `QTimer.singleShot` (1,5 s e 4 s).
9. **Texto (Draft ShapeString) gravado**: as curvas B-spline da fonte deram auto-interseção no STL em algumas tessellations. No modo árvore com `Part::Cut` da extrusão passou; no modo Part, trocar as curvas por polígono (`wire.discretize(Deflection=0.02)`).
10. **Valor negativo na planilha precisa de "="** (`"=-30 mm"`); sem ele vira texto. O `arvore.planilha` põe o "=" sozinho.
11. **Elipse no Sketcher**: depois de `sk.exposeInternalGeometry(e)`, o índice `e + 1` é o eixo maior e `e + 2` o menor (para as restrições de medida).
12. **Pocket corta no sentido contrário à normal do esboço**; usar `Reversed = True` quando precisar do outro lado.
13. **Medida de BSpline ou loft**: usar `shape.optimalBoundingBox()`; o `BoundBox` é folgado.
14. **FreeCAD parado sem janela com CPU em 0** no macOS: `sample <pid>` mostra a thread presa em `open()` dentro de `Document::restore`. É o pedido de acesso à pasta (Documentos, Mesa...), e quem libera é o usuário em Ajustes, Privacidade e Segurança, Arquivos e Pastas.
15. **Engrenagem evolvente (`InvoluteGearFeature`) funciona sem tela**: `Part::Part2DObjectPython` + `_InvoluteGear(obj)`, dentro do corpo, com `AttachmentSupport` no plano XY e Pad. `NumberOfTeeth`, `Modules`, `PressureAngle` e `ProfileShiftCoefficient` aceitam expressão da planilha. Mas o `check(True)` aborta (`BOPAlgo OperationAborted`) em qualquer sólido feito com esse perfil, até numa extrusão pura dele: validar com `isValid`, `check(False)` e o STL sem auto-interseção. Exemplo em `exemplos/engrenagem-registro/peca.py`.
