"""Aparência ao abrir uma peça no FreeCAD com janela. Só mexe na tela: não recalcula.

O freecadcmd não grava cor. As peças guardam a cor na propriedade `Cor` (hex), posta
por arvore.cor(); este script pinta, mostra a vista isométrica e enquadra.
Rodado pelo `p3d abrir`:  FreeCAD arquivo.FCStd lib/aparencia.py
"""

import sys

import FreeCAD as App
import FreeCADGui as Gui


def rgb(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4))


doc = App.ActiveDocument
if doc is None:
    raise RuntimeError("Abra o .FCStd antes.")
for o in doc.Objects:
    if "Cor" in o.PropertiesList and o.ViewObject is not None:
        material = App.Material(DiffuseColor=rgb(o.Cor))
        o.ViewObject.ShapeAppearance = material
        o.ViewObject.Visibility = True
        # Corpo do PartDesign mostra a feature da ponta (Tip): ela é que aparece na tela.
        if o.TypeId == "PartDesign::Body" and o.Tip is not None:
            for f in o.Group:
                if f.isDerivedFrom("PartDesign::Feature") and f.ViewObject is not None:
                    f.ViewObject.Visibility = f is o.Tip
            o.Tip.ViewObject.ShapeAppearance = material
    if o.TypeId == "App::DocumentObjectGroup" and o.ViewObject is not None:
        o.ViewObject.Visibility = True

# A página Iniciar abre por cima do documento depois que este script roda, então a
# arrumação final roda de novo com atraso: traz a vista 3D para a frente, abre a
# árvore até as features de cada corpo e enquadra.
try:
    from PySide import QtCore, QtWidgets
except ImportError:
    from PySide import QtCore, QtGui as QtWidgets


def finalizar():
    janela = Gui.getMainWindow()
    if sys.platform.startswith("linux") and not janela.isMaximized():
        janela.showMaximized()  # no Linux a janela abre pequena
    area = janela.findChild(QtWidgets.QMdiArea)
    if area is not None:
        for sub in area.subWindowList():
            if sub.windowTitle().startswith(doc.Label):
                area.setActiveSubWindow(sub)
    for arvore in janela.findChildren(QtWidgets.QTreeWidget):
        arvore.expandToDepth(2)
    vista = Gui.getDocument(doc.Name).activeView()
    vista.viewIsometric()
    vista.fitAll()
    try:
        Gui.getDocument(doc.Name).Modified = False  # só a tela mudou: fechar sem perguntar
    except Exception:
        pass


finalizar()
for atraso in (1500, 4000):
    QtCore.QTimer.singleShot(atraso, finalizar)
