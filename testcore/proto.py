import sys
sys.path.insert(0, '/home/pi/ciyus/')

from core.core import Core

# not class, there is no self.___
def regstate_cb(state):
	print str(state)

def main():
	core = Core()
	core.cb.set_cb_regstate(regstate_cb)
	core.start()

	print "Registered at",
	print "sip:",core.transport.info().host, " port",core.transport.info().port

	while True:
		print "Menu: m=make call, h=hangup call, a=answer call, q=quit"
		input = sys.stdin.readline().rstrip("\r\n")
		if input == "m":
			print "Destination URI:",
			input = sys.stdin.readline().rstrip("\r\n")
			if input == "":
				continue
			core.make_call(input)
			continue

		elif input == "h":
			core.hangup_call(core.calls.current_call)
			continue

		elif input == "a":
			core.answer_call(core.calls.current_call)
			continue
		
		elif input == "q":
			break

	core.stop()

if __name__ == "__main__":
	main()
