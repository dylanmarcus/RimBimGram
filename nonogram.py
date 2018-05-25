from graphics import *
import numpy as np


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
		playing = True
		click = WIN.getMouse()
		for row in range(self.size):
			for column in range(self.size):
				p1, p2 = self.getPoints(row, column)
				if click.x > p1.x and click.x < p2.x and click.y > p1.y and click.y < p2.y:
					if self.cells[row][column].state == 'blank':
						self.cells[row][column].state = 'filled'
						self.userBoard[row][column] = 1
					elif self.cells[row][column].state == 'filled':
						self.cells[row][column].state = 'blank'
						self.userBoard[row][column] = 0
					self.cells[row][column].drawCell(p1, p2, WIN)
				if click.x < 20 and click.y < 20:
					playing = False
		return playing




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
	board = Board([1])
	windowSize = board.size * board.cellSize + board.offset
	WIN = GraphWin("Game", windowSize, windowSize)
	board.drawBoard(WIN)
	playing = True
	while playing:
		playing = board.click(WIN)
		print np.matrix(board.userBoard)
	WIN.getMouse()
	WIN.close()


main()