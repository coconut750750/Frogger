import sys
import random
import os
import time
import threading
from module import *

class Moveable(threading.Thread):
	def __init__(self, row, ID, direction, speed, isCar, isLast):
		threading.Thread.__init__(self)
		if direction == RIGHT:
			self.x = 0
		else:
			self.x = LENGTH+1
		self.y = row
		self.direction = direction
		self.ID = ID
		self.speed = 1-speed
		self.isCar = isCar
		self._is_running = True
		self.symbol = TESTER
		self.isLast = isLast
		
	def run(self):
		for i in range(0,LENGTH):
			if not self._is_running:
				break
			if self.direction == RIGHT:
				add = 1
			else:
				add = -1
			self.x+=add

			#if not self.isLast and not self.isCar:
			#	pass

			if self.direction == RIGHT and self.x != 0 and board[self.y][self.x-1] == self.symbol:
				board[self.y][self.x-1] = SPACE

			elif self.direction == LEFT and self.x < LENGTH and board[self.y][self.x+1] == self.symbol:
				board[self.y][self.x+1] = SPACE #SPACE

			if self.x > 0 and self.x <= LENGTH:
				board[self.y][self.x] = self.symbol

			if self.symbol == PLAYER:
				global playerPOS
				if self.direction == RIGHT:
					playerPOS[1] += 1
				else:
					playerPOS[1] -= 1

			time.sleep(self.speed)
		board[self.y][self.x] = SPACE
		board[self.y][LENGTH-1] = SPACE
		self.stop()
	
	def stop(self):
		self._is_running = False
		try:
			if self.isCar:
				carList.remove(self)
			else:
				logList.remove(self)
		except ValueError:
			pass
	
	def shift(self, amount):
		board[self.y][self.x] = SPACE
		if self.y+1 > HEIGHT:
			self.stop()
			return
		self.y += amount
		board[self.y][self.x] = self.symbol

class Car(Moveable):
	def __init__(self, row, ID, direction, speed):
		super(Car, self).__init__(row, ID, direction, speed, True, False)
		self.symbol = CAR
		carList.append(self)

class Log(Moveable):
	def __init__(self, row, ID, direction, speed, isLast):
		super(Log, self).__init__(row, ID, direction, speed, False, isLast)
		self.symbol = LOG
		logList.append(self)
