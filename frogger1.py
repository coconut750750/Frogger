#!/usr/bin/python3

import sys
import random
import os
import time
import threading
import termios
import contextlib

os.system('clear')

LENGTH = 20
HEIGHT = 20
RIGHT = 1
LEFT = 0
NUMBEROFCARS = 10
CAR = "\033[033m=\033[00m"
SPACE = " "
FREESPACE = "\033[042m \033[00m"
DANGERSPACE = "\033[041m \033[00m"
PLAYER = "i"
playerPOS = []
U = "w"
R = "d"
D = "s"
L = "a"
steps = 0

carList = []

board = []
freeRows = []
dangerRows = []

threads = []

newFreeRow = []
newDangerRow = []

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

class Car(threading.Thread):

	def __init__(self, row, ID, direction, speed):
		threading.Thread.__init__(self)
		if direction == RIGHT:
			self.x = 0
		else:
			self.x = LENGTH
		self.y = row
		self.direction = direction
		self.ID = ID
		self.speed = speed
		carList.append(ID)
		self._is_running = True
	def run(self):
		for i in range(0,LENGTH):
			if not self._is_running:
				return
			if self.direction == RIGHT:
				add = 1
			else:
				add = -1
			self.x+=add
			if self.direction == RIGHT and self.x != 0 and board[self.y][self.x-1] == CAR:
				board[self.y][self.x-1] = SPACE
			elif self.direction == LEFT and self.x < LENGTH and board[self.y][self.x+1] == CAR:
				board[self.y][self.x+1] = SPACE
			if self.x > 0 and self.x < LENGTH:
				board[self.y][self.x] = CAR
			time.sleep(self.speed)
		if self.direction == RIGHT:
			board[self.y][LENGTH] = SPACE
		else:
			board[self.y][1] = SPACE
		self.stop()
	def stop(self):
		self._is_running = False
		try:
			carList.remove(self.ID)
		except ValueError:
			return
	def shift(self, amount):
		board[self.y][self.x] = SPACE
		if self.y+1 > HEIGHT:
			self.stop()
			return
		self.y += amount
		board[self.y][self.x] = CAR
		

class KeyboardListener(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._is_running = True
	def run(self):
		try:
			while self._is_running:
				with raw_mode(sys.stdin):
					while True:
						ch = sys.stdin.read(1)
						if not ch or ch == chr(4):
							break
						move(ch)
		except (Exception, KeyboardInterrupt) as e:
			pass
	def stop(self):
		self._is_running = False

def printBoard():
	hasPlayer = False
	for l in range(0,len(board)):
		for i in range(0,len(board[l])):
			if i == 0:
				board[l][i] = "|"
			if l-1 in freeRows and board[l][i] == SPACE:
				sys.stdout.write(FREESPACE)
			elif l-1 in dangerRows and board[l][i] == SPACE:
				sys.stdout.write(DANGERSPACE)
			else:
				sys.stdout.write(board[l][i])
			if board[l][i] == PLAYER:
				hasPlayer = True
		if l == 0:
			sys.stdout.write("\t steps: "+str(steps))
		print()
	sys.stdout.write("\033[F"*(HEIGHT+2))
	sys.stdout.flush()
	if not hasPlayer:
		gameover()


def start(tuple):
	global playerPOS
	x = tuple[0]
	y = tuple[1]
	playerPOS = [HEIGHT, int(LENGTH/2)]
	board.append(["-"]*(x+2))
	for i in range(0,y):
		board.append(["|"])
		if random.randrange(0,2) == 0:
			freeRows.append(i)
		else:
			dangerRows.append(i)
		for y in range(0,x):
			board[len(board)-1].append(SPACE)
		board[len(board)-1].append("|")
	board.append(["-"]*(x+2))
	updatePlayer()

def shiftBoard():
	global freeRows, dangerRows
	for car in range(1, len(threads)):
		threads[car].shift(1)

	tempFree = []
	tempDanger = []
	for i in range(0,len(freeRows)):
		if freeRows[i] < HEIGHT-1:
			tempFree.append(freeRows[i] + 1)
	for i in range(0,len(dangerRows)):
		if dangerRows[i] < HEIGHT-1:
			tempDanger.append(dangerRows[i] + 1)
	freeRows = tempFree
	dangerRows = tempDanger
	if random.randrange(0,2) == 0:
		freeRows.append(0)
	else:
		dangerRows.append(0)

def updatePlayer():
	x = playerPOS[0]
	y = playerPOS[1]
	for l in range(0,len(board)):
		for i in range(0,len(board[l])):
			if board[l][i] == PLAYER:
				board[l][i] = SPACE
				break
	if board[x][y] == CAR:
		return
	board[x][y] = PLAYER

def move(direction):
	global playerPOS, steps
	if direction == U:
		if steps < 3:
			steps += 1
		playerPOS[0] -= 1
		if playerPOS[0] < HEIGHT-3:
			shiftBoard()
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
	updatePlayer()
	
def gameover():
	time.sleep(1)
	os.system("clear")
	print("GAME OVER")
	print("STEPS:",steps)
	time.sleep(0.5)
	quit()

def quit():
	for i in range(0, len(threads)):
		threads[i].stop()
	sys.stdout.write("\033[E"*(HEIGHT))
	print("PRESS Q TO CONTINUE...")
	exit()

def main():
	try:
		start((LENGTH,HEIGHT))

		carID = 0
		threads.append(KeyboardListener())
		threads[0].start()

		while True:
			if len(carList) < NUMBEROFCARS:
				car = Car(random.choice(dangerRows)+1, carID, random.randrange(0,2), random.random()/3)
				threads.append(car)
				car.start()
				carID += 1
			printBoard()
			time.sleep(0.1)
	except KeyboardInterrupt:
		try:
			quit()
		except Exception:
			return


if __name__=='__main__':
	main()
