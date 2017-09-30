from PyQt4 import QtCore, QtGui
from custbutt import RoomButton

class ui_nursepanel(object):

	def setupUI(self, nursepanel):
		#nursepanel.setObjectName("NursePanel")
		self.mainlayout = QtGui.QGridLayout()
		self.mainlayout.setSpacing(10)

		self.room1 = RoomButton("Room 1")
		self.room2 = RoomButton("Room 2")
		self.room3 = RoomButton("Room 3")

		self.mainlayout.addWidget(self.room1, 1, 0)
		self.mainlayout.addWidget(self.room2, 2, 1)
		self.mainlayout.addWidget(self.room3, 3, 2)

		self.setLayout(self.mainlayout)

		self.setGeometry(300, 300, 350, 350)
		self.setWindowTitle("Review")

		self.show()

	


