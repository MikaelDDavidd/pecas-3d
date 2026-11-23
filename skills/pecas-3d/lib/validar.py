# Rodado pelo `p3d validar arquivo.FCStd [--exportar]`. Reabre o projeto (por exemplo depois
# de mudar a planilha na tela), recalcula e passa todas as checagens de lib/validacao.py.
# Com --exportar, refaz STEP e STL na pasta do arquivo (o .FCStd não é regravado).
import os
import sys

import FreeCAD as App

import validacao

if len(sys.argv) < 2:
    raise SystemExit("uso: p3d validar arquivo.FCStd [--exportar]")
arq = sys.argv[1]
exportar = "--exportar" in sys.argv[2:]
doc = App.openDocument(arq)
doc.recompute()
nome = os.path.splitext(os.path.basename(arq))[0]
ok = validacao.conferir(doc, pasta_saida=os.path.dirname(arq) if exportar else None, nome=nome, salvar=False)
raise SystemExit(0 if ok else 1)
