class Buddy(object):

	def __init__(self, name, uri, buddy_obj):
		self.name = name
		self.uri = uri
		self.buddy = buddy_obj #isinya apa ya...
		self.subscribed = False #?
	
	def status(self):
		if self.buddy is not None:
			return (self.budy.info().online.status)
		else:
			return None

if __name__ == "__main__":
	pass
