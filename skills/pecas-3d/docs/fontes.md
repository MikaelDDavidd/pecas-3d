# Fontes

Lista curada das fontes usadas nos documentos de `docs/`. Pesquisa feita em outubro/2026.
Prioridade: documentação de fabricante (impressora, filamento, inserto) > testes publicados com método (CNC Kitchen) > guias de birôs de impressão > normas reproduzidas > fóruns (só quando não há fonte melhor, e sempre marcado).

## Fabricantes de impressora e fatiador

| Fonte | Para que serve |
|---|---|
| [Prusa KB: Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) | Tabela de espessura de parede por perímetros, overhang 45–60°/75°, folga móvel >= 0,3 mm, precisão 0,2 mm, chanfro na base. |
| [Prusa KB: Layers and perimeters](https://help.prusa3d.com/article/layers-and-perimeters_1748) | Altura de camada (máx. 80% do bico, mín. 0,10 mm), primeira camada 0,20 mm, mínimo de 2 perímetros, >= 3 camadas de topo, parede de 0,86 mm. |
| [Prusa KB: Infill](https://help.prusa3d.com/article/infill_42) | Infill 10–15% para a maioria, raramente > 30%; resistência vem dos perímetros. |
| [Prusa KB: Infill patterns](https://help.prusa3d.com/article/infill-patterns_177130) | Características de cada padrão de infill (gyroid, cubic, adaptive cubic, grid etc.). |
| [Prusa KB: Elephant foot compensation](https://help.prusa3d.com/article/elephant-foot-compensation_114487) | Valor de 0,2 mm para bico 0,4 e diagnóstico pelo brim descolado. |
| [Prusa KB: Organic supports](https://help.prusa3d.com/article/organic-supports_480131) | Vantagens e parâmetros do suporte orgânico/árvore. |
| [Prusa KB: Skirt and brim](https://help.prusa3d.com/article/skirt-and-brim_133969) | Brim de no mínimo 3 mm e quando usar. |
| [Prusa KB: Insert pause or custom G-code at layer](https://help.prusa3d.com/article/insert-pause-or-custom-g-code-at-layer_120490) | Como pausar a impressão para embutir porcas e ímãs. |
| [Prusa KB: PLA](https://help.prusa3d.com/article/pla_2062), [PETG](https://help.prusa3d.com/article/petg_2059), [ASA](https://help.prusa3d.com/article/asa_1809), [ABS](https://help.prusa3d.com/article/abs_2058), [PC](https://help.prusa3d.com/article/polycarbonate-pc_165812), [Nylon](https://help.prusa3d.com/article/nylon-pa_167188), [Flexible](https://help.prusa3d.com/article/flexible-materials_2057) | Fichas de material: temperatura de uso, UV, dificuldade, temperaturas de impressão, usos típicos. |
| [Prusa Blog: Practical uses of color change](https://blog.prusa3d.com/practical-uses-of-color-change-in-prusaslicer_59563/) | Folga de 0,15 mm em todas as direções para objetos embutidos (porca, ímã). |
| [Bambu Lab Filament Guide (PDF)](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) | Tabela comparável de HDT, flexão, módulo, impacto XY/Z (anisotropia), absorção de água, secagem e recozimento de 11 materiais. |
| [OrcaSlicer wiki](https://www.orcaslicer.com/wiki/) ([Precision](https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_precision.html), [Walls](https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_walls.html), [Infill](https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_infill.html), [Patterns quick reference](https://www.orcaslicer.com/wiki/print_settings/strength/strength_settings_patterns_quick_reference.html)) | Nomes e efeito de parâmetros no Orca/Bambu Studio; compensação X-Y de furo/contorno; notas de resistência por padrão de infill. |
| [UltiMaker Cura: Infill settings](https://support.ultimaker.com/s/article/1667411002588) | Infill mínimo de 15% e padrões para 80–100%. |
| [UltiMaker: Mastering infill patterns](https://ultimaker.com/learn/mastering-3d-printing-infill-patterns-from-gyroid-to-lightning/) | Faixas de infill por uso (15–25% protótipo funcional, 30–50% uso final). |

## Testes e ensaios

| Fonte | Para que serve |
|---|---|
| [CNC Kitchen: Stop printing flat: the 45° secret](https://cnckitchen.com/blog/stop-printing-flat-the-45-secret-for-stronger-parts) | Tração de PLA por orientação (63 MPa plano x 31 MPa em pé; 30/45/60°), adesão de camada ~50%. |
| [CNC Kitchen: Dicas de insertos térmicos](https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey) | Temperatura do ferro por material, furo reto, furo cego L+1 mm, furos impressos saem menores. |
| [CNC Kitchen Store: tabela "Dimensions & Design Guidelines"](https://cnckitchen.store/products/heat-set-insert-m3-x-5-7-100-pieces) | Ø do furo, comprimento e parede mínima de cada inserto CNC Kitchen (M2 a M10). |
| [HackSpace: Experiments with strong 3D prints](https://hackspace.raspberrypi.com/articles/experiments-with-strong-3d-prints) | Comparação perímetros x infill em flexão. |
| [Embedded Computing: 3D printed fasteners: inserts](https://www.embedded-computing.com/home-page/3d-printed-fasteners-part-1-inserts) | Resumo (secundário) dos testes de arrancamento/torque do CNC Kitchen com M3. |

## Insertos e fixadores

| Fonte | Para que serve |
|---|---|
| [Ruthex: página do inserto RX-M3x5.7 (tabela "Größe")](https://www.ruthex.de/en/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen) | Ø do furo (d3), comprimento e parede mínima de todos os insertos Ruthex. |
| [Ruthex: jogo de brocas para insertos](https://www.ruthex.de/en/products/ruthex-hss-bohrer-set-5-tlg-fur-gewindeeinsatze-m2-m2-5-m3-m4-m5-m6-din-338-bohrer-3-2-4-0-5-6-6-4-8-0-mm-fur-kunststoff-stahl-alu-kupfer-messing-uvm) | Confirma os diâmetros de furo 3,2 / 4,0 / 5,6 / 6,4 / 8,0 mm. |
| [EJOT DELTA PT Flyer](https://www.ejot.de/medias/sys_master/Industry_Flyer/Industry_Flyer/h11/hc7/9331662782494/EJOT-DELTA-PT-Flyer-08.23-en.pdf) e [Bossard DELTA PT](https://media.bossard.com/-/media/bossard-group/website/documents/brochures/brochures_products_english/delta-pt_en.pdf) | Furo piloto 0,8–0,88 x d para parafuso direto em termoplástico; dimensões de boss. |
| [fasten.it: ISO 4032](https://fasten.it/norms/norm/din_en_iso_4032), [ISO 4762](https://fasten.it/norms/norm/din_en_iso_4762), [ISO 7046-2](https://fasten.it/Norms/Norm/DIN_EN_ISO_7046_2) | Dimensões de porca sextavada, parafuso allen cilíndrico e escareado Phillips. |
| [Engineers Edge: ISO 10642](https://engineersedge.com/hardware/bs_en_iso_10642_14583.htm) | Diâmetro de cabeça do allen escareado. |
| [Optimas: Tapping sizes](https://optimas.com/technical-resources/tapping-sizes/), [AMES: Metric clearance hole chart](https://amesweb.info/Screws/Metric-Clearance-Hole-Chart.aspx), [Albany County Fasteners](https://www.albanycountyfasteners.com/media/6b/b8/g0/1764944339/clearance-hole-chart.pdf) | Furos passantes ISO 273 (fina/média/grossa = H12/H13/H14). |

## Guias de design de birôs e universidades

| Fonte | Para que serve |
|---|---|
| [Hubs: How to design parts for FDM](https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/) | Overhang 45°, ponte < 5 mm, pinos > 5 mm, furos horizontais, chanfro na base, anisotropia. |
| [Hubs: Dimensional accuracy](https://www.hubs.com/knowledge-base/dimensional-accuracy-3d-printed-parts/) | Tolerância +-0,5% (mín. +-0,5 mm) desktop, +-0,15% industrial, contração 0,2–1%. |
| [Hubs: Snap-fit joints](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) | Espessura >= 1 mm, largura >= 5 mm, filete >= 0,5h, folga FDM 0,5 mm, evitar braço em Z. |
| [Hubs: Threaded fasteners](https://www.hubs.com/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners/) | Rosca impressa não abaixo de M5; parede >= diâmetro do parafuso; insertos. |
| [UZH Additive Manufacturing: Design Guideline FDM (PDF)](https://www.amf.uzh.ch/dam/jcr:fd1ee024-1a98-488b-89ec-ffd85befa786/Design-Guideline-FDM.pdf) | Tabela compacta: paredes 1,0 mm, relevo 1,0 mm/fonte 14 pt, furo 2 mm, folga 0,5 mm, pino 3 mm, feature 2 mm. |
| [Hydra Research / AMIST (U. Louisville) cheat sheet](https://centers.louisville.edu/amist/amist-print-farm) | Ponte < 10 mm e outros mínimos FFF. |
| [Xometry: FDM design guide](https://xometry.pro/en/?p=22061) | Folga deslizante 0,2–0,3 mm; imprimir partes que encaixam na mesma orientação. |
| [Fictiv: How to design snap-fit components](https://www.fictiv.com/articles/how-to-design-snap-fit-components) e [Core77 (mesmo autor)](https://www.core77.com/posts/65318/how-to-design-snap-fit-components) | Folgas 0,2/0,3/0,4 mm por tipo de encaixe; deformação "aceitável" por material; redução de 50% para braço em Z. |

## Snap-fit (engenharia de plásticos)

| Fonte | Para que serve |
|---|---|
| [Bayer: Snap-Fit Joints for Plastics: A Design Guide (PDF)](https://fab.cba.mit.edu/classes/S62.12/people/vernelle.noel/Plastic_Snap_fit_design.pdf) | Fórmulas de deflexão (0,67 e 1,09 · ε · l²/h), força, deformação admissível por material, regra dos 60% para uso repetido. |
| [Machine Design: New equations make fastening plastic components a snap](https://www.machinedesign.com/archive/new-equations-make-fastening-plastic-components-snap) | Fórmula com fator Q e força de montagem com atrito e ângulo de entrada. |

## Temperatura em carro

| Fonte | Para que serve |
|---|---|
| [ASU News: Vanos et al., *Temperature* (2018)](https://news.asu.edu/20180516-discoveries-asu-study-hot-cars-can-hit-deadly-temperatures-within-one-hour) | Painel ~69 °C (157 °F) após 1 h ao sol; banco, volante, ar da cabine; sombra. |
| [Scripps/UC San Diego](https://scripps.ucsd.edu/news/research-highlight-hot-cars-can-hit-life-threatening-levels-approximately-one-hour) | Pico de painel > 165 °F (~74 °C). |
| [JJMIE (2022): temperatura em cabine estacionada](https://jjmie.hu.edu.jo/vol16-5/06-JJMIE-184-22.pdf) | Painel até 93 °C e ar interno até 74,8 °C sem sombra (clima quente). |

## Fontes secundárias / comunitárias (usadas só com aviso)

| Fonte | Para que serve |
|---|---|
| [Prusa Forum: Need advice on design tolerances](https://forum.prusa3d.com/forum/english-forum-general-discussion-announcements-and-releases/need-advice-on-design-tolerances/) | Faixas práticas de folga (0,1 justo / 0,2–0,25 normal / 0,3–0,4 folgado; print-in-place ~0,25). |
| [Prusa Forum: inserting magnets](https://forum.prusa3d.com/forum/how-do-i-print-this-printing-help/how-to-safely-insert-magnets-into-a-print) e [MakerWorld press-fit magnet](https://makerworld.com/models/2932423) | Folga para ímã por press-fit (+0,1–0,2 PLA, ~+0,3 PETG). |
| [MakerWorld: Tolerance & Fit Test](https://makerworld.com/en/models/2820462-tolerance-fit-test) | Modelo de teste e faixas press-fit (nominal) / justo (+0,1–0,2) / deslizante (>= +0,2). |
| [MakerWorld: X-Y Compensation Tool](https://makerworld.com/en/models/129893-x-y-compensation-tool) | Método para calibrar compensação X-Y no fatiador. |
| [Printables: Threaded insert hole tolerance test](https://printables.com/model/1040630-threaded-insert-hole-tolerance-test) | Teste de furos para inserto baseado nas medidas CNC Kitchen. |
| [3DJake: Outdoor-ready filaments](https://www.3djake.ch/en-CH/info/guide/outdoor-ready-filaments-for-weather-resistant-3d-prints) | Comparação qualitativa de UV entre PETG e ASA (varejista). |
| [Bambu Forum: PETG-CF HDT](https://forum.bambulab.com/t/bambu-petg-cf-low-hdt-compared-to-prusament/11609) | Divergência de HDT do PETG-CF entre Bambu (74 °C) e Prusament (96 °C). |
| [Fabbaloo: The new teardrop](https://www.fabbaloo.com/2011/12/the-new-teardrop-html) e [Meltio Design Guidelines](https://meltio3d.com/wp-content/uploads/2024/02/Meltio_Whitepapers_Design-Guidelines.pdf) | Técnica de furo em gota e gota truncada. |
