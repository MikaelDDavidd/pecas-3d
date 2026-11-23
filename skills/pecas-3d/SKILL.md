---
name: pecas-3d
description: Projeta, altera, valida e abre peças para impressão 3D FDM como projeto nativo do FreeCAD com árvore editável (corpo do PartDesign, esboços restritos, medidas numa planilha), exportando STL e STEP. macOS e Linux. Use quando pedirem para criar, desenhar, modelar ou ajustar uma peça, suporte, encaixe, caixa, tampa, engrenagem ou adaptador para imprimir, para validar ou reexportar um .FCStd depois de mexer na planilha, ou para abrir uma peça no FreeCAD.
---

# Peças 3D no FreeCAD

Cada peça sai como projeto nativo do FreeCAD: um corpo do PartDesign por peça impressa, esboços com 0 grau de liberdade e toda medida na planilha `Medidas`. Quem abrir no FreeCAD muda a medida na planilha, aperta Ctrl+R e a peça se refaz.

Tudo passa pelo `scripts/p3d` desta skill. Chame sempre pelo caminho absoluto, com `bash` na frente (o bit de execução pode se perder num zip): `bash <pasta da skill>/scripts/p3d ...`. Abaixo, `p3d` abrevia isso.

## 0. Primeira vez na máquina

Rode `p3d diagnostico`. Se a config não existe, **pergunte antes** de rodar o setup:

- **Linux**: o setup baixa o FreeCAD 1.1.4 oficial (AppImage, ~800 MB, ocupa ~3 GB em `~/.local/share/pecas-3d`), confere o SHA256 fixo no script e extrai sem sudo.
- **macOS**: o setup só acha o FreeCAD. Se não houver, peça ao usuário para instalar (`brew install --cask freecad` ou o .dmg de freecad.org) e rode o setup de novo.

```bash
p3d setup     # rodar em segundo plano ou com timeout de 600000 ms: o download passa de 2 min
p3d testar    # tem que terminar em TODOS_OK
```

O setup termina em `SETUP_OK FreeCAD <versão>`. Qualquer outro final: mostre a saída de `p3d diagnostico`. Download interrompido continua de onde parou ao rodar o setup de novo.

## 1. Entender a peça

Pergunte só o que faltar, numa pergunta curta e com sugestão:

- **O que encaixa nela**: medidas reais (paquímetro ou foto com régua). Sem medida, proponha um valor como parâmetro, escreva `MEDIR` no comentário e avise na entrega. Não chute.
- **Uso e ambiente**: carga, calor, sol, água. Decide o material.
- **Fixação**: parafuso, porca, inserto, ímã, encaixe, abraçadeira.
- **Tamanho**: cabe na mesa da impressora? Se não, dividir em partes com encaixe.

Os números vêm dos docs, não da memória:

| Assunto | Arquivo |
|---|---|
| Paredes, overhang, pontes, orientação | `docs/design-fdm.md` |
| Folgas e encaixes | `docs/tolerancias-encaixes.md` |
| Parafusos, porcas, insertos, ímãs | `docs/fixacao.md` |
| Materiais | `docs/materiais.md` |
| Fatiador | `docs/fatiamento.md` |
| API do FreeCAD por script e pegadinhas (seção 8: árvore) | `docs/freecad-python.md` |

Resumo para bico de 0,4 mm: parede funcional de 4 perímetros (~1,7 mm), mínimo 0,9 mm; folga diametral de 0,4 mm em encaixe deslizante e 0,2 mm em justo; furo vertical +0,15 mm; furo horizontal acima de 5 mm em gota; overhang até 45 graus; ponte até 10 mm; carga e clipes no plano XY. Peça no sol: ASA. PETG só na sombra. PLA nunca em carro ou ao ar livre.

## 2. Modelar

```bash
p3d nova <nome-em-kebab> <pasta do projeto do usuário>
```

Cria `<pasta>/<nome>/peca.py` a partir de `exemplos/modelo-peca.py`. Nunca crie peças dentro da pasta da skill. Ao editar:

- Dicionário `P` no topo com um comentário por medida: vira a planilha `Medidas` e aceita `param=valor` na linha de comando. Nenhum número solto na geometria, exceto 0.
- Um corpo do PartDesign por peça impressa. Esboços com `arvore.esboco` e cotas ligadas à planilha (`arvore.retangulo`, `circulo`, `poligono`). Features com nome do que fazem (`FuroDoParafuso`, não `Pocket001`).
- `arvore.recomputar(doc, "etapa")` depois de cada bloco. `arvore.cor(peca, "RRGGBB")` em cada peça impressa: é assim que a validação acha as peças.
- Modelar na orientação de impressão, face maior em Z=0.
- Terminar com `validacao.conferir(doc, pasta_saida=SAIDA, nome=NOME)`, como no modelo.

