import pjsua as pj

class Call(object):
	_current_call = None
	_calls = []

	def _get_current_call(self):
		return self._current_call

	def _set_current_call(self, call):
		self._current_call = call

	current_call = property(_get_current_call, _set_current_call)

	def _get_list_calls(self):
		return self._calls

	def _set_list_calls(self, calls):
		self._calls = calls

	list = property(_get_list_calls, _set_list_calls)

	def __init__(self):
		pass

if __name__ == "__main__":
	pass
