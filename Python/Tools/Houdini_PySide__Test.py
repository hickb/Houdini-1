
# Houdini-PySide Test
# A small test learned/copied from Youtube user vuxster.

# A floating toolbar for commonly used SOPs

import hou
from PySide import QtCore as qtc
from PySide import QtGui as qtg
from functools import partial

#-------------------------------------------------------------------

try:    app = qtg.QApplication(['houdini'])
except: app = qtg.QApplication.instance()

eventLoop = qtc.QEventLoop()

def qt_callback():
    if not ctl.isVisible():
        try:    hou.ui.removeEventLoopCallback(qt_callback)
        except: pass
    eventLoop.processEvents()
    app.sendPostedEvents(None, 0)
#-------------------------------------------------------------------
ctl = None
def show(ctl_):
    global ctl
    ctl = ctl_
    ctl.show()
    hou.ui.addEventLoopCallback(qt_callback)
#-------------------------------------------------------------------
def create_sop(sopName = "null"):
    selAll = hou.selectedNodes()
    if len(selAll) > 0:
        s = selAll[0]
        sel = hou.node(s.path())
        p = hou.node(s.path()).parent()
        
        o = p.createNode(sopName)
        o.setName(sopName, True)
        c = hou.Color()
        c.setRGB([0,1,0])
        #o.setColor(c)
        o.setCurrent(True, True)
        try:
            o.setFirstInput(sel)
        except:
            pass
        o.moveToGoodPosition()
    
        o.setDisplayFlag(True)
        o.setRenderFlag(True)


widget = qtg.QFrame()
widget.setFrameShape(qtg.QFrame.StyledPanel)
wsize = qtc.QSize(400,200)
#wsize.setWidth(400,200)
#widget.sizeHint(wsize)
widget.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)

#widget.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)
layout = qtg.QVBoxLayout(widget)

#-------------------------------------------------------------------
sops = []
sops.append("null")
sops.append("group")
sops.append("merge")
sops.append("xform")
sops.append("box")
sops.append("grid")
sops.append("skin")
sops.append("circle")
sops.append("facet")
sops.append("carve")

#-------------------------------------------------------------------

for i in range(0, len(sops)):
    sop = sops[i]
    b = qtg.QPushButton("Create " + sop, widget)
    if i < 4:  
        b.setStyleSheet('QPushButton {background-color: blue; color: yellow}')
    b.clicked.connect(partial(create_sop,sop))
    layout.addWidget(b)

b2 = qtg.QPushButton("Close", widget)
b2.clicked.connect(widget.hide)
layout.addWidget(b2)

show(widget)

