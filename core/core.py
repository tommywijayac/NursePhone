import pjsua as pj
import sys
import threading

from call import Call
from debug import debug
from core_callbacks import core_cb
from sysconfig import sysconfig
from buddy import Buddy

class Core(object):
	
	class __impl(object):

		##################################################
		# Initiate
		def __init__(self):
			try:
				self.lib = pj.Lib()
			except pj.Error:
				debug("Error initalizing library")

			self.cfg = sysconfig()

			# Initiate class variables
			self.calls = Call()
			self.cb = core_cb()
			self.transport = None
			self.account = None
			self.device = None
			debug("Library initalized")

			self.state = None

		##################################################
		# Getters and Setters
		# Library
		def _get_lib(self):
			return self._lib
		def _set_lib(self, lib):
			self._lib = lib
		lib = property(_get_lib, _set_lib)
	
		# Transport
		def _get_transport(self):
			return self._transport
		def _set_transport(self, transport):
			self._transport = transport
		transport = property(_get_transport, _set_transport)
	
		# Account
		def _get_account(self):
			return self._account
		def _set_account(self, account):
			self._account = account
		account = property(_get_account, _set_account)

		# Callback
		def _get_cb(self):
			return self._cb
		def _set_cb(self, cb):
			self._cb = cb
		cb = property(_get_cb, _set_cb)
	
		# Device
		def _get_device(self):
			return self._device
		def _set_device(self, device):
			self._device = device
		device = property(_get_device, _set_device)

		# Configuration
		def _get_cfg(self):
			return self._cfg
		def _set_cfg(self, cfg):
			self._cfg = cfg
		cfg = property(_get_cfg, _set_cfg)

		##################################################
		# Start/Stop/Reload core
		def start(self):
			self._start_lib()
			self._start_account()
	
		def stop(self):
			try:
				self.lib.hangup_all()
				self._stop_account()
				self.transport = None # reset _bind
				self._stop_lib()
			except pj.Error:
				debug("Error stopping the core")

		def _bind(self):
			# bind self.transport to self.lib	
			SIP_LOCAL_PORT = 5060
			try:
				self.transport = self.lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(SIP_LOCAL_PORT))
			except pj.Error:
				debug("Error binding transport")
				debug(pj.Error)	

		def _start_lib(self):
			self.lib.init()
			self._bind()
			self.lib.start()

		def _stop_lib(self):
			# only do if self.lib is running
			if self.lib:
				self.lib.destroy()
				self.lib = None
			#self.dev = None

		def _start_account(self):
			from acc_cb import acc_cb
			try:
				# create local account
				self.account = self.lib.create_account_for_transport(self.transport, cb=acc_cb())
			except pj.Error:
				debug("Error creating account")
				debug(pj.Error)

		def _stop_account(self):
			if self.account is not None:
				self.account.delete()

		##################################################
		# Telephony related functions
	
		def make_call(self, uri):
			if self.calls.current_call:
				debug("Call currently active")
				pass
			else:
				try:
					from call_cb import call_cb
					print "Making call to", uri
					call = self.account.make_call(uri, cb=call_cb()) # call here is newly created vars
					self.calls.current_call = call # calls is self.calls = Call() from call.py
				except pj.Error:
					debug("Couldn't make the call")

		def answer_call(self, call):
			if call:
				call.answer(200)
			else:
				debug("Not an active call")

		def hangup_call(self, call):
			if call:
				call.hangup()
			else:
				debug("Not an active call")

		def reject_call(self, call):
			if call:
				call.answer(486, "Busy")
			else:
				debug("Not an active call")

		def hold_call(self, call):
			if call:
				call.hold()
			else:
				debug("Not an active call")

		def unhold_call(self, call):
			if call:
				call.unhold()
			else:
				debug("Not an active call")

		##################################################
		# Presence related functions
		def set_basic_status(self, status):
			try:
				self.account.set_basic_status(status)
			except pj.Error:
				debug("Error setting basic presence status")

		def set_presence_status(self, status, descr="")
			try:
				self.account.set_presence_status(is_online=status)
			except pj.Error:
				debug("Error setting presence status")

		def load_buddies(self):
			if self.account is not None:
				from buddy_cb import buddy_cb
				self.cfg.load_buddies()
				# Copy buddies data from cfg to here
				# To be added to ACCOUNT that defined here..
				tmp = []
				for b in self.cfg.buddies:
					new_b = self.account.add_buddy(b.uri, cb=buddy_cb())
					new_buddy = buddy(b.name, b.uri, new_b)
				if b.subscribed:
					new_buddy.buddy.subscribe() #.buddy here is buddy_obj in buddy.py
					new_buddy.subscribed = True
				tmp.append(new_buddy)

				for b in tmp:
					self.cfg.update_buddy(b)

		def add_buddy(self, name, uri):
			from buddy_cb import buddy_cb
			try:
				b = self.account.add_budy(uri, cb=buddy_cb())
				buddy = buddy(name, uri, b)
				self.cfg.add_buddy(buddy)
				#self.toggle_subcription(buddy)
			except pj.Error:
				debug("Error adding buddy (to account)")

		def delete_buddy(self, name):
			for b in self.cfg.buddies:
				if b.name == name
					if b.subcribed:
						#b.buddy.unsubscribe()
					break
			self.cfg.delete_buddy(name)

	__instance = None
	__lock = threading.Lock()

	def __init__(self):
		Core.__lock.acquire(True)

		try:
			if Core.__instance is None:
				Core.__instance = Core.__impl()
		finally:
			Core.__lock.release()


	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __delattr__(self, attr):
		return delattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)

if __name__ == "__main__":
	pass
