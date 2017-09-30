import sys
from datetime import datetime

if "-d" in sys.argv:
	DEBUG = True
else:
	DEBUG = False

import os

def debug(msg):
	try:
		if DEBUG:
			if type(msg) == unicode:
				print datetime.now().strftime("%d.%m %H:%M:%S") + " " + msg.encode("utf-8")
			else:
				print datetime.now().strftime("%d.%m %H:%M:%S") + " " + msg
	except:
		pass
