# Roda dentro do freecadcmd, chamado pelo `p3d gerar`. Não chamar direto.
# Lê o script e os argumentos de variáveis de ambiente (o freecadcmd tenta abrir
# como arquivo qualquer argumento extra da linha de comando), monta sys.argv,
# roda o script como __main__ e sai com os._exit(code) para o exit code chegar ao shell.
import os
import runpy
import sys
import traceback

# Sem locale UTF-8 (LC_CTYPE=C) o stdout do freecadcmd é ASCII e print com acento quebra.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

script = os.environ["FCAD_SCRIPT"]
args = [os.environ[f"FCAD_ARG_{i}"] for i in range(int(os.environ.get("FCAD_ARGC", "0")))]
lib = os.environ.get("FCAD_LIB")

sys.argv = [script] + args
# A lib entra por último na frente: um arvore.py na pasta da peça não pode substituí-la.
for p in (os.path.dirname(script), lib):
    if p:
        if p in sys.path:
            sys.path.remove(p)
        sys.path.insert(0, p)

code = 0
try:
    runpy.run_path(script, run_name="__main__")
except SystemExit as exc:
    c = exc.code
    code = c if isinstance(c, int) else (0 if c is None else 1)
    if c is not None and not isinstance(c, int):
        print(c, file=sys.stderr)
except BaseException:
    traceback.print_exc()
    code = 1
finally:
    sys.stdout.flush()
    sys.stderr.flush()
os._exit(code)
