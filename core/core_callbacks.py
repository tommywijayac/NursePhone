class core_cb(object):
	# ZEN ZEN ZEN WAKARANAI
	def set_cb_regstate(self, func):
		self._regstate = func

	def regstate(self, *args, **kwargs):
		if hasattr(self, "_regstate") and callable(self._regstate):
			self._regstate(*args, **kwargs)

	def set_cb_incoming_call(self, func):
		self._incoming_call = func

	def incoming_call(self, *args, **kwargs):
		if hasattr(self, "_incoming_call") and callable(self._incoming_call):
			self._incoming_call(*args, **kwargs)

	def set_cb_callstate(self, func):
		self._callstate = func

	def callstate(self, *args, **kwargs):
		if hasattr(self, "_callstate") and callable(self._callstate):
			self._callstate(*args, **kwargs)
	
	def set_cb_mediastate(self, func):
		self._mediastate = func

	def buddystate(self, *args, **kwargs):
		if hasattr(self, "_buddystate") and callable(self._buddystate):
			self._buddystate(*args, **kwargs)
	
	def set_cb_buddystate(self, func):
		self._buddystate = func

	def mediastate(self, *args, **kwargs):
		if hasattr(self, "_mediastate") and callable(self._mediastate):
			self._mediastate(*args, **kwargs)

	def set_cb_hangup(self, func):
		self._hangup = func

	def hangup(self, *args, **kwargs):
		if hasattr(self, "_hangup") and callable(self._hangup):
			self._hangup(*args, **kwargs)

	def __init__(self):
		pass

if __name__ == "__main__":
	pass
