import sys
sys.path.insert(0, '/home/pi/ciyus')

import pjsua as pj
from core import Core
from core.util.buddystate import buddystate

class buddy_cb(pj.BuddyCallback):

	def __init__(self, buddy=None):
		pj.BuddyCallback.__init__(self, buddy)
		self.core = Core()

	def on_state(self):
		info = self.buddy.info()
		b = self.core.cfg.find_buddy(info.uri)
		if b:
			buddy_state = buddystate(b.name, info.subscribed, info.online_status, info.uri)
			self.core.cb.buddystate(buddy_state)

if __name__ == "__main__":
	pass
