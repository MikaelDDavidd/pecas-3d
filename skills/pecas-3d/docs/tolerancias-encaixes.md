# Tolerâncias e encaixes em FDM

Folgas para peças que se encaixam, deslizam, giram, travam (snap-fit) ou são impressas já montadas (print-in-place).
Bico 0,4 mm, camada 0,2 mm, impressora calibrada (Prusa/Bambu classe MK4/X1/P1).

**Nenhuma fonte séria dá um valor universal.** A Prusa diz explicitamente que não existe valor único: depende de tamanho, orientação, geometria, calibração, fatiador e material ([Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)). Os valores abaixo são o **ponto de partida do projeto**; toda peça com encaixe crítico deve ser precedida de uma **peça de teste de tolerância** (ver seção 9).

---

## 0. Convenção do projeto (ler antes de usar qualquer número)

Metade da confusão nas fontes é "folga por lado" versus "folga total". Neste projeto:

| Termo | Significado | Exemplo |
|---|---|---|
| **Folga diametral** (Ø) | diferença entre o diâmetro do furo e o diâmetro do eixo | eixo 8,0 + folga diametral 0,4 → furo 8,4 |
| **Folga por lado** (radial) | distância entre as superfícies de um lado | folga por lado 0,2 = folga diametral 0,4 |
| Encaixe prismático (caixa/tampa, macho-fêmea retangular) | sempre **por lado** | lingueta 5,0 de largura, folga 0,2 por lado → rasgo 5,4 |

No código FreeCAD, nomear variáveis explicitamente: `folga_diametral`, `folga_por_lado`.

---

## 1. Tabela-mestre de folgas (padrão do projeto)

