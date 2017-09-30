import sys
sys.path.insert(0, '/home/pi/ciyus')
import os

import pjsua as pj
import threading
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("example.cfg")
import traceback

from buddy import Buddy
from debug import debug

class sysconfig(object):

	class __impl(object):
		# Get and Set
		def _get_media(self):
			return self._media
		def _set_media(self):
			self._media = media
		media = property(_get_media, _set_media)

		def _get_buddies(self):
			return self._buddies
		def _set_buddies(self):
			self._buddies = buddies
		buddies = property(_get_buddies, _set_buddies)

		# Presence related config functions
		def load_buddies(self):
			try:
				self.buddies = []
				b = config.get('Room1', 'name')
				c = config.get('Room1', 'uri')
				x = config.getint('Room1', 'subscribed')
				d = Buddy(b, c, None)
				if x == 1:
					d.subscribed = True
				self.buddies.append(d)
				
				e =	config.get('Room2', 'name')
				f = config.get('Room2', 'uri')
				y = config.getint('Room2', 'subscribed')
				g = Buddy(e, f, None)
				if y == 1:
					g.subscribed = True
				self.buddies.append(g)
			except Exception,e:
				return False
			return True

		def find_buddy(self, text):
			for b in self.buddies:
				if b.name == str(text) or b.uri == str(text):
					return b #return object
			return none

		def update_buddy(self, buddy):
			for b in self.buddies:
				if b.name == buddy.name:
					self.buddies.remove(b)
					self.buddies.append(buddy)
					break;

		def toggle_buddy_subscription(self, buddy):
			for each_section in config.sections():	
				for name, value in config.items(each_section):
					if value == buddy.uri:
						config.set(each_section, 'subscribed', int(buddy.subscribed))

		def add_buddy(self, buddy):
			for b in self.buddies:
				if b.name == buddy.name or b.uri == buddy.uri:
					found = true
					debug("Error adding new buddy. Duplicate Name or Uri")
					break
			if found == false:
				self.buddies.append(buddy)
				debug("Success adding new buddy")

		def delete_buddy(self, name):
			for b in self.buddies:
				if b.name == name:
					self.buddies.remove(b)
					debug("Deleting {0} ({1}) from buddy".format(b.name, b.uri))

		def __init__(self):
			self.media = pj.MediaConfig()
			#self._load_config(self.media, "media")

			self.buddies = []

		__instance = None
		__lock = threading.Lock()

		# Initialize the ONLY sysconfig instance (if needed)
		def __init__(self):
			sysconfig.__lock.acquire(True)
			try:
				if sysconfig.__instance is None:
					sysconfig.__instance = sysconfig.__impl()
			finally:
				sysconfig.__lock.release()

		# Delegate access to implementation
		def __getattr__(self, attr):
			return getattr(self.__instance, attr)

		def __delattr__(self, attr):
			return delattr(self.__instance, attr)

		def __setattr__(self, attr, value):
			return setattr(self.__instance, attr, value)
