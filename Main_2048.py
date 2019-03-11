import time
import pygame
from random import randint
from pygame.locals import *
from constants_2048 import *
pygame.init()
clock = pygame.time.Clock()
numFont = pygame.font.SysFont('courier', int(cellSize*.5))

board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
preMoveBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
tempBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
storageBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
collisionBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
endingLocations = [[[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0]]]
queuedArray = [[0,0],[0,0],[0,0],[0,0]]

newTileLoc = [0,0]
newTileVal = 0
score = 0
tempScore = 0
tileCount = 1
tempTileCount = 1
gameWon = False
gameLost = False
tempGameWon = False
tempGameLost = False
validMove = 0
latestDirection = ""

window = pygame.display.set_mode((window_Width, window_Height))
window.fill((255,255,255))
pygame.display.set_caption ('2048')
screen = pygame.display.get_surface()
moveTraversalKey = {
	'right' : ((0,-1),(1,0),(-1,0)),
	'left' : ((0,1),(1,0),(0,0)),
	'down' : ((1,0),(0,-1),(0,-1)),
	'up' : ((1,0),(0,1),(0,0))
}
	
def printBoard():
	for y in range(0,4):
		for x in range(0,4):
			print(board[x][y], end = "   ")
		print("\n\n")
	print("\n**********************\nScore:",score,tempGameLost, validMove)

def printTempBoard():
	for y in range(0,4):
		for x in range(0,4):
			print(tempBoard[x][y], end = "   ")
		print("\n\n")
	print("\n$$$$$$$$$$$$\nScore:",validMove)
def justify(direction):
	global tempBoard, storageBoard	
	tempVec = moveTraversalKey[direction]
	storageBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for x in range(0,4):
		placeholder = 0
		for y in range(0,4):
			tempInt = tempBoard[tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1]]
			if tempInt != 0:
				storageBoard[tempVec[0][0] * x + tempVec[0][1] * placeholder + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * placeholder + tempVec[2][1]] = tempInt
				placeholder += 1
	tempBoard = [col[:] for col in storageBoard]

def processShift(direction):   	
	global tempBoard, collisionBoard, tempTileCount, tempScore, tempGameWon, validMove
	originalBoard = [col[:] for col in tempBoard]
	validMove = 0
	for x in range(0,4):
		for y in range(0,4):
			collisionBoard[x][y] = 0
	justify(direction)
	tempVec = moveTraversalKey[direction]
	for x in range(0,4):
		for y in range(0,3):
			tempInt1 = tempBoard[tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1]]	
			tempInt2 = tempBoard[tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] + tempVec[0][1] ] [tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1] + tempVec[1][1]]
			if tempInt1 != 0 and tempInt1 == tempInt2:
				tempBoard[tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1]] = 2*tempInt1		
				collisionBoard[tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1]] = 1		
				tempBoard[tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] + tempVec[0][1] ] [tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1] + tempVec[1][1]] = 0
				tempScore += 2*tempInt1
				tempTileCount -= 1
				if tempInt1 == 1024:
					tempGameWon = 1
	justify(direction)
	for x in range (0,4):
		for y in range(0,4):
			if tempBoard[x][y] != originalBoard[x][y]:
				validMove = 1
def processMove(direction):
	if tempGameLost or tempGameWon:
		return (tempBoard,validMove)
	animateShift(direction)
	if validMove == 1:
		processNewTile()
	if tempTileCount == 16:
		checkLoss()
	return (tempBoard,validMove)
def checkLoss():
	global tempBoard, collisionBoard, tempTileCount, tempScore, tempGameWon, tempGameLost, validMove
	tempBoardHolder = [col[:] for col in tempBoard]
	collisionBoardHolder = [col[:] for col in collisionBoard]
	tileCountHolder = tempTileCount
	validMoveHolder = validMove
	scoreHolder = tempScore
	gameWonHolder = tempGameWon
	noMove = True
	for direction in ['right','left','down','up']:
		processShift(direction)
		tempBoard = [col[:] for col in tempBoardHolder]
		tempTileCount = tileCountHolder
		collisionBoard = [col[:] for col in collisionBoardHolder]
		tempScore = scoreHolder
		tempGameWon = gameWonHolder
		if validMove == 1:
			noMove = False
		validMove = validMoveHolder
	tempGameLost = noMove
		
def processNewTile():
	global tempTileCount, tempBoard,newTileVal, newTileLoc
	newTile = 0
	fullBoard = 0
	while(newTile == 0):
		newTileLoc[0] = randint(0,3)
		newTileLoc[1] = randint(0,3)
		if tempBoard[newTileLoc[0]][newTileLoc[1]] == 0:
			val = randint(0,10)
			if val < 10:
				tempBoard[newTileLoc[0]][newTileLoc[1]] = 2
			else:
				tempBoard[newTileLoc[0]][newTileLoc[1]] = 4
			newTileVal = tempBoard[newTileLoc[0]][newTileLoc[1]]
			newTile = 1
			tempTileCount += 1
		

