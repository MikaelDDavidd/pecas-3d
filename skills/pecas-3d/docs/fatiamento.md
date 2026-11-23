# Fatiamento: parâmetros que mandam na resistência

O design (design-fdm.md) define o que dá para imprimir; o fatiador define quão forte a peça sai.
Este documento lista os parâmetros que importam, os valores padrão do projeto e o **nome de cada parâmetro** nos fatiadores populares.

---

## 0. Regra principal: paredes antes de infill

- "The strength of a model is mostly defined by the number of perimeters (not infill)." Para peça mais forte, aumente perímetros; infill ajuda principalmente na **compressão** ([Prusa KB, Infill](https://help.prusa3d.com/article/infill_42); repetido em [Layers and perimeters](https://help.prusa3d.com/article/layers-and-perimeters_1748)).
- Teste independente (flexão): cada +10% de infill somou ~1,5 kg na carga de ruptura; **2 perímetros extras somaram ~1,67 kg** gastando só 0,42 m de filamento ([HackSpace magazine](https://hackspace.raspberrypi.com/articles/experiments-with-strong-3d-prints)).
- A carga numa peça em flexão/torção se concentra na "casca" (paredes + topo/fundo), exatamente como num tubo. Infill alto é caro e rende pouco.

---

## 1. Perfis padrão do projeto

| Parâmetro | Decorativo | **Funcional (padrão)** | Estrutural |
|---|---|---|---|
| Altura de camada | 0,20 mm | **0,20 mm** | 0,20 mm |
| Primeira camada | 0,20 mm | **0,20 mm** | 0,20 mm |
| Paredes (perímetros) | 2 | **4** (~1,7 mm) | 6 (~2,6 mm) |
| Camadas de topo | 4 (0,8 mm) | **5 (1,0 mm)** | 6–7 (1,2–1,4 mm) |
| Camadas de fundo | 3 (0,6 mm) | **4 (0,8 mm)** | 5 (1,0 mm) |
| Infill | 10–15% | **20–25%** | 40–50% |
| Padrão de infill | gyroid / adaptive cubic | **gyroid** (ou cubic) | gyroid / cubic |
| Gerador de paredes | Arachne | **Arachne** | Arachne |
| Compensação elephant foot | 0,2 mm | **0,2 mm** | 0,2 mm |
| Brim | não (salvo base pequena) | conforme seção 6 | conforme seção 6 |
| Suporte | evitar no design; árvore se precisar | idem | idem |

Faixas das fontes para infill:
- Prusa: "Most models can be printed with 10-15% infill"; "You'll rarely need infill higher than 30%"; 100% força padrão rectilinear e pode piorar a aparência ([Prusa KB](https://help.prusa3d.com/article/infill_42)).
- UltiMaker: no mínimo 15% em aplicações padrão ([UltiMaker Cura: Infill settings](https://support.ultimaker.com/s/article/1667411002588)); 15–25% gyroid/cubic para protótipo funcional, 30–50% para peça de uso final ([UltiMaker, infill patterns](https://ultimaker.com/learn/mastering-3d-printing-infill-patterns-from-gyroid-to-lightning/)).

**Fugir do padrão quando:**
- Peça leva **compressão** (pé de móvel, calço, apoio): subir infill (40–60%) antes de paredes.
- Peça de **TPU** que deve ser macia: 1–2 paredes, 10–15% infill ([Prusa KB, Flexible](https://help.prusa3d.com/article/flexible-materials_2057)).
- Peça pequena (< ~20 mm) funcional: com 4–6 paredes ela já fica quase sólida; infill quase não importa.
- Região de parafuso/inserto/ímã: usar **modificador local** (seção 7) em vez de subir o infill da peça inteira.

---

## 2. Paredes / perímetros

| Item | Valor | Fonte |
|---|---|---|
| Mínimo dos perfis Prusa | 2 perímetros | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |
| Espessura por perímetro | 0,45 mm (Prusa) / 0,42 mm (Bambu/Orca) | [Prusa KB](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) |
| Arachne | larguras variáveis, lida com paredes finas; desativa "Detect thin walls" | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |

Mais paredes = mais resistência, rigidez e adesão entre camadas, ao custo de tempo ([OrcaSlicer wiki: Walls](https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_walls.html)).

---

## 3. Topo e fundo (top/bottom shells)

| Item | Valor | Fonte |
|---|---|---|
| Mínimo de camadas de topo | >= 3 | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |
| Exemplo Prusa | 3 camadas a 0,3 mm; 9 camadas a 0,1 mm (mesma espessura ~0,9 mm) | [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748) |
| Padrão do projeto | topo >= 1,0 mm, fundo >= 0,8 mm | adotado |

Pensar em **espessura**, não em número de camadas: se mudar a altura de camada, o número muda. PrusaSlicer e Orca têm "minimum shell thickness" para isso.

Infill baixo (< 15%) com topo fino gera "pillowing" (topo ondulado/furado): mais camadas de topo ou padrão que sustenta topo (ex.: support cubic, lightning: só para peça não estrutural).

---

## 4. Padrões de infill

| Padrão | Característica | Quando usar | Fonte |
|---|---|---|---|
| **Gyroid** | 3D, resistência igual em todas as direções, bom peso/resistência; "our favorite" (Prusa) | padrão funcional; não colide com o bico | [Prusa KB, Infill patterns](https://help.prusa3d.com/article/infill-patterns_177130) |
| **Cubic** | 3D, resistência XY e Z boas | alternativa mais rápida ao gyroid | [Prusa KB](https://help.prusa3d.com/article/infill-patterns_177130), [OrcaSlicer quick ref](https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_patterns_quick_reference.html) |
| Adaptive cubic | denso perto das paredes, ralo no meio; ~1/4 menos material que rectilinear | peças grandes com muito volume interno | [Prusa KB](https://help.prusa3d.com/article/infill-patterns_177130) |
| Grid | resistente, mas cruzamentos acumulam material, barulhento, pode falhar | evitar em velocidade alta | [Prusa KB](https://help.prusa3d.com/article/infill-patterns_177130) |
| Honeycomb | boa resistência mecânica, ~25% mais material, até 2x o tempo | quando tempo não importa | [Prusa KB](https://help.prusa3d.com/article/infill-patterns_177130) |
| Rectilinear | rápido; único recomendado para 100% | peça sólida | [Prusa KB](https://help.prusa3d.com/article/infill-patterns_177130) |
| Lightning / Support cubic | só sustenta o topo; **não** melhora propriedades mecânicas | peça decorativa | [Prusa KB](https://help.prusa3d.com/article/infill-patterns_177130) |
| Concentric | flexível | TPU, peças flexíveis | [Prusa KB](https://help.prusa3d.com/article/infill-patterns_177130) |

Quadro de notas do OrcaSlicer (escala 0–8, cubo de teste): gyroid, cubic, grid, honeycomb e TPMS-D com resistência 6 em XY e Z; lightning e support cubic com 2 ([OrcaSlicer wiki](https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_patterns_quick_reference.html)).

---

## 5. Suporte em árvore / orgânico

- Orgânico/árvore: "easily removable, do not scar the surface, and are fast and cheap to print"; grid gasta mais material, demora mais e marca a peça ([Prusa KB, Organic supports](https://help.prusa3d.com/article/organic-supports_480131)).
- Para superfície plana grande em balanço, suporte normal/snug pode ser melhor (comentário de representante Prusa na mesma página).
- **Pintar suporte** (paint-on supports / support blockers / enforcers) só onde precisa, em vez de "suporte em tudo".
- Interface de suporte no topo melhora a face de baixo; Prusa recomenda manter interface em vez de aumentar densidade de galhos ([Prusa KB](https://help.prusa3d.com/article/organic-supports_480131)).
- TPU: distância Z do suporte ~0,3 mm e separação XY >= 100% ([Prusa KB, Flexible](https://help.prusa3d.com/article/flexible-materials_2057)).
- Ângulo limite (overhang threshold) do projeto: **45°** (design-fdm.md, seção 3). Atenção: alguns fatiadores medem a partir da horizontal; conferir na interface.

---

## 6. Brim (aba de aderência)

| Item | Valor | Fonte |
|---|---|---|
| Largura mínima | **>= 3 mm** | [Prusa KB, Skirt and brim](https://help.prusa3d.com/article/skirt-and-brim_133969) |
| Quando usar | peça alta de base pequena; várias peças pequenas; base pequena | [Prusa KB](https://help.prusa3d.com/article/skirt-and-brim_133969) |
| Padrão do projeto | PLA/PETG: só se base pequena ou alta (3–5 mm). ABS/ASA/PA/PC: **5–8 mm** sempre em peça com cantos (warping) | adotado |
| Brim descolado da peça | elephant foot compensation alta demais | [Prusa KB](https://help.prusa3d.com/article/elephant-foot-compensation_114487) |

Brim em peça com encaixe pela base: retirar bem (rebarba vira interferência). Alternativa: "mouse ears" (discos só nos cantos) modelados no CAD ou pelo fatiador.

---

## 7. Modificadores locais

Aumentar paredes/infill **só** onde precisa (em volta de inserto, porca, furo de parafuso):
- PrusaSlicer: Add modifier → mudar Perimeters / Fill density só naquele volume.
- OrcaSlicer / Bambu Studio: Add modifier (ou "Negative part/Modifier") por objeto.
- Cura: Per Model Settings → "Modify settings for overlaps" / Infill mesh.

Alternativa no próprio CAD: modelar um furo fino "falso" (0,1–0,2 mm) em volta da região → o fatiador cria perímetros ali (técnica comum; não confirmada em fonte primária nesta pesquisa).

---

## 8. Precisão dimensional no fatiador

| Ajuste | Uso | Fonte |
|---|---|---|
| Elephant foot compensation | 0,2 mm com bico 0,4 | [Prusa KB](https://help.prusa3d.com/article/elephant-foot-compensation_114487) |
| X-Y hole compensation (Orca/Bambu) | aumenta/diminui só furos | [OrcaSlicer wiki: Precision](https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_precision.html) |
| X-Y contour compensation (Orca/Bambu) | aumenta/diminui o contorno externo | idem |
| Calibração | medir peça de teste, desvio / 2 = compensação por lado | [OrcaSlicer wiki](https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_precision.html), [MakerWorld X-Y tool](https://makerworld.com/en/models/129893-x-y-compensation-tool) |

**Regra do projeto:** como o CAD do projeto já soma +0,15 mm em furos verticais (tolerancias-encaixes.md, seção 2), deixar X-Y hole compensation em **0** no fatiador: senão compensa duas vezes. Se um dia a compensação passar para o fatiador, zerar no CAD.

---

## 9. Nome dos parâmetros por fatiador

Nomes conforme a interface em inglês. Bambu Studio e OrcaSlicer compartilham a mesma base (Orca é um fork do Bambu Studio), por isso os nomes coincidem.

| Conceito | PrusaSlicer | OrcaSlicer / Bambu Studio | UltiMaker Cura |
|---|---|---|---|
| Altura de camada | Layer height | Layer height | Layer Height |
| Primeira camada | First layer height | Initial layer height | Initial Layer Height |
| Paredes | Perimeters | Wall loops | Wall Line Count (ou Wall Thickness) |
| Gerador de paredes | Perimeter generator (Classic/Arachne) | Wall generator (Classic/Arachne) | (Arachne nativo desde Cura 5) |
| Topo / fundo | Solid layers: Top / Bottom; Minimum shell thickness | Top shell layers / Bottom shell layers; Top/Bottom shell thickness | Top Layers / Bottom Layers; Top/Bottom Thickness |
| Densidade de infill | Fill density | Sparse infill density | Infill Density |
| Padrão de infill | Fill pattern | Sparse infill pattern | Infill Pattern |
| Suporte ligado | Generate support material | Enable support | Generate Support |
| Tipo de suporte | Style: Grid / Snug / Organic | Type: normal(auto) / tree(auto) | Support Structure: Normal / Tree |
| Ângulo limite de suporte | Overhang threshold | Threshold angle | Support Overhang Angle |
| Brim | Brim type + Brim width (Skirt and brim) | Brim type + Brim width | Build Plate Adhesion Type = Brim; Brim Width |
| Elephant foot | Elephant foot compensation | Elephant foot compensation | Initial Layer Horizontal Expansion (valor negativo) |
| Compensação de contorno | XY Size Compensation | X-Y contour compensation | Horizontal Expansion |
| Compensação de furo | (sem opção dedicada na KB consultada) | X-Y hole compensation | Hole Horizontal Expansion |
| Pausa em camada | Insert pause print (M601) no slider | Add pause (slider de camadas) | Post Processing → Pause at height |
| Modificador local | Add modifier | Add modifier | Per Model Settings / Infill mesh |

Fontes dos nomes: [Prusa KB](https://help.prusa3d.com/article/layers-and-perimeters_1748), [Prusa KB Organic supports](https://help.prusa3d.com/article/organic-supports_480131), [Prusa KB pause](https://help.prusa3d.com/article/insert-pause-or-custom-g-code-at-layer_120490), [OrcaSlicer wiki](https://www.orcaslicer.com/wiki/), [UltiMaker Cura: Infill settings](https://support.ultimaker.com/s/article/1667411002588). Os nomes do Cura para expansão horizontal, suporte e brim vêm do conhecimento da interface e não foram conferidos página a página nesta pesquisa.

---

## 10. Ordem de ajuste quando a peça quebra

1. Orientação errada (carga separando camadas)? → reorientar (design-fdm.md, seção 8).
2. Poucas paredes? → +2 perímetros.
3. Topo/fundo finos? → >= 1,0 mm.
4. Material errado para a temperatura/impacto? → materiais.md.
5. Adesão de camada fraca (ABS/ASA com muita ventilação, temperatura baixa)? → menos ventilação, +5–10 °C no bico, impressora fechada ([CNC Kitchen](https://cnckitchen.com/blog/stop-printing-flat-the-45-secret-for-stronger-parts) cita queda forte de adesão em ABS com muita refrigeração).
6. Só então infill mais alto.
