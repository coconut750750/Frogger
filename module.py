LENGTH = 20
HEIGHT = 20
RIGHT = 1
LEFT = 0
NUMBEROFCARS = 15
NUMBEROFLOGS = 15
CAR = "\033[033m=\033[00m"
SPACE = " "
FREESPACE = "\033[042m \033[00m"
DANGERSPACE = "\033[043m \033[00m"
WATERSPACE = "\033[046m \033[00m"
PLAYER = "i"
LOG = "o"
TESTER = "z"
U = "w"
R = "d"
D = "s"
L = "a"

def reset():
	global playerPOS, steps, finalSteps, carList, logList, rowsNeedLog, board, freeRows, dangerRows, waterRows, threads, directions
	playerPOS = [HEIGHT, int(LENGTH/2)]
	steps = 0
	finalSteps = 0
	carList = []
	logList = []
	rowsNeedLog = []
	board = []
	#ROW OF THE BOARD - 1 CORRESPONDS TO ROW STORES HERE
	freeRows = []
	dangerRows = []
	waterRows = []
	threads = []
	directions = [[],[]]

reset()
