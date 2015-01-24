'''
########################################################################
# Misc Utilities
# by Vishang Shah (vishangshah.com)
# IMPORTANT : This tool is tested and works only with Houdini 14.
#
# Description : Miscellaneous Utilities to help with Houdini and Houdini Engine workflows.
#
	1. Add a Switch to selected node for debugging in Houdini Engine.
	2. 
#
#
# Usage : Copy the parent folder HOUtilities to [your houdini 14.0 installation]\houdini\python2.7libs\
#
To Do : Expose switch input to parent HDA or geometry's Parameters
To Do : Option to have an auto-Null input to switch op. Like "Switch to nothing" mode.
#
########################################################################
'''
# Import libraries
import os
import sys

import hou

from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtWebKit

from functools import partial

from . import Color
reload(Color)


class MiscUtilities(QFrame):
	def __init__(self, parent=None):
		'''
		Initialize MiscUtilities and create main layout.
		'''
		super(MiscUtilities, self).__init__(parent)

		# Global UI vars
		self.ui_button_width = 160
		self.ui_button_height = 40

		# Parent layout
		self.layout = QVBoxLayout(self)
		self.layout.setAlignment(Qt.AlignTop)
		# Set main layout
		self.setFixedLayout()

	def setFixedLayout(self):
		'''
		Create fixed layout.
		'''
		fixedLayout = QHBoxLayout()
		fixedLayout.setAlignment(Qt.AlignLeft)

		# Refresh HDAs
		btnSwitch = QPushButton("Add a Switch")
		btnSwitch.setMinimumWidth(self.ui_button_width)
		btnSwitch.setMaximumWidth(self.ui_button_width)
		btnSwitch.clicked.connect(partial(self.addSwitchForDebug, ""))
		fixedLayout.addWidget(btnSwitch)

		self.layout.addLayout(fixedLayout)

	def addSwitchForDebug(self, parentOp = ""):
		'''
		Add switch op to bypass selected node and expose switch input to the parent.
		'''
		
		currentSel = hou.selectedNodes()
		if len(currentSel) == 1:
			current = currentSel[0]
			opName = "switch"
			parentNode = hou.node(current.path()).parent()

			# Get inputs and outputs
			outNodes = current.outputs()
			inNodes = current.inputs()

			#Create switch
			newNode = current.createOutputNode(opName)
			newNode.setName(opName, True)
			newNode.setColor(Color.Default)

			# Set correct inputs to switch node
			if len(inNodes) > 0:
				newNode.setFirstInput(inNodes[0])
				newNode.setNextInput(current)

	
			# Insert switch between current and its immediate output node
			if len(outNodes) > 0:
				currentOut = outNodes[0]
				currentOut.setFirstInput(newNode)
			
			newNode.moveToGoodPosition()


