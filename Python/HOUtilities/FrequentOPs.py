########################################################################
# Frequent OPs
# by Vishang Shah (vishangshah.com)
# IMPORTANT : This tool is tested and works only with Houdini 14, due to PySide support.
#
# Description : Provides an interface for quick access to frequently used OPs
#
# Usage : Copy the folder Frequent_OPs to [your houdini 14.0 installation]\houdini\python2.7libs\
#
########################################################################

# Import libraries
import os
import sys
import json

import hou

from PySide import QtCore, QtGui, QtWebKit
from functools import partial

from . import Color

reload(Color)

# Reload

# HDAManager
class FrequentOPs(QtGui.QFrame):
	def __init__(self, parent=None):
		super(FrequentOPs, self).__init__(parent)

		# all HDAs in current houdini file
		self.opNames = []

		# UI vars
		self.ui_button_width = 120
		self.ui_button_height = 40

		# Main Layout
		self.mainLayout = QtGui.QHBoxLayout()
		self.setLayout(self.mainLayout)

		#helloWidget = QtGui.QLabel('Frequent OPs')
		#self.mainLayout.addWidget(helloWidget)
		
		self.refreshOpNames()


	def listOpNames(self):
		self.opNames = []
		self.opNames.append("null")
		self.opNames.append("group")
		self.opNames.append("merge")
		self.opNames.append("xform")
		self.opNames.append("-")
		self.opNames.append("curve")
		self.opNames.append("grid")
		self.opNames.append("box")
		self.opNames.append("-")
		self.opNames.append("resample")
		self.opNames.append("carve")
		self.opNames.append("facet")
		self.opNames.append("-")
		self.opNames.append("pointwrangle")
		self.opNames.append("attribwrangle")
		self.opNames.append("attribcreate")
		self.opNames.append("vopsop")


	def refreshOpNames(self):
		'''
		Refresh HDAs
		'''
		self.listOpNames()
		#columnLayout = QtGui.QVBoxLayout()
		columns = []

		for i in range(0, len(self.opNames)):
			if(self.opNames[i] == "-"):
				#self.mainLayout.addStretch(1)
				columnLayout = QtGui.QVBoxLayout()
				columnLayout.setAlignment(QtCore.Qt.AlignTop)
				columns.append(columnLayout)
			else:
				if(i == 0):
					columnLayout = QtGui.QVBoxLayout()
					columnLayout.setAlignment(QtCore.Qt.AlignTop)
					columns.append(columnLayout)
				op = self.opNames[i]
				btnOp = QtGui.QPushButton(op)
				btnOp.setMaximumWidth(self.ui_button_width)
				btnOp.setMinimumHeight(self.ui_button_height)
				btnOp.setMaximumHeight(self.ui_button_height)
				#if i < 4:  
					#btnOp.setStyleSheet('QPushButton {background-color: blue; color: yellow}')
				btnOp.clicked.connect(partial(self.create_sop, op))
				columnLayout.addWidget(btnOp)#, (1, 0), (2,2))

		for column in columns:
			self.mainLayout.addLayout(column)
			#self.mainLayout.addStretch(0)

		# Clear main layout
		
		'''
		btnRefresh = QtGui.QPushButton("Refresh")
		btnRefresh.setMinimumWidth(self.ui_button_width)
		btnRefresh.setMaximumWidth(self.ui_button_width)
		btnRefresh.clicked.connect(self.create_sop)
		self.mainLayout.addWidget(btnRefresh)
		'''

	def create_sop(self, opName = "null"):
		currentSel = hou.selectedNodes()
		if len(currentSel) == 1:
			#s = currentSel[0]
			#sel = hou.node(s.path())
			parentNode = hou.node(currentSel[0].path()).parent()

			newNode = parentNode.createNode(opName)
			newNode.setName(opName, True)
			'''
			colorGreen = hou.Color()
			colorGreen.setRGB([0,1,0])

			colorBlack = hou.Color()
			colorBlack.setRGB([0,0,0])
			'''
			#colorBlack = hou.Color((0,0,0))
			if(opName == "null"):
				newNode.setColor(Color.Black)
			else:
				newNode.setColor(Color.Default)

			newNode.setCurrent(True, True)

			try:
				newNode.setFirstInput(hou.node(currentSel[0].path()))
			except:
				pass
			newNode.moveToGoodPosition()

			newNode.setDisplayFlag(True)
			newNode.setRenderFlag(True)


	def findLoadedHDAs(self):
		'''
		Returns a list of loaded HDAs in Houdini scene.
		HDAs installed by default with Houdini are skipped.
		'''
		self.loadedHDAs = []
		# Scan all node categories
		for category in hou.nodeTypeCategories().values():
			# Scan all node types
			for nodeType in category.nodeTypes().values():
				nodeDef = nodeType.definition()
				# If its a valid and unique HDA
				if (nodeDef is not None) and \
					(nodeDef.libraryFilePath() not in self.loadedHDAs):
					# If not stored at "HFS" (Houdini Installation)
					if not nodeDef.libraryFilePath().startswith(hou.getenv("HFS")):
						self.loadedHDAs.append(nodeDef)

		self.populateHDALayout()

	def populateHDALayout(self):
		'''
		Populate layout with loaded HDAs.
		'''
		for hda in self.loadedHDAs:
			print hda.description()
			btnHDA = QtGui.QPushButton(hda.description())
			btnHDA.setMinimumWidth(self.ui_button_width)
			self.mainLayout.addWidget(btnHDA)

		

