import pjsua as pj

from core import Core #terkoneksi di call (sama, tp karena udah diinit di core.py jd ini yg di link kesana). (cb juga)
from debug import debug

class call_cb(pj.CallCallback):
	def __init__(self, call=None):
		pj.CallCallback.__init__(self, call)
		self.core = Core()

	# Notification when call state has changed
	def on_state(self):
		if self.call.info().state == pj.CallState.DISCONNECTED:
			self.core.calls.current_call = None
			self.core.cb.hangup()

		uri = self.call.info().remote_uri
		state = self.call.info().state_text
		code = self.call.info().last_code
		reason = self.call.info().last_reason
		self.core.cb.callstate(uri, state, code, reason)

	# Notification when call's media state has changed
	def on_media_state(self):
		if self.call.info().media_state == pj.MediaState.ACTIVE:
			# Connect the call to sound device
			call_slot = self.call.info().conf_slot
			self.core.lib.instance().conf_connect(call_slot, 0)
			self.core.lib.instance().conf_connect(0, call_slot)
			debug("Media is now active")
		else:
			debug("Media is inactive")

if __name__ == "__main__":
	pass
