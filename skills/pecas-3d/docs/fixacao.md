# Fixação: parafusos, porcas, insertos térmicos e ímãs

Tabelas para projetar furos e alojamentos de fixadores métricos M2 a M5 em peças FDM (bico 0,4 mm).
Dimensões de fixadores vêm das normas ISO (reproduzidas em fasten.it e tabelas de fornecedores: conferir na norma oficial antes de desenho de produção). Folgas de impressão são **padrão do projeto** e devem ser calibradas com peça de teste.

Convenção: todas as folgas de furo abaixo são **diametrais** (ver [tolerancias-encaixes.md](tolerancias-encaixes.md), seção 0).

---

## 0. Cola rápida (padrão do projeto)

| | M2 | M2.5 | M3 | M4 | M5 |
|---|---|---|---|---|---|
| Furo passante (CAD, vertical) | 2,4 | 2,9 | **3,4** | 4,5 | 5,5 |
| Furo passante folgado / horizontal | 2,6 | 3,1 | 3,6 | 4,8 | 5,8 |
| Furo para parafuso direto no plástico | 1,7 | 2,1 | **2,5** | 3,4 | 4,2 |
| Nut trap: entre faces (CAD) | 4,3 | 5,3 | **5,8** | 7,3 | 8,3 |
| Nut trap: profundidade (CAD) | 1,9 | 2,3 | 2,7 | 3,5 | 5,0 |
| Cabeça cilíndrica ISO 4762: Ø alojamento | 4,4 | 5,1 | **6,1** | 7,6 | 9,1 |
| Cabeça cilíndrica: profundidade alojamento | 2,2 | 2,7 | 3,2 | 4,2 | 5,2 |
| Inserto térmico (CNC Kitchen/Ruthex): Ø furo | 3,2 | 4,0 | **4,0** | 5,6–5,7 | 6,4–6,5 |
| Inserto: profundidade do furo cego | L+1 | L+1 | L+1 | L+1 | L+1 |
| Inserto: parede mínima em volta | 1,3 | 1,6 | 1,6 | 2,1 | 2,6 |

Detalhes, fontes e quando fugir do padrão nas seções abaixo.

---

## 1. Furo passante (clearance hole)

