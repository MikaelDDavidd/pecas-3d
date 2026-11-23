# Materiais para FDM

Escolha de filamento por temperatura de uso, resistência, UV, flexibilidade e dificuldade.
Números de laboratório vêm do **Bambu Lab Filament Guide** (mesma metodologia para todos os materiais, o que permite comparar) e da **Prusa Knowledge Base**. Valores mudam por marca: para peça crítica, conferir o TDS (technical data sheet) do filamento comprado.

---

## 0. Decisão rápida

| Situação | Material padrão | Alternativa |
|---|---|---|
| Protótipo, peça de mesa, organizador, gabarito interno | **PLA** | PETG |
| Peça funcional dentro de casa (suporte, clipe, caixa de eletrônica) | **PETG** | PLA se não esquentar |
| **Peça para dentro de carro** | **ASA** | PETG só em área sempre na sombra; PC/PA-CF para painel com carga |
| Peça externa (sol + chuva) | **ASA** | PETG por tempo limitado |
| Peça flexível (amortecedor, pé, vedação, capa) | **TPU 95A** | - |
| Engrenagem, peça com desgaste/atrito, alta temperatura | **PA (nylon) / PA-CF** | PC |
| Rigidez máxima com pouco peso | **PET-CF / PA-CF** | PLA-CF (rígido, mas mesma temperatura do PLA) |
| Perto de motor/fonte quente (> 100 °C) | **PC** ou **PA-CF / PET-CF** | - |

---

## 1. Tabela comparativa (Bambu Lab Filament Guide)

Fonte de todas as colunas numéricas: [Bambu Filament Guide (PDF)](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf). A coluna "PETG" do guia corresponde ao PETG HF da Bambu.

| Material | HDT @0,45 MPa | Flexão XY (resist.) | Módulo flexão XY | Impacto XY | Impacto Z (adesão de camada) | Absorção água | Secagem obrigatória | Bico (°C) |
|---|---|---|---|---|---|---|---|---|
| PLA | **57 °C** | 76 MPa | 2750 MPa | 26,6 kJ/m² | 13,8 | 0,43% | opcional | 190–230 |
| PETG | **69 °C** | 65 MPa | 1670 MPa | 52,7 | 13,6 | 0,32% | opcional | 240–270 |
| ABS | **87 °C** | 62 MPa | 1880 MPa | 39,3 | 7,4 | 0,65% | opcional | 240–280 |
| ASA | **100 °C** | 65 MPa | 1920 MPa | 41,0 | 4,9 | 0,45% | opcional | 240–280 |
| PC | **117 °C** | 108 MPa | 2310 MPa | 34,8 | 9,0 | 0,25% | **sim** | 260–290 |
| TPU 95A | n/d | n/d | n/d | 125,2 | 88,7 | 1,16% | **sim** | 220–240 |
| PLA-CF | 55 °C | 89 MPa | 3950 MPa | 23,2 | 7,8 | 0,42% | opcional | 210–240 |
| PETG-CF | 74 °C | 70 MPa | 2910 MPa | 41,2 | 10,7 | 0,30% | opcional | 240–270 |
| PET-CF | **205 °C** | 131 MPa | 5320 MPa | 36,0 | 4,5 | 0,37% | **sim** | 260–300 |
| PAHT-CF | **194 °C** | 125 MPa | 4230 MPa | 57,5 | 13,3 | 0,88% | **sim** | 260–300 |
| PA6-CF | **184 °C** | 151 MPa | 5460 MPa | 40,3 | 15,5 | 2,35% | **sim** | 260–300 |

Como ler:
- **HDT** (heat deflection temperature) a 0,45 MPa = temperatura em que o corpo de prova deforma sob carga leve. É o melhor número único para "até que temperatura a peça aguenta". Sob carga constante (parafuso apertado, peso pendurado), a peça já flui (creep) **abaixo** do HDT: deixar margem de 15–20 °C.
- **Impacto Z** é o retrato da adesão entre camadas: ASA e PET-CF são ótimos no plano e fracos entre camadas.
- Compostos CF exigem **bico de aço endurecido** (hardened steel); o guia recomenda bico 0,6 mm para PET-CF/PA-CF ([Bambu Filament Guide](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf)).

---

## 2. Fichas por material

