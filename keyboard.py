import threading
import termios
import contextlib
import sys
import time

class KeyboardListener(threading.Thread):
	def __init__(self, game):
		threading.Thread.__init__(self)
		self._is_running = True
		self.game = game
	
	def run(self):
		
		#try:
			with self.raw_mode(sys.stdin):
				while self._is_running:
					ch = sys.stdin.read(1)
					if not ch or ch == chr(4):
						break
					self.game.move(ch)
					time.sleep(0.2)
		#except (Exception, KeyboardInterrupt) as e:
		#	print(e)
	
	def stop(self):
		self._is_running = False
	
	@contextlib.contextmanager
	def raw_mode(self,file):
	    old_attrs = termios.tcgetattr(file.fileno())
	    new_attrs = old_attrs[:]
	    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
	    try:
	        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
	        yield
	    finally:
	        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)