def drawBoard():
	pygame.draw.rect(window, (187,173,160),(boardLocX,boardLocY,boardSize,boardSize))
	for x in range(0,4):
		for y in range(0,4):
			drawCell(x,y)
			if board[x][y] != 0:
				drawCell(x,y,board[x][y])	
	pygame.display.update()

def animateShift(direction):
	global endingLocations, queuedArray, preMoveBoard, collisionBoard
	preMoveBoard = [col[:] for col in tempBoard]
	processShift(direction)
	tempVec = moveTraversalKey[direction]
	for x in range(0,4):
		if collisionBoard[tempVec[0][0] * x + tempVec[0][1] *2 + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * 2 + tempVec[2][1]] == 1:
			if collisionBoard[tempVec[0][0] * x + tempVec[0][1] * 0 + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * 0 + tempVec[2][1]] == 1:
				collisionBoard[tempVec[0][0] * x + tempVec[0][1] *2 + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * 2 + tempVec[2][1]] = 0
				collisionBoard[tempVec[0][0] * x + tempVec[0][1] *1 + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * 1 + tempVec[2][1]] = 1
			
		for y in range(0,4):
			endingLocations[x][y][0] = 9
			endingLocations[x][y][1] = 9 
	for x in range(0,4):
		for y in range(0,4):
				queuedArray[y][0] = 9
				queuedArray[y][1] = 9
		placeholder = 0	
		for y in range(0,4):
			if preMoveBoard[tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1]] != 0:
				xcoor = tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] 
				ycoor = tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1]	
				queuedArray[placeholder][0]= xcoor
				queuedArray[placeholder][1]= ycoor
				placeholder += 1	
		placeholder = 0
		for y in range(0,4):
			collisionCheck = collisionBoard[tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] ] [tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1]]	
			if placeholder < 4 and queuedArray[placeholder][0] != 9:
				for z in range(0,collisionCheck+1):
					endingLocations[queuedArray[placeholder+z][0]][queuedArray[placeholder+z][1]][0] = tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0] 
					endingLocations[queuedArray[placeholder+z][0]][queuedArray[placeholder+z][1]][1] = tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1] 
				placeholder += collisionCheck+1
	for x in range(0,4):
		for y in range(0,4):
			if endingLocations[x][y][0]!=9:
				for z in range(0,2):
					if endingLocations[x][y][z] < 0:
						endingLocations[x][y][z]= 4 + endingLocations[x][y][z]
def renderMotion(direction):
	tempVec = moveTraversalKey[direction]
	pygame.draw.rect(window, (187,173,160),(boardLocX,boardLocY,boardSize,boardSize))
	for x in range(0,4):
		for y in range(0,4):
			drawCell(x,y)
	for iterator in range(0,10):
		t = iterator/9
		pygame.draw.rect(window, (187,173,160),(boardLocX,boardLocY,boardSize,boardSize))
		for x in range(0,4):
			for y in range(0,4):
				drawCell(x,y)
		for x in range(0,4):
			for y in range(0,4):
				startingX = tempVec[0][0] * x + tempVec[0][1] * y + tempVec[2][0]
				startingY = tempVec[1][0] * x + tempVec[1][1] * y + tempVec[2][1]
				if preMoveBoard[startingX][startingY] != 0:
					if startingX < 0:
						startingX += 4
					if startingY < 0:
						startingY += 4
					locx = (endingLocations[startingX][startingY][0] - startingX)*t + startingX
					locy = (endingLocations[startingX][startingY][1] - startingY)*t + startingY
					drawCell(locx,locy, preMoveBoard[startingX][startingY])
		pygame.display.update()
		pygame.event.get()
		clock.tick(60)
def renderPops():
	window.fill((255,255,255))
	pygame.draw.rect(window, (187,173,160),(boardLocX,boardLocY,boardSize,boardSize))
	for x in range(0,4):
		for y in range(0,4):
			drawCell(x,y)
	for iterator in range(0,6):
		t = iterator/5
		window.fill((255,255,255))
		pygame.draw.rect(window, (187,173,160),(boardLocX,boardLocY,boardSize,boardSize))
		for x in range(0,4):
			for y in range(0,4):
				drawCell(x,y)
		for x in range(0,4):
			for y in range(0,4):
				if collisionBoard[x][y] == 0:
					drawCell(x,y,tempBoard[x][y])
				else:
					drawCell(x,y,tempBoard[x][y],1.3 -.6*abs(t-.5))
		if validMove == 1:
			drawCell(newTileLoc[0],newTileLoc[1],newTileVal,1.3 - .6*abs(t-.5))
		pygame.display.update()
		pygame.event.get()
		clock.tick(45)