### PLA
| Item | Valor | Fonte |
|---|---|---|
| Temperatura de uso | "gets soft and deforms at temperatures over 60 °C"; HDT 57 °C | [Prusa KB](https://help.prusa3d.com/article/pla_2062), [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| UV | degrada sob UV | [Prusa KB](https://help.prusa3d.com/article/pla_2062) |
| Impacto | ruim; quebra ao longo das camadas ou em estilhaços | [Prusa KB](https://help.prusa3d.com/article/pla_2062) |
| Dificuldade | "one of the easiest materials to print" | [Prusa KB](https://help.prusa3d.com/article/pla_2062) |
| Impressão (Prusament) | bico 215/210 °C, mesa 60 °C | [Prusa KB](https://help.prusa3d.com/article/pla_2062) |
| Uso típico | modelos conceituais, protótipos, brinquedos de baixo desgaste; "not suitable for technical and outdoor use" | [Prusa KB](https://help.prusa3d.com/article/pla_2062) |

Rígido (maior módulo entre os não-CF), mas frágil. Ruim para snap-fit e dobradiça viva.

### PETG
| Item | Valor | Fonte |
|---|---|---|
| Temperatura de uso | uso externo "below 80 °C" (Prusa); HDT 69 °C (Bambu) | [Prusa KB](https://help.prusa3d.com/article/petg_2059), [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| Impacto | "Tough and durable"; maior impacto XY entre os rígidos (52,7 kJ/m²) | [Prusa KB](https://help.prusa3d.com/article/petg_2059), [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| UV | resistência UV limitada (amarela/perde ductilidade com o tempo); ASA é muito superior | [3DJake guia outdoor](https://www.3djake.ch/en-CH/info/guide/outdoor-ready-filaments-for-weather-resistant-3d-prints) (fonte secundária) |
| Dificuldade | fácil; adequado a iniciantes | [Prusa KB](https://help.prusa3d.com/article/petg_2059) |
| Impressão (Prusament) | bico 230/240 °C, mesa 85/90 °C | [Prusa KB](https://help.prusa3d.com/article/petg_2059) |
| Uso típico | peças mecânicas, suportes, braçadeiras, peças estanques, caixas de eletrônica | [Prusa KB](https://help.prusa3d.com/article/petg_2059) |

Divergência: Prusa fala em "até 80 °C"; HDT medido da Bambu é 69 °C. **Projeto adota 65 °C como limite prático do PETG** (com carga, menos).

### ABS
| Item | Valor | Fonte |
|---|---|---|
| Temperatura de uso | HDT 87 °C; "good high-temperature resistance" | [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf), [Prusa KB](https://help.prusa3d.com/article/abs_2058) |
| UV | "Lacks UV resistance (unlike ASA)"; amarela e fica quebradiço ao ar livre | [Prusa KB](https://help.prusa3d.com/article/abs_2058) |
| Dificuldade | empena muito; **exige impressora fechada (enclosure)**; contração ~1–2%; fumos de estireno | [Prusa KB](https://help.prusa3d.com/article/abs_2058) |
| Impressão | bico 255 °C, mesa 100 °C (80–110) | [Prusa KB](https://help.prusa3d.com/article/abs_2058) |
| Uso típico | peças técnicas baratas com calor e esforço; peças alisadas com acetona | [Prusa KB](https://help.prusa3d.com/article/abs_2058) |

Para o projeto: **ASA substitui ABS** em quase tudo (mesma impressão, com UV).

### ASA
| Item | Valor | Fonte |
|---|---|---|
| Temperatura de uso | "up to 93 °C" (Prusa); HDT 100 °C (Bambu) | [Prusa KB](https://help.prusa3d.com/article/asa_1809), [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| UV | resistente a UV, mais que ABS | [Prusa KB](https://help.prusa3d.com/article/asa_1809) |
| Impacto | alto impacto e resistência ao desgaste | [Prusa KB](https://help.prusa3d.com/article/asa_1809) |
| Dificuldade | empena bastante; enclosure recomendado ("necessary for printing large parts") | [Prusa KB](https://help.prusa3d.com/article/asa_1809) |
| Impressão | bico 260 °C, mesa 105/110 °C | [Prusa KB](https://help.prusa3d.com/article/asa_1809) |
| Uso típico | peças técnicas e **externas** | [Prusa KB](https://help.prusa3d.com/article/asa_1809) |

Ponto fraco: adesão entre camadas (impacto Z 4,9 kJ/m², o menor da tabela) → orientar com cuidado, evitar cargas que separem camadas, impressora fechada e pouca ventilação.

### TPU (flexível)
| Item | Valor | Fonte |
|---|---|---|
| Dureza | 60A–90A Shore (o mais comum para FDM é 95A) | [Prusa KB](https://help.prusa3d.com/article/flexible-materials_2057) |
| Impressão | bico 230–245 °C, mesa 60–75 °C; velocidade ~20 mm/s, máx 30–40 mm/s | [Prusa KB](https://help.prusa3d.com/article/flexible-materials_2057) |
| Dificuldade | alta (entupimento, ponte ruim, fiapos): mais fácil em extrusora direct drive | [Prusa KB](https://help.prusa3d.com/article/flexible-materials_2057) |
| Projeto | menos perímetros/topo = mais flexível; mais perímetros/infill = mais firme | [Prusa KB](https://help.prusa3d.com/article/flexible-materials_2057) |
| Uso típico | arruelas espaçadoras, pneus de RC, solas, correias, amortecedores | [Prusa KB](https://help.prusa3d.com/article/flexible-materials_2057) |

Adesão entre camadas excelente (impacto Z 88,7 kJ/m²: [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf)). Secar antes de usar.

### PA (nylon)
| Item | Valor | Fonte |
|---|---|---|
| Temperatura de uso | "excellent thermal and mechanical resistance"; PA-CF com HDT 184–194 °C | [Prusa KB](https://help.prusa3d.com/article/nylon-pa_167188), [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| Umidade | higroscópico; pode absorver até 10% do peso em água; secar >= 4 h abaixo de 90 °C | [Prusa KB](https://help.prusa3d.com/article/nylon-pa_167188) |
| Dificuldade | "very hard to print", só para experientes; empena; enclosure ajuda | [Prusa KB](https://help.prusa3d.com/article/nylon-pa_167188) |
| Impressão | bico 285 °C, mesa 110 °C | [Prusa KB](https://help.prusa3d.com/article/nylon-pa_167188) |
| Uso típico | peças técnicas com calor, química e esforço; resistente à abrasão; flexível em parede fina | [Prusa KB](https://help.prusa3d.com/article/nylon-pa_167188) |

Melhor material para snap-fit, engrenagem e dobradiça viva. PA-CF (com fibra) é bem mais fácil de imprimir que PA puro e não empena tanto.

### PC (policarbonato)
| Item | Valor | Fonte |
|---|---|---|
| Temperatura de uso | HDT 117 °C | [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| Resistência | "High impact tenacity and tensile strength"; maior resistência à flexão entre não-CF (108 MPa) | [Prusa KB](https://help.prusa3d.com/article/polycarbonate-pc_165812), [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| Dificuldade | PC puro "very hard to print"; PC Blend bem mais fácil; empena, enclosure ajuda | [Prusa KB](https://help.prusa3d.com/article/polycarbonate-pc_165812) |
| Impressão | bico 275 °C, mesa 110/115 °C | [Prusa KB](https://help.prusa3d.com/article/polycarbonate-pc_165812) |
| Uso típico | peças técnicas com calor e esforço mecânico (ex.: dutos de ventoinha) | [Prusa KB](https://help.prusa3d.com/article/polycarbonate-pc_165812) |

UV: a Prusa não informa; PC comum amarela ao sol sem aditivo UV (não confirmado em fonte desta pesquisa).

### Compostos com fibra de carbono (CF)
- **PLA-CF**: mais rígido que PLA (módulo 3950 MPa), mas **mesma temperatura** (HDT 55 °C) e menor impacto. Não resolve calor.
- **PETG-CF**: HDT 74 °C (Bambu): a Prusament declara 96 °C para o PETG-CF dela, divergência discutida no [fórum da Bambu](https://forum.bambulab.com/t/bambu-petg-cf-low-hdt-compared-to-prusament/11609). Usar o TDS da marca comprada.
- **PET-CF / PAHT-CF / PA6-CF**: HDT 184–205 °C, rigidez alta; exigem secagem e bico de aço endurecido. Adesão entre camadas variável (PET-CF fraco em Z).
- Todos: bico de aço endurecido; fibra deixa a peça mais "fosca" e esconde camadas.

---

## 3. Peça para dentro de CARRO no sol (Brasil)

### Quanto esquenta

| Medição | Sol direto (1 h) | Sombra (1 h) | Fonte |
|---|---|---|---|
| Painel (dashboard), média | **157 °F ≈ 69 °C** | 118 °F ≈ 48 °C | [Vanos et al., *Temperature* (2018), via ASU](https://news.asu.edu/20180516-discoveries-asu-study-hot-cars-can-hit-deadly-temperatures-within-one-hour) |
| Painel, pico | > 165 °F ≈ **74 °C** | - | [Scripps/UC San Diego](https://scripps.ucsd.edu/news/research-highlight-hot-cars-can-hit-life-threatening-levels-approximately-one-hour) |
| Volante | 127 °F ≈ 53 °C | 107 °F ≈ 42 °C | ASU (mesmo estudo) |
| Banco | 123 °F ≈ 51 °C | 105 °F ≈ 41 °C | ASU |
| Ar da cabine | 116 °F ≈ 47 °C | ~100 °F ≈ 38 °C | ASU |
| Painel, carro estacionado sem sombra (Iraque) | até **93 °C**; ar interno até 74,8 °C | - | [JJMIE 2022](https://jjmie.hu.edu.jo/vol16-5/06-JJMIE-184-22.pdf) |

O estudo da ASU foi feito em Tempe (Arizona) em dias de verão com ar acima de ~38 °C (100 °F). Não foi encontrado estudo equivalente medido no Brasil; um carro escuro estacionado ao sol do verão do Nordeste/Centro-Oeste deve ficar na mesma faixa (inferência, não medição).

### Comparação com os materiais

| Material | HDT | Painel ao sol (69–93 °C) | Cabine na sombra / porta-objetos (38–53 °C) |
|---|---|---|---|
| PLA | 57 °C | **deforma** | marginal (pode fluir sob carga; não usar) |
| PETG | 69 °C | **não usar** (HDT = temperatura média do painel) | aceitável |
| ABS | 87 °C | aceitável até ~85 °C; sem UV, amarela | ok |
| **ASA** | **100 °C** | **recomendado** (calor + UV) | ok |
| PC | 117 °C | ok (verificar UV) | ok |
| PA-CF / PET-CF | 184–205 °C | ok, margem grande | ok |

A Prusa diz que PLA "gets soft and deforms at temperatures over 60 °C" ([Prusa KB](https://help.prusa3d.com/article/pla_2062)): abaixo do que o painel atinge em 1 hora de sol.

**Regra do projeto para carro:**
1. **Padrão: ASA**, com impressora fechada.
2. **PETG** só para peça que nunca pega sol direto e não fica sobre o painel (ex.: dentro do porta-luvas, embaixo do banco, console coberto).
3. **PLA: nunca** dentro de carro.
4. Peça no painel/para-brisa **com carga** (suporte de celular com ímã, peso pendurado): PC ou PA-CF/PET-CF; ASA no limite.
5. Preferir **cor clara** em peça exposta ao sol (absorve menos radiação: princípio físico geral, não medido nesta pesquisa).
6. Ímã de neodímio comum perde força acima de ~80 °C (ver fixacao.md).

---

## 4. Recozimento (annealing): aumenta resistência térmica

O guia da Bambu lista recozimento pós-impressão para vários materiais (PLA 50–60 °C; ABS e ASA 80–90 °C; PC 85–100 °C; PET-CF, PAHT-CF e PA6-CF 90–130 °C; sempre 6–12 h; PETG e TPU sem recozimento) ([Bambu Filament Guide](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf)). Recozer muda dimensões (contração/empenamento): **não é recomendado para peça com tolerância** sem testar antes. O projeto não depende de recozimento; escolher o material certo.

---

## 5. Secagem

| Material | Condição (estufa) | Fonte |
|---|---|---|
| PLA | 55 °C, 8 h (opcional) | [Bambu](https://cdn1.bambulab.com/filament/a5e185aed14e6/filament-guide-en-4.pdf) |
| PETG | 65 °C, 8 h (opcional) | idem |
| ABS / ASA / PC | 80 °C, 8 h | idem |
| TPU | 70 °C, 8 h (obrigatória) | idem |
| PA / PA-CF / PET-CF | 80 °C, 8–12 h (obrigatória) | idem |
| Nylon (Prusa) | >= 4 h abaixo de 90 °C | [Prusa KB](https://help.prusa3d.com/article/nylon-pa_167188) |

Filamento úmido: estalos no bico, fiapos, bolhas e perda de resistência.
