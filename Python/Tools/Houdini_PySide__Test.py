# Houdini-PySide Test
# A small test learned/copied from Youtube user vuxster.

import hou
from PySide import QtCore as qtc
from PySide import QtGui as qtg

#

try:    app = qtg.QApplication(['houdini'])
except: app = qtg.QApplication.instance()

eventLoop = qtc.QEventLoop()

def qt_callback():
    if not ctl.isVisible():
        try:    hou.ui.removeEventLoopCallback(qt_callback)
        except: pass
    eventLoop.processEvents()
    app.sendPostedEvents(None, 0)

ctl = None
def show(ctl_):
    global ctl
    ctl = ctl_
    ctl.show()
    hou.ui.addEventLoopCallback(qt_callback)

def create_box():
        hou.node("/obj").createNode("geo").createNode("box")

'''
button_widget = qtg.QPushButton("Hello")
button_widget.clicked.connect(button_widget.hide)
button_widget.setWindowFlags(qtc.Qt.FramelessWindowHint | qtc.Qt.WindowStaysOnTopHint)
show(button_widget)
'''

widget = qtg.QFrame()
widget.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
layout = qtg.QVBoxLayout(widget)

b1 = qtg.QPushButton("Create Box", widget)
b2 = qtg.QPushButton("Close", widget)

b1.clicked.connect(create_box)
b2.clicked.connect(widget.hide)

layout.addWidget(b1)
layout.addWidget(b2)

show(widget)
