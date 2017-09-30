from ui_nursepanel import ui_nursepanel as formClass
from PyQt4 import QtCore, QtGui
baseClass = QtGui.QDialog

import sys

class NursePanel(formClass, baseClass):
	def __init__(self, parent=None):
		# initialization
	
		self.setupUI(self)

def main():
	app = QtGui.QApplication(sys.argv)
	bam = NursePanel()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
