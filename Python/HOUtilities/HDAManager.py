########################################################################
# HDA Manager
# by Vishang Shah (vishangshah.com)
# IMPORTANT : This tool is tested and works only with Houdini 14.
#
# Description : Provides an interface for quick access to some HDA functionalities.
#
# Usage : Copy the folder HDA_Manager to [your houdini 14.0 installation]\houdini\python2.7libs\
#
########################################################################

# Import libraries
import os
import sys
import json

import hou

from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtWebKit

from functools import partial

from . import Color
reload(Color)

# Reload

# HDAManager
class HDAManager(QWidget):
	def __init__(self, parent=None):
		super(HDAManager, self).__init__(parent)

		# all HDAs in current houdini file
		self.loadedHDAs = []

		# Global UI vars
		self.ui_button_width = 120
		self.ui_button_height = 20

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
		btnRefresh = QPushButton("Refresh HDAs")
		btnRefresh.setMinimumWidth(self.ui_button_width)
		btnRefresh.setMaximumWidth(self.ui_button_width)
		btnRefresh.clicked.connect(self.findLoadedHDAs)
		fixedLayout.addWidget(btnRefresh)

		# Save All
		btnSaveAll = QPushButton("Save All")
		btnSaveAll.setMinimumWidth(self.ui_button_width)
		btnSaveAll.setMaximumWidth(self.ui_button_width)
		#btnSaveAll.clicked.connect(self.findLoadedHDAs)
		fixedLayout.addWidget(btnSaveAll)

		self.layout.addLayout(fixedLayout)


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
		# Remove HDA widget if it exists
		HDAScroll = self.layout.itemAt(1)

		if(HDAScroll):
			h = self.layout.takeAt(1)
			w = h.widget()
			w.setParent(None)
			del h,w
			#self.layout.removeWidget(HDAScroll)

		HDAWidget = QFrame()
		HDALayout = QVBoxLayout()
		
		# Iterate through all HDA assets and create the layout
		#for i in range(0, 100):
		for hda in self.loadedHDAs:
			print hda.description()
			row = QHBoxLayout()
			row.setAlignment(Qt.AlignLeft)

			btnFav = QToolButton()
			#icon = btnFav.style().standardIcon(QStyle.SP_TitleBarContextHelpButton)
			icon = btnFav.style().standardIcon(QStyle.SP_ArrowUp)
			btnFav.setIcon(icon)
			row.addWidget(btnFav)

			'''
			btnLockToggle = QToolButton()
			btnLockToggle.setMinimumWidth(50)
			btnLockToggle.setMaximumWidth(50)
			icon = btnLockToggle.style().standardIcon(QStyle.SP_DialogOpenButton)
			btnLockToggle.setIcon(icon)
			btnLockToggle.clicked.connect(partial(self.toggleLockOnHDA, hda, btnLockToggle))
			row.addWidget(btnLockToggle)
			'''

			lblHDA = QLabel(hda.description())
			lblHDA.setMinimumWidth(150)
			lblHDA.setMaximumWidth(150)
			row.addWidget(lblHDA)

			btnSave = QToolButton()
			btnSave.setMinimumWidth(120)
			btnSave.setMaximumWidth(120)
			icon = btnSave.style().standardIcon(QStyle.SP_DialogSaveButton)
			btnSave.setIcon(icon)
			btnSave.clicked.connect(partial(self.saveHDA, hda))
			row.addWidget(btnSave)

			HDALayout.addLayout(row)
			

		HDAWidget.setLayout(HDALayout)

		scroll = QScrollArea()
		scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		scroll.setWidget(HDAWidget)

		self.layout.addWidget(scroll)

	def saveHDA(self, hda):
		print("Save - " + hda.description())

		# Get all instances of HDA
		for node in hou.node("/").allSubChildren():
			if (node.type().definition() == hda and (not node.isLocked())):
				node.type().definition().updateFromNode(node)


			
				
        

		