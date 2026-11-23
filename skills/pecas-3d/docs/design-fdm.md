# Design para FDM: regras de projeto

Referência rápida para projetar peças em FreeCAD que vão ser impressas em FDM (filamento), bico padrão **0,4 mm**.
Cada número importante tem a fonte ao lado. Quando as fontes divergem, aparece o intervalo e o **valor adotado pelo projeto** (sempre calibrar com peça de teste antes de confiar).

Lista completa de fontes: [fontes.md](fontes.md). Encaixes e folgas: [tolerancias-encaixes.md](tolerancias-encaixes.md). Parafusos, insertos e ímãs: [fixacao.md](fixacao.md).

---

## 0. Resumo dos padrões do projeto (cola rápida)

| Regra | Padrão adotado | Faixa nas fontes | Fonte |
|---|---|---|---|
| Bico | 0,4 mm | - | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) |
| Largura de linha (extrusion width) | 0,45 mm (Prusa) / 0,42 mm (Bambu/Orca) | - | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) |
| Altura de camada | 0,20 mm | 0,10 a 0,32 mm (máx. 80% do bico) | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |
| Parede mínima imprimível | 0,9 mm (2 linhas) | 0,45 mm (1 linha) a 1,0 mm | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135), [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) |
| Parede funcional (carga leve) | 1,6 a 1,8 mm (4 linhas) | - | adotado (múltiplo da largura de linha) |
| Overhang sem suporte | 45° em relação à vertical | 45° a 60°; até 75° em impressoras com refrigeração 360° | [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/), [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) |
| Ponte (bridge) | até 10 mm; ideal até 5 mm | < 5 mm sem flecha; < 10 mm aceitável | [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/), [Hydra/AMIST](https://centers.louisville.edu/amist/amist-print-farm) |
| Aresta em contato com a mesa | chanfro 45°, 0,4 a 0,6 mm | - | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135), [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) |
| Furo horizontal > ~5 mm | perfil gota (teardrop) 45° | - | ver seção 9 |
| Detalhe mínimo (feature) | 2,0 mm | - | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) |
| Pino mínimo | 3,0 mm; pino estrutural > 5 mm | 1 a 5 mm | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf), [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) |
| Furo mínimo | 2,0 mm | - | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) |
| Texto em relevo/baixo-relevo | profundidade 1,0 mm, altura da letra >= 5 mm, traço >= 0,8 mm | 0,3 a 1,0 mm | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) + adotado |
| Precisão esperada | +-0,2 mm (Prusa calibrada); +-0,5% (mín. +-0,5 mm) genérico desktop | - | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135), [Hubs](https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/) |
| Resistência no eixo Z | ~50% da resistência no plano XY | - | [CNC Kitchen](https://cnckitchen.com/blog/stop-printing-flat-the-45-secret-for-stronger-parts) |

---

## 1. Largura de linha, paredes e espessura mínima

A espessura de uma parede vertical deve ser um **múltiplo da largura de linha** (extrusion width). Paredes "quebradas" (ex.: 1,1 mm com linha de 0,45 mm) geram gap fill ou buracos.

Tabela da Prusa (bico 0,4 mm, largura de linha 0,45 mm no PrusaSlicer): [Prusa KB, Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135):

| Perímetros | Espessura (PrusaSlicer, 0,45 mm) | Equivalente Orca/Bambu (0,42 mm) | Uso |
|---|---|---|---|
| 1 | 0,45 mm | 0,42 mm | só decorativo; frágil |
| 2 | 0,9 mm (sugestão exata: 0,86 mm) | 0,84 mm | mínimo imprimível com qualidade; caixas leves |
| 3 | 1,35 mm | 1,26 mm | paredes de carcaça |
| 4 | 1,8 mm | 1,68 mm | **padrão funcional do projeto** |
| 6 | 2,7 mm | 2,52 mm | estrutural / com carga |

- "Walls thinner than one nozzle perimeter are not printable": paredes abaixo de 1 linha somem no fatiamento ([Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)).
- Valor sugerido para 2 perímetros a 0,2 mm de camada: **0,86 mm** ([Prusa KB, Layers and perimeters](https://help.prusa3d.com/article/layers-and-perimeters_1748)).
- Fontes de birô (impressoras industriais) pedem **1,0 mm** como mínimo para paredes apoiadas e não apoiadas ([UZH AMF](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf)); a Hubs cita 0,8 mm como valor que qualquer impressora atende ([Hubs](https://www.hubs.com/knowledge-base/key-design-considerations-3d-printing/)).
- O gerador de perímetros **Arachne** (padrão no PrusaSlicer 2.5+, Orca, Bambu Studio e Cura 5) varia a largura da linha e tolera melhor paredes fora do múltiplo, mas o múltiplo continua sendo o ideal.

**Padrão do projeto:** parede mínima 0,9 mm só para peça decorativa; **1,6–1,8 mm** para peça funcional; >= 2,4 mm onde houver parafuso, inserto ou carga.

**Fugir do padrão quando:** peça flexível de TPU (paredes finas dão flexibilidade); vaso/spiral mode (1 linha de propósito); peça grande sem carga (pode baixar para 1,2 mm).

---

## 2. Altura de camada

| Item | Valor | Fonte |
|---|---|---|
| Máximo | < 80% do bico → **0,32 mm** com bico 0,4 | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |
| Mínimo recomendado | 0,10 mm ("we do not suggest going lower than 0.10 mm") | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |
| Primeira camada | **0,20 mm** (padrão de todos os perfis Prusa) | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |
| Padrão do projeto | **0,20 mm** | adotado |

- Camada menor = melhor resolução em Z e overhang/curvas mais limpos, mais tempo de impressão.
- Projetar alturas (Z) de detalhes como **múltiplos da altura de camada** (0,2 mm): degraus de 0,3 mm viram 0,2 ou 0,4.
- Camada mais grossa tende a reduzir adesão entre camadas em alguns estudos ([meta-análise citada pelo CNC Kitchen/estudos acadêmicos](https://cnckitchen.com/blog/stop-printing-flat-the-45-secret-for-stronger-parts)); para peça estrutural, ficar em 0,2 mm.

---

## 3. Overhang (balanço)

Ângulo medido **a partir da vertical** (0° = parede vertical, 90° = teto horizontal).

| Fonte | Limite sem suporte |
|---|---|
| [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) | "can usually be printed up to 45°"; acima disso precisa de suporte |
| [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) | 45° a 60° conforme bico e ajustes; até **75°** em impressoras com refrigeração 360° (MK4S, CORE One) |
| [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) | 45° |

**Padrão do projeto: 45°.** Superfícies funcionais (que encaixam) nunca acima de 45°. Até 55° só em superfície estética, sabendo que a face de baixo fica mais rugosa.

---

## 4. Pontes (bridging)

Ponte = trecho horizontal ligando dois apoios, impresso "no ar".

| Fonte | Valor |
|---|---|
| [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) | **< 5 mm** evita flecha e marcas; mais longo precisa dividir a peça ou pós-processar |
| [Hydra Research / AMIST cheat sheet](https://centers.louisville.edu/amist/amist-print-farm) | < 10 mm |

**Padrão do projeto:** ponte até **10 mm** é aceitável; até **5 mm** quando a face de baixo é funcional. Acima de 10 mm: redesenhar (pilar intermediário, arco, teto em 45°, dividir peça).

A primeira camada da ponte flecha um pouco: se a face de baixo da ponte é cota de encaixe, somar ~1 altura de camada de folga ali.

---

## 5. Suportes: como evitar no design

Suporte custa tempo, material e deixa marca. Ordem de preferência:

1. **Reorientar a peça** para que nenhum overhang passe de 45° (ver seção 8, mas sem sacrificar resistência).
2. **Chanfro de 45° no lugar de teto horizontal** (ex.: rebaixo, bolsão de porca virado para baixo).
3. **Furos horizontais em gota** (seção 9).
4. **Dividir a peça** em partes que imprimem planas e juntar com parafuso/cola/encaixe.
5. **Ponte curta** (< 5–10 mm) no lugar de overhang.
6. **Camada de sacrifício**: membrana de 1 camada (0,2 mm) tampando um furo que fica de cabeça para baixo; perfura depois com broca/estilete. Útil para nut trap / alojamento de cabeça virado para a mesa.
7. Só então suporte. Preferir **suporte em árvore/orgânico** ("easily removable, do not scar the surface, and are fast and cheap to print": [Prusa KB, Organic supports](https://help.prusa3d.com/article/organic-supports_480131)).

Detalhes de suporte no fatiador: [fatiamento.md](fatiamento.md).

---

## 6. Chanfro x filete (regra "chanfro embaixo, filete em cima")

| Onde | Usar | Por quê |
|---|---|---|
| Arestas na face apoiada na mesa (horizontais, de baixo) | **Chanfro 45°** | Filete na face de baixo vira overhang que chega a ~90° na base; chanfro de 45° fica dentro do limite. A Prusa recomenda chanfro para acabamento limpo ([Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)). |
| Arestas de cima e verticais | **Filete** (raio) | Filete em cima não cria overhang; filete em aresta vertical é desenhado no plano XY, sem problema. |
| Base da peça (contato com a mesa) | Chanfro 45° de 0,4–0,6 mm | Compensa elephant foot e reduz warping ([Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/): "Add a 45° chamfer or radius on edges touching the build plate"). |
| Cantos internos com carga | Filete >= 0,5x espessura | Concentração de tensão (mesma regra do snap-fit, ver tolerancias-encaixes.md). |

---

## 7. Elephant foot (pé de elefante)

A primeira camada é esmagada contra a mesa e sai **mais larga** que o desenho ([Prusa KB, Elephant foot compensation](https://help.prusa3d.com/article/elephant-foot-compensation_114487)).

| Ação | Valor | Fonte |
|---|---|---|
| Compensação no fatiador | **0,2 mm** "usually work well for the default 0.4 mm nozzle" | [Prusa KB](https://help.prusa3d.com/article/elephant-foot-compensation_114487) |
| No design | chanfro 45° de **0,4–0,6 mm** na aresta de baixo | adotado (redundância com a compensação; [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) recomenda chanfro/raio na base) |
| Sinal de excesso | brim descolado da peça → compensação alta demais | [Prusa KB](https://help.prusa3d.com/article/elephant-foot-compensation_114487) |

Na prática do projeto: **sempre** chanfrar a base em peças que encaixam pela face de baixo (tampas, gavetas, encaixes deslizantes).

---

## 8. Orientação da peça e anisotropia

A peça FDM é **anisotrópica**: a ligação entre camadas (eixo Z) é o ponto fraco.

### Números

| Material / teste | Plano XY | Eixo Z | Razão Z/XY | Fonte |
|---|---|---|---|---|
| PLA, tração, Prusa CORE One, camada 0,2 | 63 MPa | 31 MPa | ~49% | [CNC Kitchen](https://cnckitchen.com/blog/stop-printing-flat-the-45-secret-for-stronger-parts) |
| PLA, impacto | 26,6 kJ/m² | 13,8 kJ/m² | 52% | [Bambu Filament Guide](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| PETG, impacto | 52,7 kJ/m² | 13,6 kJ/m² | 26% | idem |
| ABS, impacto | 39,3 kJ/m² | 7,4 kJ/m² | 19% | idem |
| ASA, impacto | 41,0 kJ/m² | 4,9 kJ/m² | 12% | idem |
| PC, impacto | 34,8 kJ/m² | 9,0 kJ/m² | 26% | idem |
| PAHT-CF, impacto | 57,5 kJ/m² | 13,3 kJ/m² | 23% | idem |

- CNC Kitchen: "layer adhesion is typically around 50% of the in-plane strength", podendo cair muito com ABS e muita ventilação ([CNC Kitchen](https://cnckitchen.com/blog/stop-printing-flat-the-45-secret-for-stronger-parts)).
- Imprimir **inclinado** ajuda quando não dá para deitar: 30° = 44 MPa, 45° = 40 MPa, 60° = 36 MPa contra 31 MPa em pé (mesma fonte). Recomendação dele: inclinar pelo menos 45°.

### Regras de orientação

1. **Carga de tração/flexão deve correr ao longo das camadas (XY), nunca puxando uma camada da outra.** Ex.: gancho de parede impresso deitado de lado, não em pé.
2. **Snap-fit, clipes e molas** sempre no plano XY ([Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/): "avoid snap-fit cantilevers built vertically in the Z direction").
3. **Furos de precisão** na vertical (eixo do furo = Z) saem redondos; furos horizontais saem ovalados/caídos no topo.
4. **Maior face plana na mesa** para adesão e para evitar suporte.
5. Conflito entre resistência e suporte: **resistência ganha** em peça funcional; aceitar suporte ou dividir a peça.
6. Pino/eixo que leva flexão: deitar (eixo em X/Y). Pino vertical pequeno quebra na linha de camada ([Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/): pinos < 5 mm são fracos; adicionar filete na base ou usar pino metálico).

---

## 9. Furos horizontais: perfil gota (teardrop)

O topo de um furo redondo horizontal é um overhang que chega a 90° (teto). Solução clássica: **perfil gota**: círculo com o topo substituído por duas retas a 45° que se encontram numa ponta.

| Situação | Solução |
|---|---|
| Furo horizontal <= ~5 mm | redondo normal costuma passar (ponte curta); folga extra de ~1 camada no topo |
| Furo horizontal > 5 mm, funcional | **teardrop 45°** (ponta para cima, +Z) |
| Teardrop alto demais para o espaço | **gota truncada**: corta a ponta e deixa um topo plano curto (vira ponte curta) |
| Alternativa | hexágono com vértice para cima (overhang máximo 30°) ou quadrado girado 45° |
| Furo para parafuso de precisão | reorientar a peça para o furo ficar vertical, ou imprimir menor e furar com broca ([Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/)) |

Construção no FreeCAD (Part/Sketcher): círculo de raio r + duas tangentes a 45° a partir dos pontos (±r·sin45°, r·cos45°) até a ponta em (0, r·√2). A ponta fica **1,414·r** acima do centro. Gota truncada: cortar em altura r·1,1 a r·1,2.

Fonte da técnica: guias de design (ex.: [Meltio Design Guidelines](https://meltio3d.com/wp-content/uploads/2024/02/Meltio_Whitepapers_Design-Guidelines.pdf), [Fabbaloo, "The new teardrop"](https://www.fabbaloo.com/2011/12/the-new-teardrop-html)). Não há "norma" de fabricante sobre isso; é prática consolidada.

---

## 10. Primeira camada

| Item | Valor | Fonte |
|---|---|---|
| Altura | 0,20 mm | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |
| Compensação de elephant foot | 0,2 mm | [Prusa KB](https://help.prusa3d.com/article/elephant-foot-compensation_114487) |
| Brim | >= 3 mm quando a base é pequena/alta | [Prusa KB, Skirt and brim](https://help.prusa3d.com/article/skirt-and-brim_133969) |

No design:
- A face de baixo é a mais plana e a mais precisa em Z; deixar nela as superfícies de referência.
- Evitar contato pontual ou linha fina com a mesa: criar uma "sapata" plana.
- Cantos vivos na base levantam (warping), principalmente ABS/ASA/PA: arredondar cantos em planta (raio >= 2–3 mm) e chanfrar a aresta ([Hubs, accuracy](https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/): "Adding a radius on the bottom edge in contact with the build plate or a brim is recommended").

---

## 11. Cantos vivos

- **Cantos internos** (reentrantes) concentram tensão: filete de pelo menos 0,5–1 mm em peça funcional; >= 0,5x espessura em raiz de clipe/aba.
- **Cantos externos em planta** (vistos de cima) não podem ser mais finos que o bico: o bico de 0,4 mm arredonda naturalmente com raio ~0,2 mm. Não projetar canto externo com raio menor que 0,2 mm esperando nitidez.
- **Cantos externos na base** levantam com warping (seção 10).
- **Pontas agudas** (cunhas < 30°) viram blob ou somem; truncar com face de >= 0,8 mm.

---

## 12. Texto em relevo e baixo-relevo

| Parâmetro | Valor adotado | Fonte / observação |
|---|---|---|
| Altura (relevo) ou profundidade (baixo-relevo) | **1,0 mm** (mínimo 0,6 mm = 3 camadas) | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf): "Min. 1.0 mm embossed" |
| Tamanho da fonte | **>= 14 pt (~5 mm de altura)** | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) |
| Espessura do traço | **>= 0,8 mm** (2 linhas de extrusão) | adotado (múltiplo da largura de linha) |
| Tipo de fonte | sem serifa, bold (ex.: DejaVu Sans Bold, Liberation Sans Bold) | legibilidade depende muito da fonte ([UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf)) |

Outras referências dão valores menores (0,3 mm de relevo, 0,5 mm de baixo-relevo): o 1,0 mm do projeto é conservador e garante leitura.

Onde colocar:
- **Face de cima**: melhor resultado (relevo ou baixo-relevo).
- **Face vertical**: bom; letras com partes horizontais viram pequenas pontes.
- **Face de baixo (na mesa)**: só baixo-relevo, e ainda assim com bordas menos nítidas; relevo na face de baixo exige suporte.
- Baixo-relevo é mais robusto (não quebra) e não atrapalha empilhamento/encaixe.

---

## 13. Detalhes mínimos

| Detalhe | Mínimo | Fonte |
|---|---|---|
| Feature genérica | 2,0 mm | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) |
| Pino (diâmetro) | 3,0 mm (imprime); > 5 mm para ter perímetros + infill e resistência real | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf), [Hubs](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) |
| Furo | 2,0 mm (depende do comprimento do furo e da parede em volta) | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) |
| Folga entre peças/partes móveis | 0,5 mm (birô) / >= 0,3 mm (Prusa) | [UZH](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf), [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) |
| Aba/clipe (espessura) | >= 1,0 mm na raiz | [Hubs](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) |
| Rosca impressa | não abaixo de M5 | [Hubs](https://www.hubs.com/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners/) |

Furos menores que ~3 mm: imprimir menores e furar com broca, ou deixar só uma marca de centro.

---

## 14. Precisão dimensional e contração

| Item | Valor | Fonte |
|---|---|---|
| Precisão Prusa calibrada | "accurate to at least 0.2 mm" | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) |
| FDM desktop (genérico) | +-0,5% (limite inferior +-0,5 mm) | [Hubs](https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/) |
| FDM industrial | +-0,15% (limite inferior +-0,2 mm) | [Hubs](https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/) |
| Contração | 0,2–1% conforme material; ABS 1–2% | [Hubs](https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/), [Prusa KB ABS](https://help.prusa3d.com/article/abs_2058) |

- **Furos verticais saem menores** que o CAD ("Printed holes usually come out smaller than in CAD": [CNC Kitchen](https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey)). Compensação: ver [tolerancias-encaixes.md](tolerancias-encaixes.md).
- Peças grandes perdem precisão; dividir objetos grandes melhora a precisão de cada parte ([Hubs](https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/)).
- **Exportar STL/3MF com tesselação fina** no FreeCAD (desvio <= 0,01–0,02 mm): furo de 3 mm com tesselação grossa vira polígono e fica menor ainda.

---

## 15. Checklist antes de exportar

- [ ] Orientação de impressão definida e carga principal no plano XY.
- [ ] Nenhum overhang > 45° sem solução (chanfro, gota, ponte curta, divisão).
- [ ] Pontes <= 10 mm.
- [ ] Paredes múltiplas da largura de linha; >= 1,6 mm onde é funcional.
- [ ] Chanfro na base (0,4–0,6 mm) e chanfros (não filetes) nas arestas de baixo.
- [ ] Furos horizontais > 5 mm em gota.
- [ ] Folgas de encaixe aplicadas (tolerancias-encaixes.md).
- [ ] Furos de parafuso/inserto conforme fixacao.md.
- [ ] Material escolhido pela temperatura de uso (materiais.md).
- [ ] Peça de teste de tolerância impressa antes da peça final, se houver encaixe.
