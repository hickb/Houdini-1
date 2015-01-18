########################################################################
# HDA Manager
# by Vishang Shah (vishangshah.com)
# IMPORTANT : This tool is tested and works only with Houdini 14, due to PySide support.
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

from PySide import QtCore, QtGui, QtWebKit

# Reload

# HDAManager
class HDAManager(QtGui.QFrame):
	def __init__(self, parent=None):
		super(HDAManager, self).__init__(parent)

		# all HDAs in current houdini file
		self.loadedHDAs = []

		# UI vars
		self.ui_button_width = 100

		# Main Layout
		self.mainLayout = QtGui.QVBoxLayout()
		self.setLayout(self.mainLayout)

		self.refreshLoadedHDAs()


	def refreshLoadedHDAs(self):
		'''
		Refresh HDAs
		'''

		# Clear main layout
		

		btnRefresh = QtGui.QPushButton("Refresh")
		btnRefresh.setMinimumWidth(self.ui_button_width)
		btnRefresh.setMaximumWidth(self.ui_button_width)
		btnRefresh.clicked.connect(self.findLoadedHDAs)
		self.mainLayout.addWidget(btnRefresh)


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

		

