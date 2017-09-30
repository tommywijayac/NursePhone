from PyQt4 import QtCore, QtGui

from debug import debug
from core import Core
import sys
import threading

class Connector(object):

	def __init__(self, ui):
		self.form = ui
		# dimanakah letak form.ui????? apa hubungannya????
		
		try:
			self.core = Core()
			self.holding = False #flag
			self.core.cb.set_cb_callstate(self.call_state_cb)
			self.core.cb.set_cb_regstate(self.regstate_cb)
			self.core.cb.set_cb_incoming_call(self.incoming_call_cb)

			self.core.start()

		except Exception, e:
			debug("failed")
	
	#########################################################
	# Telephony related functions - connect to core
	# Why? to be modular!
	# You can see core and core+gui as separated project
	# This connector is the "core" for the latter

	def make_call(self, uri):
		if len(uri) > 0:
			try:
				self.core.make_call(uri)
			except:
				QtGui.QMessageBox.critical(self.form, "Error", str(e))

	def answer_call(self):
		try:
			self.core.answer_call(self.core.calls.current_call)
		except:
			QtGui.QMessageBox.critical(self.form, "Error", str(e))

	def hangup_call(self):
		try:
			self.core.hangup_call(self.core.calls.current_call)
		except:
			QtGui.QMessageBox.critical(self.form, "Error", str(e))

	def reject_call(self):
		try:
			self.core.reject_call(self.core.calls.current_call)
		except:
			QtGui.QMessageBox.critical(self.form, "Error", str(e))

	def hold_call(self):
		try:
			if self.holding:
				#self.form.ui.actionHold.setText("hold")
				self.holding = False
				self.core.unhold_call(self.core.calls.current_call)
			else:
				#self.form.ui.actionHold.setText("unhold")
				self.holding = True
				self.core.hold_call(self.core.calls.current_call)
		except:
			QtGui.QMessageBox.critical(self.form, "Error", str(e))

	def call_state_cb(self, uri, state, code, reason):
		debug("call state: %s %s %s" % (uri, state, code))
		arg1 = QtCore.Q_ARG(str, uri)
		arg2 = QtCore.Q_ARG(str, state)
		arg3 = QtCore.Q_ARG(int, code)
		arg4 = QtCore.Q_ARG(str, reason)
		QtCore.QMetaObject.invokeMethod(self.form, "onStateChange", QtCore.Qt.QueuedConnection, arg1, arg2, arg3, arg4)
		return

	def regstate_cb(self, uri, code, reason):
		if code == "200":
			QtCore.QMetaObject.invokeMethod(self.form, "onRegister", QtCore.Qt.QueuedConnection)
		else:
			QtCore.QMetaObject.invokeMethod(self.form, "onRegisterfailed", QtCore.Qt.QueuedConnection)

	def incoming_call_cb(self, call_info, dev_error):
		QtCore.QMetaObject.invokeMethod(self.form, "onIncomingCall", QtCore.Qt.QueuedConnection)