Ajudantes: `lib/arvore.py` (árvore) e `lib/pecas3d.py` (porca, inserto, furo em gota, chanfro). Exemplos completos: `exemplos/regua-folgas/` (pinos print-in-place, texto gravado) e `exemplos/engrenagem-registro/` (engrenagens evolventes, furo em D, checagens próprias passadas para `conferir`).

## 3. Gerar e validar

```bash
p3d gerar <pasta>/<nome>/peca.py [param=valor ...]      # peça grande pode levar 1-2 min: timeout 600000 ms
p3d render <pasta>/<nome>/saida/<nome>.stl               # PNG ao lado do STL, vista iso
p3d render <pasta>/<nome>/saida/<nome>.stl <outro>.png E07A2F tras
```

O `gerar` imprime `[ok]` ou `[FALHOU]` por checagem e termina em `VALIDACAO_OK` ou `VALIDACAO_FALHOU`:

- recálculo sem erro e peças achadas;
- todo esboço com 0 grau de liberdade;
- cada peça um sólido válido, apoiado em Z=0, sem invadir as outras;
- 5 medidas da planilha mudadas em +5%, recálculo válido e valores de volta;
- STL fechado, sem non-manifold e sem auto-interseção (um com tudo e um por peça).

A peça só está pronta com `VALIDACAO_OK`. Depois abra os PNGs e confira a forma.

Antes de entregar, revise o `peca.py` contra os docs (ou peça isso a um subagente). Para cada problema: onde, por que importa e a correção com número.

1. Paredes e nervuras em múltiplos da largura de linha.
2. A carga principal não pode puxar camadas (eixo Z).
3. Overhang acima de 45 graus, ponte longa, furo horizontal sem gota.
4. Folgas e furos de parafuso, porca e inserto conforme as tabelas.
5. Material adequado ao uso.
6. Medida solta no código ou estimativa sem `MEDIR`.

## 4. Abrir e entregar

```bash
p3d abrir <pasta>/<nome>/saida/<nome>.FCStd
```

Abra no fim se a sessão tiver tela. `ABERTO` = janela aberta com cores, vista isométrica e árvore expandida. `SEM_TELA` (sessão SSH ou servidor) = só informe o caminho do arquivo. No macOS, se a janela não aparecer, é o pedido de acesso à pasta, que o usuário libera em Ajustes, Privacidade e Segurança.

Escreva `<pasta>/<nome>/README.md`: para que serve, medidas principais, medidas `MEDIR`, material e por quê, orientação, fatiador (paredes, preenchimento, suporte), como regenerar e quais medidas da planilha mexer.

Na resposta: preview, medidas principais, material, orientação, fatiador, caminho do STL, medidas a conferir e o que pede peça de teste.

## Depois de editar na tela

```bash
p3d validar <arquivo>.FCStd --exportar    # confere de novo e refaz STL e STEP
```

## Segurança

`p3d gerar` executa o script Python com as permissões do usuário, e um .FCStd pode trazer objetos com código. Se o `peca.py` ou o .FCStd veio de outra pessoa, leia antes de rodar ou abrir.

## Problemas comuns

| Sintoma | Saída |
|---|---|
| `FreeCAD ainda não configurado` | rodar `p3d setup` (com o ok do usuário) |
| `ignorando FreeCAD 0.x` | versão antiga da distro; o setup instala o 1.1.4 |
| `download falhou` | rodar `p3d setup` de novo: continua de onde parou |
| `passou de N s` | script lento ou travado; `P3D_TIMEOUT=3600` aumenta |
| `Invalid alias` | alias da planilha com nome de unidade (`h`, `w`, `r`, `m`, `s`, `g`): usar nome por extenso |
| esboço com grau de liberdade | faltou cota; usar os ajudantes de `lib/arvore.py` |
| `abrir` fecha logo no Linux | ver `~/.local/share/pecas-3d/abrir.log` (costuma ser OpenGL) |
| Windows | não suportado; usar WSL2 com Ubuntu |

Scripts de peça importam `FreeCAD`: rodam só com `p3d gerar`, nunca com `python3`.