Norma de referência: **ISO 273** (séries fina, média e grossa). Valores via [Optimas tapping sizes](https://optimas.com/technical-resources/tapping-sizes/) e [AMES clearance chart](https://amesweb.info/Screws/Metric-Clearance-Hole-Chart.aspx) (mesmos números da ISO 273; a norma em si é paga):

| Rosca | Fina (close, H12) | Média (normal, H13) | Grossa (free, H14) |
|---|---|---|---|
| M2 | 2,2 | 2,4 | 2,6 |
| M2.5 | 2,7 | 2,9 | 3,1 |
| M3 | 3,2 | 3,4 | 3,6 |
| M4 | 4,3 | 4,5 | 4,8 |
| M5 | 5,3 | 5,5 | 5,8 |

Mapeamento fina/média/grossa = H12/H13/H14 segundo [Albany County Fasteners](https://www.albanycountyfasteners.com/media/6b/b8/g0/1764944339/clearance-hole-chart.pdf).

**Padrão do projeto para impressão:**
- Furo **vertical** com impressora calibrada: série **média** (M3 = 3,4). O furo impresso sai ~0,1–0,2 menor, ficando próximo da série fina, o que ainda passa o parafuso.
- Furo **horizontal**, impressora não calibrada, ou alinhamento entre várias peças: série **grossa** (M3 = 3,6).
- Furo de **posicionamento preciso**: imprimir na série fina e passar broca.

---

## 2. Parafuso direto no plástico (autoatarraxante / rosca formada)

Referência industrial: parafusos para termoplásticos tipo **EJOT DELTA PT**: furo piloto **dh = 0,8 x d1** (d1 = diâmetro nominal); até **0,88 x d1** para materiais mais carregados/resistentes ([EJOT DELTA PT Flyer](https://www.ejot.de/medias/sys_master/Industry_Flyer/Industry_Flyer/h11/hc7/9331662782494/EJOT-DELTA-PT-Flyer-08.23-en.pdf)). Boss com diâmetro externo de ~2 x d1, engajamento ~2 x d1, alívio de borda d1 + 0,2 mm ([Bossard DELTA PT](https://media.bossard.com/-/media/bossard-group/website/documents/brochures/brochures_products_english/delta-pt_en.pdf); a notação do "d" do diâmetro externo é ambígua na fonte resumida: ver lacunas).

| Rosca / parafuso | 0,8 x d | 0,88 x d | **Adotado no CAD (impresso)** |
|---|---|---|---|
| M2 / 2,2 mm | 1,6 | 1,76 | 1,7 |
| M2.5 | 2,0 | 2,2 | 2,1 |
| M3 / 3,0 mm | 2,4 | 2,64 | **2,5** |
| M4 | 3,2 | 3,52 | 3,4 |
| M5 | 4,0 | 4,4 | 4,2 |

Adotado = ~0,84 x d: o furo impresso encolhe um pouco, e o plástico impresso (com camadas) racha mais fácil que o injetado; parafuso de máquina métrico (não PT) também entra nesses valores com bastante esforço.

Regras:
- Parede em volta do furo >= **diâmetro do parafuso** ([Hubs](https://www.hubs.com/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners/)); projeto: boss externo >= 2,5 x d.
- Profundidade de engajamento >= 2 x d; furo cego com +2 mm de fundo para cavaco.
- Eixo do furo em Z (as camadas seguram a rosca formada; furo horizontal tende a abrir entre camadas).
- Paredes do boss com >= 3–4 perímetros (a rosca é formada nos perímetros, não no infill).
- Uso: montagem permanente ou poucas vezes. Para montar/desmontar sempre → **inserto térmico**.

Dados de resistência (secundários): nos testes do CNC Kitchen com M3, o arrancamento (pull-out) foi parecido entre parafuso direto, inserto térmico e Helicoil (~120 kg); o inserto ganhou em torque de arranque (~3 N·m) ([resumo em Embedded Computing](https://www.embedded-computing.com/home-page/3d-printed-fasteners-part-1-inserts)).

---

## 3. Porca sextavada embutida (nut trap)

Dimensões da porca **ISO 4032** (style 1): [fasten.it ISO 4032](https://fasten.it/norms/norm/din_en_iso_4032):

| Rosca | s (entre faces) | e mín (entre cantos) | m máx (altura) |
|---|---|---|---|
| M2 | 4,0 | 4,32 | 1,6 |
| M2.5 | 5,0 | 5,45 | 2,0 |
| M3 | 5,5 | 6,01 | 2,4 |
| M4 | 7,0 | 7,66 | 3,2 |
| M5 | 8,0 | 8,79 | 4,7 |

**Alojamento no CAD:**
- Entre faces = **s + 0,3 mm** (0,15 por lado: mesmo valor que a Prusa recomenda para objetos embutidos: "0,15mm in all directions", [Prusa Blog](https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/)).
- Profundidade = **m + 0,3 mm** (porca entrando por cima/lateral) ou m + 0,15 se embutida com pausa.
- Desenhar o hexágono pelo **entre faces** (s), não pelo diâmetro do círculo circunscrito. No FreeCAD: polígono regular de 6 lados com raio circunscrito **R = (s + 0,3) / √3** (equivalente a (s + 0,3) / (2 · cos 30°)). Ex.: M3 → R = 5,8 / 1,732 = 3,35 mm.
- Orientar o hexágono com **duas faces paralelas ao eixo X** ou com um vértice para cima conforme a direção de inserção; se o alojamento é lateral (porca entra de lado, "slot"), o rasgo tem largura = s + 0,3.

| Variante | Quando |
|---|---|
| Porca entra pela face de cima, presa por pressão | montagem fácil; folga 0,2–0,3 em s; prende o giro, não prende contra puxar para cima |
| Porca em rasgo lateral (slot) | porca não cai; parafuso entra de baixo |
| Porca embutida com **pausa** (M601 / "Insert pause" no fatiador) | máxima resistência; folga 0,15 em todas as direções; cobrir com 2–3 camadas para esconder ([Prusa Blog](https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/), [Prusa KB pause](https://help.prusa3d.com/article/insert-pause-or-custom-g-code-at-layer_120490)) |
| Alojamento virado para a mesa (de cabeça para baixo) | usar **camada de sacrifício** de 0,2 mm sobre o hexágono, ou ponte em degraus; furar depois |

Atenção ao pausar: há relato de que a pausa entra uma camada depois da escolhida; conferir no preview que a cavidade ainda está aberta ([comentários no Prusa KB](https://help.prusa3d.com/article/insert-pause-or-custom-g-code-at-layer_120490)).

---

## 4. Alojamento de cabeça (counterbore e countersink)

### 4.1 Cabeça cilíndrica: ISO 4762 (allen, socket head cap screw)

Dimensões: [fasten.it ISO 4762](https://fasten.it/norms/norm/din_en_iso_4762), conferido com catálogo Würth (M4: dk 7, k 4):

| Rosca | dk máx (Ø cabeça) | k máx (altura) | **Ø alojamento (dk + 0,6)** | **Profundidade (k + 0,2)** |
|---|---|---|---|---|
| M2 | 3,8 | 2,0 | 4,4 | 2,2 |
| M2.5 | 4,5 | 2,5 | 5,1 | 2,7 |
| M3 | 5,5 | 3,0 | 6,1 | 3,2 |
| M4 | 7,0 | 4,0 | 7,6 | 4,2 |
| M5 | 8,5 | 5,0 | 9,1 | 5,2 |

Folga de +0,6 diametral: deixa passar a ferramenta e absorve erro de impressão. Para cabeça embutida rente à superfície, somar a altura desejada abaixo da face.

Alojamento com o furo para cima (cabeça entra por cima): sem problema. Alojamento virado para a mesa: o "teto" entre o Ø do alojamento e o Ø do furo passante é overhang de 90° → usar **camada de sacrifício** (membrana de 1 camada no fundo do alojamento, furada depois) ou **ponte em dois degraus** (primeiro uma ponte retangular da largura do furo, depois outra cruzada).

### 4.2 Cabeça escareada (countersunk, 90°)

| Rosca | ISO 10642 (allen) dk teórico máx | ISO 7046 (Phillips) dk máx | ISO 7046 k máx |
|---|---|---|---|
| M2 | - (ISO 10642 começa em M3) | 3,8 | 1,2 |
| M2.5 | - | 4,7 | 1,5 |
| M3 | 6,72 | 5,5 | 1,65 |
| M4 | 8,96 | 8,40 | 2,7 |
| M5 | 11,20 | 9,30 | 2,7 |

Fontes: [Engineers Edge ISO 10642](https://engineersedge.com/hardware/bs_en_iso_10642_14583.htm), [fasten.it ISO 7046-2](https://fasten.it/Norms/Norm/DIN_EN_ISO_7046_2). Ângulo 90° (+2/−0°) segundo [Accu, ISO 10642](https://accu.co.uk/countersunk-socket-head-screws/5421-SSK-M3-5-A2).

**Escareado no CAD:** cone de 90° com Ø de topo = **dk + 0,4 mm**. Escareado com a ponta do cone virada para cima (abre para a face de cima) imprime bem; escareado aberto na face de baixo (na mesa) também imprime (o cone de 45° é autossustentável). Escareado em PLA com aperto forte trinca: preferir cabeça cilíndrica em peça com carga.

---

## 5. Insertos térmicos (heat-set inserts)

### 5.1 Tabela CNC Kitchen (fabricante)

Fonte: imagem "Dimensions & Design Guidelines: Metric size inserts" da loja oficial ([cnckitchen.store](https://cnckitchen.store/products/heat-set-insert-m3-x-5-7-100-pieces)).

| Tipo | L (comprimento) | D1 (Ø inserto) | **D2 (Ø furo)** | **W (parede mín.)** |
|---|---|---|---|---|
| M2 x 3 | 3,0 | 3,6 | **3,2** | 1,3 |
| M2.5 x 4 | 4,0 | 4,6 | **4,0** | 1,6 |
| M3 x 5,7 (standard) | 5,7 | 4,6 | **4,0** | 1,6 |
| M3 x 3 (short) | 3,0 | 4,6 | **4,0** | 1,6 |
| M3 x 5 x 4 (Voron) | 4,0 | 5,0 | **4,4** | 1,6 |
| M4 x 8,1 | 8,1 | 6,3 | **5,7** | 2,1 |
| M4 x 4 (short) | 4,0 | 6,3 | **5,7** | 2,1 |
| M5 x 9,5 | 9,5 | 7,1 | **6,5** | 2,6 |
| M5 x 5,8 (short) | 5,8 | 7,1 | **6,5** | 2,6 |
| M6 x 12,7 | 12,7 | 8,7 | 8,1 | 3,3 |
| M8 x 12,7 | 12,7 | 10,2 | 9,7 | 4,5 |

Furo cego: profundidade mínima **L + 1 mm**.

### 5.2 Tabela Ruthex (fabricante)

Fonte: tabela "Größe" na página do produto ([ruthex.de, RX-M3x5.7](https://www.ruthex.de/en/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen)). d1 = Ø externo, d2 = Ø do corpo inferior, **d3 = Ø do furo**, W = parede mín., furo com profundidade mín. L + 1 mm.

| Tipo | d1 | d2 | **d3 (furo)** | L | **W** |
|---|---|---|---|---|---|
| M2 | 3,6 | 3,1 | **3,2** | 4,0 | 1,3 |
| M2.5 | 4,6 | 3,9 | **4,0** | 5,7 | 1,6 |
| M3 short | 4,6 | 3,9 | **4,0** | 4,0 | 1,6 |
| M3x5x4 Voron | 5,0 | 4,25 | **4,4** | 4,0 | 1,3 |
| M3 | 4,6 | 3,9 | **4,0** | 5,7 | 1,6 |
| M4 short | 6,3 | 5,5 | **5,6** | 4,0 | 2,1 |
| M4 | 6,3 | 5,5 | **5,6** | 8,1 | 2,1 |
| M5 short | 7,1 | 6,3 | **6,4** | 5,8 | 2,6 |
| M5 | 7,1 | 6,3 | **6,4** | 9,5 | 2,6 |
| M6 | 8,7 | 7,9 | 8,0 | 12,7 | 3,3 |
| M8 | 10,1 | 9,5 | 9,6 | 12,7 | 4,5 |

A Ruthex vende jogo de brocas para insertos de 3,2 / 4,0 / 5,6 / 6,4 / 8,0 mm (confirma os furos M2 / M2.5–M3 / M4 / M5 / M6) ([ruthex.de](https://www.ruthex.de/en/products/ruthex-hss-bohrer-set-5-tlg-fur-gewindeeinsatze-m2-m2-5-m3-m4-m5-m6-din-338-bohrer-3-2-4-0-5-6-6-4-8-0-mm-fur-kunststoff-stahl-alu-kupfer-messing-uvm)).

Diferenças entre fabricantes: M4 5,6 (Ruthex) x 5,7 (CNC Kitchen); M5 6,4 x 6,5. Comprimento do M2 e M2.5 também difere (Ruthex M2 = 4,0 / M2.5 = 5,7; CNC Kitchen M2 = 3,0 / M2.5 = 4,0). **Projetar pelo fabricante que vai ser comprado.**

### 5.3 Padrão do projeto

| Rosca | Inserto padrão | Ø furo no CAD | Profundidade (cego) | Parede mín. | Boss externo adotado |
|---|---|---|---|---|---|
| M2 | M2 x 3 (CNC K.) / M2 x 4 (Ruthex) | 3,2 | L + 1 | 1,3 | 6,0 |
| M2.5 | M2.5 | 4,0 | L + 1 | 1,6 | 7,5 |
| M3 | **M3 x 5,7** | **4,0** | **6,7** | 1,6 | **7,5–8,0** |
| M3 (pouca altura) | M3 x 3 / M3 short x 4 | 4,0 | L + 1 | 1,6 | 7,5 |
| M4 | M4 x 8,1 | 5,6 | 9,1 | 2,1 | 10 |
| M5 | M5 x 9,5 | 6,4 | 10,5 | 2,6 | 12 |

Boss externo adotado = Ø furo + 2 x (W + ~0,8 mm de margem) → arredondado para cima. W é mínimo absoluto; peça com torque usa mais.

Regras do fabricante (CNC Kitchen: [blog de dicas](https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey)):
- Furo **reto, não cônico**; normalmente **sem chanfro** na borda.
- Furo cego ~1 mm mais fundo que o inserto; furo passante pode ter o comprimento do inserto.
- Furos impressos saem menores; o teste do M3 usa furos de **4,0 a 4,4 mm**. Se apertado, aumentar em passos de 0,1 mm.
- Temperatura do ferro: **10–20 °C acima da temperatura de impressão**: ~225 °C PLA, 245 °C PETG, 265 °C ABS.
- Derreter ~90% da profundidade com a ponta e terminar empurrando com ferramenta plana; segurar alguns segundos (o inserto tende a subir).
- Encurtar inserto reduz a resistência.

Orientação: eixo do inserto preferencialmente em Z (instalação de cima para baixo, camadas envolvendo o inserto). Perímetros do boss >= 3–4 (o inserto ancora nos perímetros).

---

## 6. Ímãs de neodímio (press-fit)

| Parâmetro | Valor adotado | Faixa / fonte |
|---|---|---|
| Ø do alojamento (press-fit, vertical) | **Ø ímã + 0,15 mm** (PLA) / **+ 0,25 mm** (PETG) | +0,1 a +0,2 (PLA), ~+0,3 (PETG), relatos de usuários: [Prusa forum](https://forum.prusa3d.com/forum/how-do-i-print-this-printing-help/how-to-safely-insert-magnets-into-a-print), [MakerWorld press-fit magnet](https://makerworld.com/models/2932423) |
| Profundidade | **altura do ímã + 0,05 a 0,1 mm** (rente) | idem |
| Ímã embutido com pausa | folga 0,15 em todas as direções + gota de cola CA | [Prusa Blog](https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/) |
| Camadas por cima (ímã escondido) | 2–3 camadas (0,4–0,6 mm) para esconder ([Prusa Blog](https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/)); manter o mínimo possível, porque a força de atração cai rápido com a distância (física do ímã, não medido nesta pesquisa) | |
| Parede em volta | >= 1,2 mm (3 linhas) | adotado |

Cuidados:
- Medir o ímã com paquímetro: ímãs baratos variam +-0,1 mm.
- Ímã com pausa precisa estar bem preso (folga justa ou cola): o bico/extrusora de aço pode puxar o ímã para fora ([Prusa KB pause](https://help.prusa3d.com/article/insert-pause-or-custom-g-code-at-layer_120490), [Prusa forum](https://forum.prusa3d.com/forum/how-do-i-print-this-printing-help/how-to-safely-insert-magnets-into-a-print)).
- Ímãs próximos se atraem e podem arrancar a peça da mesa durante a impressão.
- **Polaridade**: marcar no CAD/na peça qual face fica para fora; testar o par antes de colar.
- Ímã em peça de carro no sol: neodímio comum (N) perde magnetismo de forma permanente acima de ~80 °C (dado de catálogo genérico, não confirmado em fonte primária nesta pesquisa).

---

## 7. Regras gerais de fixação

- Parede em volta de qualquer furo roscado >= diâmetro do parafuso ([Hubs](https://www.hubs.com/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners/)).
- Preferir **inserto** para tudo que desmonta; **porca embutida** para máxima força de arrancamento; **parafuso direto** para montagem permanente.
- Carga de tração no parafuso deve comprimir camadas (parafuso vertical apertando peças empilhadas), não separar camadas.
- Arruela sob a cabeça em PLA/PETG com aperto: distribui carga e reduz fluência (creep).
- Plásticos fluem sob carga constante (creep), pior com calor: parafuso apertado em peça de PLA no carro perde aperto. Ver [materiais.md](materiais.md).
