from PyQt4.QtGui import *
from PyQt4 import QtCore

#from connector import Connector
from core import Core
from debug import debug

import time
import sys

class RoomButton(QPushButton):
	def __init__(self, text="", parent=None):
		super(RoomButton, self).__init__(text, parent)
		
		self.core = Core()
		self.core.cb.set_cb_callstate(self.call_state_cb)

		self.setCheckable(True)
		self.clicked.connect(self.on_pressed)
		self.address = None

	# Room address
	def _get_address(self):
		return self._address
	def _set_address(self, address):
		self._address = address
	address = property(_get_address, _set_address)

	# Answer and end call
	def on_pressed(self):
		if self.isChecked():
			print self.core.calls.current_call.info().remote_uri
			if self.core.calls.current_call.info().remote_uri == self.address:
				self.core.answer_call(self.core.calls.current_call)
				self.setText("pressed")
			else:
				self.setText("not pressed")
				self.toggle()
		else:
			self.setText("not pressed")

	def hello(self):
		print "hello from custbutton"

	# callback functions: call when state changed
	def call_state_cb(self, uri, state, code, reason):
		debug("call state: %s %s %s" % (uri, state, code))
		arg1 = QtCore.Q_ARG(str, uri)
		arg2 = QtCore.Q_ARG(str, state)
		arg3 = QtCore.Q_ARG(int, code)
		arg4 = QtCore.Q_ARG(str, reason)
		QtCore.QMetaObject.invokeMethod(self, "onStateChange", QtCore.Qt.QueuedConnection, arg1, arg2, arg3, arg4)
		print("call from {0}. status:{1} with code {2}".format(uri, state, code))
		return

	@QtCore.pyqtSlot(str, str, int, str)
	def onStateChange(self, uri, state, code, reason):
		# Check state
		if state == "EARLY":
			print self.address, " onstatechange"
			# Check which room called			
			if uri == self.address:
				# Modify that room's button
				print "there"
				self.setStyleSheet("background-color: red")

		if state == "DISCONNCTD":
			self.setStyleSheet("background-color: None")
			print "dokodemo"

def main():
	app = QApplication(sys.argv)

	#Layout
	layout = QDialog()
	grid = QGridLayout()

	room1 = RoomButton("Room 1")
	room1.address = "<sip:ttomcet@sip.linphone.>"
	grid.addWidget(room1)

	room2 = RoomButton("Room 2")
	room2.address = "babam"
	grid.addWidget(room2)

	room3 = RoomButton("Room 3")
	room3.address = "<sip:ttomcet@sip.linphone.org>"
	grid.addWidget(room3)
	
	layout.setLayout(grid)
	layout.show()

	core = Core()
	core.start()
	#connector = Connector(self)

	sys.exit(app.exec_())
	
if __name__ == "__main__":
	main()
