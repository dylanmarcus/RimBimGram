from graphics import *
import numpy as np


class Board:
    def __init__(self, solution=[[]], size=10, cellSize=20, offset=100):
        self.size = size
        self.cellSize = cellSize
        self.offset = offset
        self.cells = [[Cell(r, c) for r in range(self.size)] for c in range(self.size)]
        self.solutionBoard = solution
        self.userBoard = [[0 for i in range(self.size)] for i in range(self.size)]
        self.button = Rectangle(Point(0, 0), Point(self.cellSize * 2, self.cellSize))
        self.buttonText = Text(Point(self.cellSize / 10, self.cellSize / 10), '')


    def getPoints(self, row, column):
        p1 = Point(
            (column * self.cellSize + self.offset),
            (row * self.cellSize + self.offset))
        p2 = Point(
            ((column + 1) * self.cellSize + self.offset),
            ((row + 1) * self.cellSize + self.offset))
        return p1, p2

    def drawBoard(self, WIN):
        button = Rectangle(Point(0,0), Point(20,20))
        button.setFill('blue')
        button.draw(WIN)
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


    def creationMode(self, WIN):
        self.button.setFill('blue')
        self.buttonText.setText('save')
        self.buttonText.draw(WIN)

        creating = True
        while creating:
            creating = self.click(WIN)
            print np.matrix(self.userBoard)
        file = open('solution.txt', 'w')
        string = str(self.userBoard)
        file.write(string)
        self.rowSequence(WIN)
        #boardArray = self.boardToString()
        #self.colSequence(boardArray, WIN)


    # def boardToString(self):
    #     string = str(self.userBoard)
    #     # for row in range(self.size):
    #     #     for column in range(self.size):
    #     #         string += str(self.userBoard[row][column])
    #     return string

    def playMode(self, solution, WIN):
        self.solutionBoard = solution
        self.button.setFill('red')
        self.buttonText.setText('quit')
        self.buttonText.draw(WIN)

    def boardToString(self):
        string = str(self.userBoard)
        simpleArray = []

        for idx in string:
            if idx == 0 or idx == 1:
                simpleArray.append(idx)
        return simpleArray


    def colSequence(self, array, WIN):
        sequence = [[]]
        subSequence = []

        for arrayIdx in range(len(array)):
            subSequence.append(arrayIdx)
            if arrayIdx % self.size == 0:
                sequence.append(subSequence)
                subSequence = []

        colSequence = []
        colCount = 0
        counter = 0

        for idx in range(self.size):
            for arrayIdx in range(self.size):
                if sequence[idx][arrayIdx] == '1':
                    counter += 1

                if idx != len(array) - 1:
                    if sequence[idx] == '0':
                        colSequence.append(sequence[idx])
                    counter = 0

            anchor = self.offset - (len(sequence) * 10) - 5
            colText = Text(Point(self.cellSize * colCount + (90 + self.cellSize), anchor), sequence)
            colText.setSize(10)
            colText.draw(WIN)
            colSequence = [[]]
            colCount += 1


    def rowSequence(self, WIN):
        sequence = []
        string = str(self.userBoard)
        counter = 0
        rowCount = 0;

        for idx in range(len(string)):

                if string[idx] == '1':
                    counter += 1

                if idx != len(string) - 1:

                    if string[idx] == '0' or string[idx+1] == ']':
                        if counter != 0:
                            sequence.append(counter)

                        counter = 0

                    if string[idx] == ']':

                        print(sequence)
                        anchor = self.offset - (len(sequence)*10) - 5
                        if len(sequence) == 0:
                            sequence.append(0)
                        rowText = Text(Point(anchor, self.cellSize * rowCount + (90 + self.cellSize)), sequence)
                        rowText.setSize(10)
                        rowText.draw(WIN)
                        rowCount += 1
                        sequence = []









class Cell:
    def __init__(self, row, column, state='blank'):
        self.state = state
        self.row = row
        self.column = column


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
    board.creationMode(WIN)

    # playing = True
    # while playing:
    #     playing = board.click(WIN)
    #     print
    #     print np.matrix(board.userBoard)
    WIN.getMouse()
    WIN.close()


main()
