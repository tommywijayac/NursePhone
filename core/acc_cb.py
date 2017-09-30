import pjsua as pj
#import os
from core import Core

class acc_cb(pj.AccountCallback):

	def __init__(self, account=None):
		pj.AccountCallback.__init__(self, account)
		self.core = Core()

	def on_reg_state(self):
		account_info = self.account.info()
		self.core.cb.regstate(str(account_info.uri), str(account_info.reg_status), str(account_info.reg_reason)) #gaktau buat apa

	def on_incoming_call(self, call):
		if self.core.calls.current_call:
		# other call is happening
			call.answer(486, "Busy..")
			return
		else:
			dev_error = False
			try:
			# play incoming sound
				pass
			except:
				dev_error = True
				self.core.device.set_null_dev() #set incoming sound to NULL
			finally:
			# initiate call
				self.core.calls.current_call = call
				from call_cb import call_cb
				self.core.calls.current_call.set_callback(call_cb())
				self.core.calls.current_call.answer(180)

				print "Incoming call from", call.info().remote_uri

				# store call info here
				info = call.info()
				self.core.cb.incoming_call(info, dev_error)

if __name__ == "__main__":
	pass