| Tipo de encaixe | Folga **diametral** adotada | Por lado | Faixa nas fontes | Fontes |
|---|---|---|---|---|
| **Press-fit** (interferência, não sai à mão) | **0,0 mm** (nominal) a −0,1 mm | 0 a −0,05 | nominal = press-fit; −0,1 em furo grande | [MakerWorld Tolerance & Fit Test](https://makerworld.com/en/models/2820462-tolerance-fit-test) |
| **Justo** (montagem à mão, sem jogo perceptível; desmontável) | **0,2 mm** | 0,1 | 0,1–0,2 | [Fictiv](https://www.fictiv.com/articles/how-to-design-snap-fit-components) (0,2 "tight fit"), [Prusa forum](https://forum.prusa3d.com/forum/english-forum-general-discussion-announcements-and-releases/need-advice-on-design-tolerances/), [MakerWorld](https://makerworld.com/en/models/2820462-tolerance-fit-test) |
| **Deslizante** (desliza/gira livre, com pouco jogo) | **0,4 mm** | 0,2 | 0,2–0,5 | [Fictiv](https://www.fictiv.com/articles/how-to-design-snap-fit-components) (0,4 "slide fits and pivot joints"), [Xometry](https://xometry.pro/en/?p=22061) (0,2–0,3), [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) (>= 0,3 móvel) |
| **Folgado** (montagem cega, alinhamento grosso) | **0,6 mm** | 0,3 | 0,5–0,6 | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) (0,5 conexão/móvel), [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) (0,5 FDM) |
| **Print-in-place** (impresso montado) | **0,6 mm** | **0,3** em XY; Z >= 0,3 mm | 0,25–0,4 por lado | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) (>= 0,3), [Prusa forum](https://forum.prusa3d.com/forum/english-forum-general-discussion-announcements-and-releases/need-advice-on-design-tolerances/) (~0,25) |
| **Objeto embutido com pausa** (porca, ímã, peso) | 0,3 mm | **0,15 em todas as direções** | - | [Prusa Blog](https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/) |

Notas:
- As faixas misturam convenções nas fontes originais (algumas dizem "gap", sem dizer se é por lado). A tabela acima já está convertida para a convenção do projeto e arredondada para o lado seguro.
- PETG costuma pedir ~0,1 mm a mais que PLA em encaixes (escorre mais, "gruda"); ABS/ASA contraem mais.
- **Encaixes grandes** (área de contato grande, perímetro > ~100 mm) pedem +0,1 mm por lado: o erro absoluto cresce com o tamanho ([Hubs](https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/)).
- Encaixe com eixo **horizontal** (furo deitado): somar ~1 altura de camada (0,2 mm) na direção Z, porque o topo do furo flecha.

---

## 2. Furos saem menores: compensação

Furo vertical impresso sai **menor** que o CAD; eixo/pino impresso sai do tamanho ou levemente maior.

| Causa | Efeito |
|---|---|
| Extrusão comprime e "puxa" para dentro em curvas fechadas | furo pequeno perde mais (proporcionalmente) |
| Tesselação do STL (polígono inscrito no círculo) | furo vira polígono menor que o círculo |
| Elephant foot | primeira camada do furo mais fechada |

Fontes: "Printed holes usually come out smaller than in CAD" ([CNC Kitchen](https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey)); recomendação de imprimir menor e furar se precisão for crítica ([Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/)); furos menores encolhem proporcionalmente mais ([MakerWorld Tolerance & Fit Test](https://makerworld.com/en/models/2820462-tolerance-fit-test)).

**Três formas de compensar (escolher UMA, nunca somar sem medir):**

| Método | Como | Quando usar |
|---|---|---|
| A. No CAD (padrão do projeto) | somar **+0,1 a +0,2 mm** no diâmetro de furos verticais de 2–10 mm, **além** da folga do encaixe | peça vai ser fatiada por qualquer pessoa/fatiador |
| B. No fatiador | **X-Y hole compensation** (Orca/Bambu), **Hole Horizontal Expansion** (Cura). Prusa: ver fatiamento.md | impressora/material calibrados, perfil fixo |
| C. Pós-processo | imprimir 0,2–0,3 mm menor e passar broca/alargador | furo de precisão (rolamento, eixo de metal) |

Calibração do fatiador (método do teste X-Y): medir desvio e dividir por 2 para obter o valor de compensação por lado (ex.: alvo 100 mm, medido 99,86 mm → 0,07 mm) ([OrcaSlicer wiki: Precision](https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_precision.html), [MakerWorld X-Y-Compensation Tool](https://makerworld.com/en/models/129893-x-y-compensation-tool)).

**Padrão do projeto:** método A com **+0,15 mm** no diâmetro de furos verticais de 2–10 mm; furos > 10 mm, +0,1 mm. Exportar com tesselação fina.

---

## 3. Press-fit

| Situação | Furo no CAD | Observação |
|---|---|---|
| Pino impresso em furo impresso (vertical) | furo = pino (nominal) | o furo já sai menor → interferência real de ~0,1–0,2 mm |
| Pino metálico (eixo, pino-guia) em furo impresso | furo = pino − 0,0 a 0,1 mm | testar; PLA racha se apertado demais |
| Rolamento (ex.: 608, Ø22) em alojamento impresso | Ø nominal + 0,0 a +0,1 | furo grande encolhe menos; testar com 3 diâmetros |
| Press-fit regulável | **crush ribs**: 3–6 nervuras de ~0,4–0,6 mm de largura que interferem 0,2–0,3 mm; furo base com folga de 0,2 | nervuras deformam em vez de rachar a parede. Dimensões das nervuras são adotadas pelo projeto (não confirmadas em fonte); calibrar com um modelo de teste como o [Printables "Crush Ribs"](https://prusaprinters.org/prints/43636-test-print-crush-ribs-version04) |

Regras:
- Parede em volta de press-fit: >= 1,6 mm (4 linhas) para não rachar entre camadas.
- Chanfro de entrada 0,5 mm x 45° no furo (guia o pino) e no pino.
- Press-fit com eixo do furo em Z: a pressão abre as camadas no plano: mais resistente que furo horizontal, onde a pressão tenta separar camadas.

---

## 4. Print-in-place (peças impressas montadas)

| Parâmetro | Valor adotado | Fonte |
|---|---|---|
| Folga por lado em XY | **0,3 mm** (mínimo testado 0,25; agressivo 0,2 em impressora muito calibrada) | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135), [Prusa forum](https://forum.prusa3d.com/forum/english-forum-general-discussion-announcements-and-releases/need-advice-on-design-tolerances/), [MakerWorld hinge](https://makerworld.com/en/models/726457) (0,2 em X1C) |
| Folga em Z (entre partes sobrepostas) | **>= 0,3 mm** (1,5 camada a 0,2 mm); preferir 0,4 | adotado: com 1 camada só, a parte de cima apoia na de baixo e funde |
| Superfícies de cima de folgas Z | não podem ser "teto" grande: usar cone/chanfro 45° | overhang (design-fdm.md) |

Dicas:
- Eixo de giro de dobradiça print-in-place **horizontal**, com o pino em forma de cone duplo (45°) dentro de alojamento cônico: imprime sem suporte (ver seção 6).
- PETG funde mais facilmente que PLA em folgas pequenas; usar 0,35–0,4 mm por lado.
- Depois de imprimir, "quebrar" o movimento com força moderada; uma película fina de elephant foot costuma prender a primeira camada → evitar folgas que começam na camada 1 (subir a peça móvel 0,2–0,4 mm ou chanfrar a base).

---

## 5. Snap-fit (cantilever)

### 5.1 Fórmulas (viga em balanço, seção retangular)

Do guia clássico da Bayer ("Snap-Fit Joints for Plastics: A Design Guide", Tabela 1): [PDF](https://fab.cba.mit.edu/classes/S62.12/people/vernelle.noel/Plastic_Snap_fit_design.pdf):

| Geometria | Deflexão admissível (= undercut) |
|---|---|
| Espessura constante | **y = 0,67 · ε · l² / h** |
| Espessura afinando linearmente até h/2 na ponta | **y = 1,09 · ε · l² / h** (permite >60% mais deflexão) |

| Força de deflexão | **P = b · h² · Es · ε / (6 · l)** |
|---|---|

Símbolos: y = deflexão (= profundidade do gancho/undercut); ε = deformação admissível na raiz (fração, 2% = 0,02); l = comprimento do braço; h = espessura na raiz; b = largura na raiz; Es = módulo secante do material.

Força de montagem (ao longo do eixo de inserção), com ângulo de entrada α e atrito μ ([Machine Design / BASF](https://www.machinedesign.com/archive/new-equations-make-fastening-plastic-components-snap)):
**W = P · (μ + tan α) / (1 − μ · tan α)**

Isolando para dimensionar (espessura constante): **ε = 1,5 · y · h / l²**.

### 5.2 Deformação admissível (ε)

Valores de **injeção** (Bayer, montagem única, 23 °C): [Bayer guide, Tabela 2](https://fab.cba.mit.edu/classes/S62.12/people/vernelle.noel/Plastic_Snap_fit_design.pdf):

| Material (injetado) | ε admissível |
|---|---|
| PC (Makrolon) | 4% |
| PC alta temperatura (Apec) | 4% |
| Blendas de PC (Makroblend) | 3,5% |
| PC/ABS (Bayblend) | 2,5% |
| PC 10% fibra de vidro | 2,2% |
| PC 20% fibra de vidro | 2,0% |

Regras da Bayer: materiais amorfos até ~70% da deformação de escoamento; semicristalinos quase até o escoamento; reforçados com fibra, ~metade do alongamento na ruptura. **Montagem/desmontagem frequente: usar ~60% desses valores.**

Para impressão 3D, a Fictiv publica "acceptable strain": PLA 4–8%, ABS 7%, Nylon 4–15% ([Fictiv](https://www.fictiv.com/articles/how-to-design-snap-fit-components)): valores otimistas, parecem baseados no material bruto. Para braço impresso em Z, reduzir a deformação admissível em **50%** ([Core77/Fictiv](https://www.core77.com/posts/65318/how-to-design-snap-fit-components)).

**Valores de projeto adotados (FDM, braço no plano XY, montagem repetida): CONSERVADORES, NÃO VÊM DE FONTE, CALIBRAR:**

| Material | ε de projeto | Comentário |
|---|---|---|
| PLA | **1,5%** | frágil; a Hubs considera PLA "less suitable" para snap-fit ([Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/)) |
| PETG | **2,0%** | tenaz, bom para clipes |
| ABS / ASA | **2,0%** | |
| PC | **2,5%** | 60% dos 4% da Bayer |
| PA (nylon) | **3,0%** | melhor material para clipe; recomendado pela Hubs junto com ABS e TPU |
| Braço impresso em Z | **metade** do valor acima | evitar sempre |

### 5.3 Dimensões e regras

| Regra | Valor | Fonte |
|---|---|---|
| Espessura mínima na raiz | 1,0 mm (projeto: >= 1,2 mm = 3 linhas) | [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) |
| Largura mínima | 5 mm | [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) |
| Filete na raiz | >= 0,5 x espessura da raiz | [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) |
| Folga nominal nas partes que se encaixam | 0,5 mm (FDM) | [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) |
| Afunilar o braço (espessura cai até a ponta) | reduz tensão na raiz | [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/), Bayer |
| Ângulo de entrada | 30° (montagem fácil) | prática da indústria; ângulo de retenção 90° = não desmonta, 45° = desmontável |
| Orientação | braço no plano XY, nunca em Z | [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) |
| Em serviço | braço sem carga (só flexiona na montagem) | [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) |

### 5.4 Exemplo de cálculo

PETG, ε = 0,02, braço de l = 15 mm, h = 1,5 mm, espessura constante:
y = 0,67 · 0,02 · 15² / 1,5 = **2,0 mm** de undercut máximo. Adotar gancho de 1,2–1,5 mm (margem).

PLA, ε = 0,015, mesmo braço: y = 0,67 · 0,015 · 225 / 1,5 = **1,5 mm** → gancho de 0,8–1,0 mm.

Se o undercut necessário não cabe: aumentar l (o efeito é quadrático), reduzir h ou afunilar o braço (fator 1,09 em vez de 0,67).

---

## 6. Dobradiças

| Tipo | Material | Regras |
|---|---|---|
| **Pino separado** (pino de metal ou filamento de 1,75 mm como eixo) | qualquer | furo do pino com folga diametral 0,2–0,3 (pino gira) ou press-fit numa das partes; parede em volta >= 1,6 mm |
| **Print-in-place com cone** | PLA, PETG | pino cônico 45° em alojamento cônico; folga 0,3 mm por lado ([Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)); eixo da dobradiça horizontal, paralelo à mesa |
| **Dobradiça viva (living hinge)** | **PP, PA, TPU**: não PLA | lâmina fina (0,3–0,6 mm, 1–2 camadas de altura) impressa na mesa; PLA rompe em poucos ciclos. Valores de lâmina são prática comum, não confirmados em fonte primária |
| Dobradiça de pino impresso em Z | - | evitar: pino quebra na linha de camada |

Dobradiça que deve **ficar parada** em posição (tampa, braço articulado): folga menor (0,15–0,2 por lado) ou adicionar atrito (anel de TPU, mola). Dobradiça de tampa de caixa: folgada para fechar livre ([MakerWorld hinge test](https://makerworld.com/en/models/726457)).

---

## 7. Encaixe macho-fêmea (prismático, cauda de andorinha, tampa)

| Situação | Folga por lado adotada |
|---|---|
| Tampa de caixa que encaixa justa (sem clipe) | 0,1–0,15 |
| Tampa deslizante (trilho) | 0,2–0,25 |
| Cauda de andorinha (dovetail) para unir peças grandes | 0,1–0,15 (fixa) / 0,2 (desmontável) |
| Pino-guia de alinhamento | 0,1 por lado |

Regras:
- Imprimir **as duas partes na mesma orientação** e com a superfície de encaixe vertical (perpendicular à mesa) ([Xometry](https://xometry.pro/en/?p=22061)).
- Chanfrar 0,5 mm x 45° a entrada da fêmea e a ponta do macho.
- Cauda de andorinha: ângulo de flanco 10–15° quando o encaixe é por deslizamento em Z; se o rasgo fica "deitado", conferir overhang.
- A face de baixo da fêmea sofre elephant foot: chanfro na base (design-fdm.md, seção 7).

---

## 8. Roscas: impressa x inserto

| Opção | Quando | Regras | Fonte |
|---|---|---|---|
| **Rosca impressa** | rosca grande, poucos ciclos, tampa de pote, ajuste | **não usar abaixo de M5**; projeto adota >= M6 / passo >= 1,0 mm; eixo da rosca em Z; folga radial 0,2–0,3 mm no perfil; perfil trapezoidal/redondo imprime melhor que 60° fino | [Hubs](https://www.hubs.com/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners/) |
| **Parafuso direto no plástico** (autoatarraxante/rosca formada) | montagem permanente, poucos ciclos | furo piloto ~0,8 x d (ver fixacao.md) | [EJOT via Bossard](https://media.bossard.com/-/media/bossard-group/website/documents/brochures/brochures_products_english/delta-pt_en.pdf) |
| **Inserto térmico (heat-set)** | **padrão do projeto** para qualquer rosca <= M5 que vai ser apertada mais de 2–3 vezes ou levar torque | tabela em fixacao.md | [CNC Kitchen](https://cnckitchen.store/products/heat-set-insert-m3-x-5-7-100-pieces), [Ruthex](https://www.ruthex.de/en/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen) |
| **Porca embutida** (nut trap) | maior força de arrancamento, montagem rara | alojamento sextavado (fixacao.md) | |
| **Macho de rosca (tap)** em furo impresso | rosca pequena eventual | furo = broca de macho padrão (M3: 2,5 mm); parede >= d | [Hubs](https://www.hubs.com/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners/) |

Parede em volta de qualquer furo roscado: **>= diâmetro do parafuso** (ex.: M5 → 5 mm) ([Hubs](https://www.hubs.com/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners/)).

Rosca impressa no FreeCAD: preferir perfil gerado (Part Helix + sweep) com a folga já aplicada no perfil fêmea; o workbench Fasteners também gera roscas modeladas.

---

## 9. Peça de teste de tolerância (obrigatória para encaixe crítico)

Antes da peça final, imprimir uma barra com:
- Furos verticais de Ø 3, 5, 8 e 10 mm, cada um em 4 versões: nominal, +0,1, +0,2, +0,3.
- Pinos correspondentes no nominal (testar press-fit, justo, deslizante).
- Um rasgo prismático de 5 mm com folgas 0,1 / 0,15 / 0,2 / 0,25 por lado.
- Um furo horizontal Ø 8 redondo e em gota.

Mesmo material, mesmo perfil de fatiamento, mesma orientação da peça final. Anotar o resultado no documento do projeto da peça e ajustar a constante de folga.

Modelos prontos de referência: [MakerWorld Tolerance & Fit Test](https://makerworld.com/en/models/2820462-tolerance-fit-test) (furos de +0,10 a +0,60 mm), [Printables Threaded Insert Hole Tolerance Test](https://printables.com/model/1040630-threaded-insert-hole-tolerance-test).