def drawCell(locX,locY, val = 0,magnification = 1):
	color = colorKey[val]
	cellCenter = (boardLocX + borderThickness + (borderThickness+cellSize)*locX + cellSize/2, boardLocY + borderThickness + (borderThickness+cellSize)*locY + cellSize/2)
	pygame.draw.rect(window, color, (cellCenter[0] - (cellSize*magnification)/2,cellCenter[1] - (cellSize*magnification)/2, cellSize * magnification,cellSize * magnification))
	for x in range(0,2):
		for y in range(0,2):
			cornerLoc = (cellCenter[0] - (cellSize*magnification)/2 + x*(.97)*cellSize*magnification,cellCenter[1] - (cellSize*magnification)/2+y*(.97)*cellSize*magnification)
			pygame.draw.rect(window,(187,173,160), (cornerLoc[0],cornerLoc[1],.03*cellSize*magnification+1,.03*cellSize*magnification+1))
			pygame.draw.circle(window,color,(int(cornerLoc[0] + (1-x)*.03*cellSize*magnification),int(cornerLoc[1] + (1-y)*.03*cellSize*magnification)),int(.03*cellSize*magnification))
	if val != 0:
		numFont = pygame.font.SysFont('courier', int(cellSize*fontKey[val][0]))
		textSurface = numFont.render(str(val),True,fontKey[val][1])
		screen.blit(textSurface, (boardLocX + borderThickness + (borderThickness+cellSize)*locX + cellSize*fontKey[val][2][0] , boardLocY + borderThickness + (borderThickness+cellSize)*locY + cellSize*fontKey[val][2][1]))

directionKey = {
	1:'right',
	2:'left',
	3:'up',
	4:'down'
}

def Strategy2():
	highestScore = 0
	for direction in ['right','down','left','up']:
		isValidMove = False
		directionScore = 0
		processMove(direction)
		if validMove == 1:
			isValidMove = True
		reset()
		for trial in range(0,30):
			winPath = False
			trialValue = 0
			processMove(direction)
			i = 1
			while i < 5:
				if processMove(directionKey[randint(1,4)])[1] == 1:
#					print(direction,i,"tempScore:",tempScore,"gameLost:",tempGameLost,"tempTileCount:",tempTileCount)
#					print(trial,i,tempScore,tempGameLost,tempTileCount)
					i += 1
			if not tempGameLost:
				trialValue = tempScore - score
			if tempGameWon:
				trialValue *= 3
			if tempTileCount < tileCount:
				trialValue *= 3*(tileCount - tempTileCount)
#			print(direction,trial,trialValue,tempGameLost)
			directionScore += trialValue
			reset()
		directionScore /= 30	
		print(direction,"average:",directionScore)		
		if directionScore >= highestScore and isValidMove:
			winningDirection = direction
			highestScore = directionScore
		reset()
#	print(tempGameLost,gameLost)
	return winningDirection
							 	
def reset():
	global tempBoard, tempTileCount, tempScore, tempGameWon, tempGameLost
	tempBoard = [col[:] for col in board]
	tempTileCount = tileCount
	tempScore = score
	tempGameWon = gameWon
	tempGameLost = gameLost

board[randint(0,3)][randint(0,3)] = 2
tempBoard = [col[:] for col in board]
printBoard()
drawBoard()
pygame.display.update()
running = 1
noMove = False
while(running==1):
	for event in pygame.event.get():
		if event.type is KEYDOWN:
			if event.key == pygame.K_q:
				running = 0
			else:
				if event.key == pygame.K_RIGHT:
					latestDirection = 'right'
				elif event.key == pygame.K_LEFT:
					latestDirection = 'left'
				elif event.key == pygame.K_UP:
					latestDirection = 'up'
				elif event.key == pygame.K_DOWN:
					latestDirection = 'down'
				board = [col[:] for col in processMove(latestDirection)[0]]
				renderMotion(latestDirection)
				renderPops()
				score = tempScore
				tileCount = tempTileCount
				gameWon = tempGameWon
				gameLost = tempGameLost
				printBoard()
				drawBoard()
				if gameWon == 1:
					print("GAME WON")
					running = 0
				if gameLost:
					print("GAME OVER")
					running = 0


#while(running ==1):
#		for event in pygame.event.get():	
#			if event.type is KEYDOWN:
#				if event.key == pygame.K_q:
#					running = 0
#		latestdirection = Strategy2()
#		print(latestdirection)
#		board = [col[:] for col in processMove(latestdirection)[0]]
	#	renderMotion(latestdirection)
	#	renderPops()
#		score = tempScore
##		tileCount = tempTileCount
#		printBoard()
#		drawBoard()
#		if gameWon == 1:
#			print("GAME WON")
#			running =0
#		elif tileCount == 16:
#			noMove = True
#			for direction in ['right','left','down','up']:
#				processShift(direction)
#				if validMove ==1:
#					noMove = False
#		if noMove:
#			print("GAME OVER")
#			running = 0
#		clock.tick(60)				
