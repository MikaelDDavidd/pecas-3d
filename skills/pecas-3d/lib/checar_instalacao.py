# Rodado pelo `p3d setup`: confere se o FreeCAD tem o que a lib usa.
import FreeCAD as App
import Import  # noqa: F401
import Mesh  # noqa: F401
import MeshPart  # noqa: F401
import Part  # noqa: F401
import Sketcher  # noqa: F401
import numpy

doc = App.newDocument("Checagem")
doc.addObject("PartDesign::Body", "Corpo")
m = doc.addObject("Spreadsheet::Sheet", "Medidas")
m.set("A1", "10 mm")
m.setAlias("A1", "lado")
doc.recompute()
assert abs(m.evalExpression("Medidas.lado").Value - 10) < 1e-9
App.closeDocument(doc.Name)

try:
    from InvoluteGearFeature import _InvoluteGear  # noqa: F401
except ImportError:
    print("AVISO engrenagem evolvente indisponível nesta versão (só o exemplo de engrenagem usa)")
print(f"MODULOS_OK numpy {numpy.__version__}")
