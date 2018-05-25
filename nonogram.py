from graphics import *


class Board:
	def __init__(self, solution, size = 10, cellSize = 20, offset = 100):
		self.size = size
		self.cellSize = cellSize
		self.offset = offset
		self.cells = [[Cell(r ,c) for r in range(self.size)] for c in range(self.size)]
		self.solutionBoard = solution
		self.userBoard = [[0 for i in range(self.size)] for i in range(self.size)]


	def getPoints(self, row, column):
		p1 = Point(
			(column * self.cellSize + self.offset),
			(row * self.cellSize + self.offset))
		p2 = Point(
			((column+1) * self.cellSize + self.offset),
			((row+1) * self.cellSize + self.offset))
		return p1, p2


	def drawBoard(self, WIN):
		for row in range(self.size):
			for column in range(self.size):	
				p1, p2 = self.getPoints(row, column)
				self.cells[row][column].drawCell(p1, p2, WIN)


	def click(self, WIN):
		click = WIN.getMouse()
		# figure out where the fuck the shit does the stuff
		# change the fucking user board
		# draw the god damned new piece of shit cell



class Cell:
	def __init__(self, row, column, state = 'blank'):
		self.state = state
		self.row = row
		self.column = column

	def getRow(self):
		return self.row


	def getColumn(self):
		return self.column


	def drawCell(self, p1, p2, WIN):
		cell = Rectangle(p1, p2)
		if self.state == 'filled':
			cell.setFill('green')
		elif self.state == 'crossedOut':
			cell.setFill('red')
		else:
			cell.setFill('white')
		cell.draw(WIN)



def main():
	board = Board()
	windowSize = board.size * board.cellSize + board.offset
	WIN = GraphWin("Game", windowSize, windowSize)
	board.drawBoard(WIN)
	WIN.getMouse()
	WIN.close()


main()