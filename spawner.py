import threading
import random
from module import *

class Spawner(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._is_running = True
	def stop(self):
		self._is_running = False
	def shift(self, amount):
		pass
	def getDirection(self, row):
		if row in directions[RIGHT]:
			return RIGHT
		elif row in directions[LEFT]:
			return LEFT
		else:
			return random.randrange(0,2)