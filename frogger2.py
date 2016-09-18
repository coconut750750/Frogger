#!/usr/bin/python3

import sys
import random
import os
import time
import threading
from module import *
from keyboard import *
from moveable import *
from spawner import *

os.system('clear')

class Frogger():
	def __init__(self):
		pass
	def printBoard(self):
		hasPlayer = False
		for l in range(0,len(board)):
			for i in range(0,len(board[l])):
				if i == 0 or i == len(board[l])-1:
					board[l][i] = "|"
				if l-1 in freeRows and board[l][i] == SPACE:
					print(FREESPACE,end="")
				elif l-1 in dangerRows and board[l][i] == SPACE:
					print(DANGERSPACE,end="")
				elif l-1 in waterRows and board[l][i] == SPACE:
					print(WATERSPACE,end="")
				else:
					print(board[l][i],end="")
				if board[l][i] == PLAYER:
					hasPlayer = True
			if l == 0:
				print("\t steps: "+str(steps),end="")
			print()
		sys.stdout.write("\033[F"*(HEIGHT+2))
		sys.stdout.flush()
		if not hasPlayer:
			self.gameover()

	def addRow(self, row):
		if random.randrange(0,3) == 2 and not(row-1 in waterRows):
			if (row == 0 and not(row+1 in waterRows)) or row != 0:
				waterRows.append(row)
				rowsNeedLog.append(row)
				return
		if random.randrange(0,2) == 0:
			freeRows.append(row)
		else:
			dangerRows.append(row)

	def start(self,tuple):
		global playerPOS, rowsNeedLog
		x = tuple[0]
		y = tuple[1]
		board.append(["-"]*(x+2))
		for i in range(0,y):
			board.append(["|"])
			if i == HEIGHT-1:
				freeRows.append(i)
			else:
				self.addRow(i)
			for y in range(0,x):
				board[len(board)-1].append(SPACE)
			board[len(board)-1].append("|")
		board.append(["-"]*(x+2))
		self.updatePlayer()
		rowsNeedLog = waterRows

	def updateRows(self, l):
		templ = []
		for i in range(0,len(l)):
			if l[i] < HEIGHT-1:
				templ.append(l[i] + 1)
		return templ

	def shiftBoard(self):
		global freeRows, dangerRows, waterRows, rowsNeedLog, threads, directions
		tempThreads = [threads[0]]
		for car in range(1, len(threads)):
			if threads[car]._is_running:
				threads[car].shift(1)
				tempThreads.append(threads[car])
		threads = tempThreads

		freeRows = self.updateRows(freeRows)
		dangerRows = self.updateRows(dangerRows)
		waterRows = self.updateRows(waterRows)
		rowsNeedLog = self.updateRows(rowsNeedLog)
		directions[RIGHT] = self.updateRows(directions[RIGHT])
		directions[LEFT] = self.updateRows(directions[LEFT])
		self.addRow(0)

	def updatePlayer(self):
		global playerPOS
		x = playerPOS[0]
		y = playerPOS[1]
		for l in range(0,len(board)):
			for i in range(0,len(board[l])):
				if board[l][i] == PLAYER:
					board[l][i] = SPACE
					break
		for log in logList:
			log.symbol = LOG

		if board[x][y] == CAR:
			return

		logIsPlayer = False

		if board[x][y] == LOG:
			board[x][y] = PLAYER
			logIsPlayer = True

		elif y>1 and board[x][y-1] == LOG:
			board[x][y-1] = PLAYER
			playerPOS[1] -= 1
			logIsPlayer = True
			y = y-1

		elif y<LENGTH and board[x][y+1] == LOG:
			board[x][y+1] = PLAYER
			playerPOS[1] += 1
			logIsPlayer = True
			y = y+1

		if logIsPlayer:
			for log in logList:
				if log.y == x and log.x == y:
					log.symbol = PLAYER
					return
			

		if x-1 in waterRows:
			return

		board[x][y] = PLAYER

	def move(self,direction):
		global playerPOS, steps
		if direction == U:
			if steps < 3:
				steps += 1
			playerPOS[0] -= 1
			if playerPOS[0] < HEIGHT-3:
				self.shiftBoard()
				playerPOS[0] += 1
				steps += 1
		if direction == R:
			if playerPOS[1] < LENGTH:
				playerPOS[1] += 1
		if direction == D:
			if playerPOS[0] < HEIGHT:
				playerPOS[0] += 1
		if direction == L:
			if playerPOS[1] > 1:
				playerPOS[1] -= 1
		self.updatePlayer()
		
	def gameover(self):
		finalSteps = steps-1
		time.sleep(1)
		os.system("clear")
		print("GAME OVER")
		print("STEPS:",finalSteps)
		time.sleep(0.5)
		self.quit()

	def quit(self):
		for i in range(0, len(threads)):
			threads[i].stop()
		sys.stdout.write("\033[E"*(HEIGHT+2))
		print("PRESS Q TO CONTINUE...")
		sys.exit()

class CarSpawner(Spawner):
	def __init__(self):
		super(CarSpawner, self).__init__()
	def run(self):
		carID = 0
		while self._is_running:
			if len(carList) < NUMBEROFCARS and len(dangerRows)>0:
				row = random.choice(dangerRows)+1
				direction = self.getDirection(row)
				if not(row in directions[direction]):
					directions[direction].append(row)

				car = Car(row, carID, direction, random.random()/2+0.15)
				threads.append(car)
				car.start()
				carID += 1
			time.sleep(0.1)
	
class LogSpawner(Spawner):
	def __init__(self):
		super(LogSpawner, self).__init__()
	def run(self):
		logID = 0
		while self._is_running:
			if len(rowsNeedLog)>0 and len(logList) < NUMBEROFLOGS:
				#length = 1
				row = random.choice(rowsNeedLog)+1
				direction = self.getDirection(row)
				if not(row in directions[direction]):
					directions[direction].append(row)
				#for i in range(0,length):
				#	if i == length-1:
				log = Log(row, logID, direction, 0.5, True)
				#	else:
				#		log = Log(self.row, logID, direction, 0.5, False)
				threads.append(log)
				log.start()
				logID += 1
				time.sleep(0.6)

def main():
	try:
		frogger = Frogger()
		frogger.start((LENGTH,HEIGHT))

		logID = 0
		threads.append(KeyboardListener(frogger))
		threads[0].start()

		spawnerCar = CarSpawner()
		spawnerCar.start()

		spawnerLog1 = LogSpawner()
		spawnerLog1.start()
		spawnerLog2 = LogSpawner()
		spawnerLog2.start()

		threads.append(spawnerCar)
		threads.append(spawnerLog1)
		threads.append(spawnerLog2)

		while True:
			frogger.printBoard()
	except KeyboardInterrupt:
		try:
			frogger.quit()
		except Exception:
			return


if __name__== '__main__':
	main()
