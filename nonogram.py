from graphics import *
import numpy as np
import math as math
import os


class Board:
    def __init__(self, solution=[[]], size=10, cellSize=20, offset=100):
        self.size = size
        self.cellSize = cellSize
        self.offset = offset
        self.cells = [[Cell(r, c) for r in range(self.size)] for c in range(self.size)]
        self.solutionBoard = solution
        self.userBoard = [[0 for i in range(self.size)] for i in range(self.size)]
        self.button = Rectangle(Point(0, 0), Point(self.cellSize * 2, self.cellSize))
        self.buttonText = Text(self.button.getCenter(), '')


    def getPoints(self, row, column):
        p1 = Point(
            (column * self.cellSize + self.offset),
            (row * self.cellSize + self.offset))
        p2 = Point(
            ((column + 1) * self.cellSize + self.offset),
            ((row + 1) * self.cellSize + self.offset))
        return p1, p2

    def drawBoard(self, WIN):
        button = Rectangle(Point(0, 0), Point(self.cellSize*2, self.cellSize))

        for row in range(self.size):
            for column in range(self.size):
                p1, p2 = self.getPoints(row, column)
                self.cells[row][column].drawCell(p1, p2, WIN)

    def getIndex(self, click):

        index = math.floor((click.x - self.offset) / self.cellSize)
        index = index + ((math.floor((click.y - self.offset) / self.cellSize) * self.size))
        return index

    def click(self, WIN):
        playing = True
        click = WIN.getMouse()
        for row in range(self.size):
            for column in range(self.size):
                p1, p2 = self.getPoints(row, column)
                index = self.getIndex(click)

                if click.x > p1.x and click.x < p2.x and click.y > p1.y and click.y < p2.y:
                    if self.cells[row][column].state == 'blank':
                        self.cells[row][column].state = 'filled'
                        self.userBoard[row][column] = 1


                    elif self.cells[row][column].state == 'filled':
                        self.cells[row][column].state = 'blank'
                        self.userBoard[row][column] = 0
                    self.cells[row][column].drawCell(p1, p2, WIN)

                    if self.userBoard == self.solutionBoard:
                        playing = False

                        winner = Rectangle(Point(0, 0), Point(WIN.getHeight(), WIN.getWidth()))
                        winner.setFill('white')
                        winnerText = Text(winner.getCenter(), 'WINNER!')
                        winner.draw(WIN)
                        winnerText.draw(WIN)
                p2 = self.button.getP2()
                buttonX = p2.x
                buttonY = p2.y

                if click.x < buttonX and click.y < buttonY:
                    playing = False
        return playing

    def creationMode(self, WIN):

        self.button.setFill('blue')
        self.buttonText.setText('save')
        self.buttonText.setTextColor("white")
        self.button.draw(WIN)
        self.buttonText.draw(WIN)

        creating = True
        while creating:
            creating = self.click(WIN)


        #print(self.userBoard)
        self.playMode(self.userBoard, WIN)

    def playMode(self, solution, WIN):
        #self.userBoard = solution
        self.rowSequence(WIN)
        self.columnSequence(WIN)

        self.button.undraw()
        self.buttonText.undraw()
        self.solutionBoard = solution
        self.button.setFill('red')
        self.buttonText.setText('quit')
        self.buttonText.setTextColor("white")
        self.button.draw(WIN)
        self.buttonText.draw(WIN)

        for row in range(self.size):
            for column in range(self.size):
                self.cells[row][column].state = 'blank'


        playing = True

        board = Board()
        board.drawBoard(WIN)
        self.userBoard = [[0 for i in range(self.size)] for i in range(self.size)]

        while playing:
            playing = self.click(WIN)

    def rowSequence(self, WIN):
        rowCount = 0
        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append(self.userBoard[r][c])
            sequence = self.sequence(row)

            anchor = self.offset / 2
            rowText = Text(
                Point(anchor + (self.offset / (len(sequence) + 2)), self.cellSize * rowCount + (90 + self.cellSize)),
                sequence)
            rowText.setSize(10)
            rowText.draw(WIN)
            rowCount += 1

    def columnSequence(self, WIN):
        colCount = 0
        for r in range(self.size):
            column = []
            for c in range(self.size):
                column.append(self.userBoard[c][r])
            sequence = self.sequence(column)

            anchor = self.offset - (len(sequence) * self.cellSize) + (self.cellSize / 2)
            for idx in range(len(sequence)):
                rowText = Text(Point(self.cellSize * colCount + (90 + self.cellSize), anchor + 20 * idx), sequence[idx])
                rowText.setSize(10)
                rowText.draw(WIN)
            colCount += 1

    def sequence(self, a):
        sequence = []
        count = 0
        for i in range(len(a)):
            if i < len(a) - 1:
                if a[i] == 1:
                    count += 1
                if a[i + 1] == 0:
                    if count != 0:
                        sequence.append(count)
                        count = 0
            else:
                if a[i] == 1:
                    count += 1
                if count != 0:
                    sequence.append(count)
        if len(sequence) == 0:
            sequence.append(0)
        return sequence


    def boardToString(self):
        string = str(self.userBoard)
        simpleArray = []

        for idx in string:
            if idx == 0 or idx == 1:
                simpleArray.append(idx)
        return simpleArray


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


def menu():
    WIN = GraphWin("Menu", 300, 300)
    width = 150
    height = 30
    buttonX1 = WIN.getWidth()/2 - (width / 2)
    buttonY1 = WIN.getHeight()/2
    buttonX2 = WIN.getWidth()/2 - (width / 2)
    buttonY2 = WIN.getHeight()/2 + height + 10

    playBoard = Rectangle(Point(buttonX1, buttonY1), Point(buttonX1 + width, buttonY1 + height))
    playBoard.setFill('blue')
    playBoardText = Text(Point(buttonX1 + (width / 2), buttonY1 + (height / 2)), 'PLAY')
    playBoardText.setTextColor('white')
    playBoard.draw(WIN)
    playBoardText.draw(WIN)


    createBoard = Rectangle(Point(buttonX2, buttonY2), Point(buttonX2 + width, buttonY2 + height))
    createBoard.setFill('blue')
    createBoardText = Text(Point(buttonX2 + (width/2), buttonY2 + (height/2)), 'NEW BOARD')
    createBoardText.setTextColor('white')
    createBoard.draw(WIN)
    createBoardText.draw(WIN)

    string = ''
    while string == '':
        click = WIN.getMouse()

        if buttonX1 < click.x < buttonX1 + width:
            if buttonY1 < click.y < buttonY1 + height:
                createBoard.undraw()
                createBoardText.undraw()
                playBoard.undraw()
                playBoardText.undraw()
                return 'play', WIN

        if buttonX2 < click.x < buttonX2 + width:
            if buttonY2 < click.y < buttonY2 + height:
                createBoard.undraw()
                createBoardText.undraw()
                playBoard.undraw()
                playBoardText.undraw()
                return 'create', WIN

def selectBoard(WIN):
    all_files = os.listdir("sequences/")

    width = 150
    height = 30

    for idx in range(len(all_files)):
        buttonX = WIN.getWidth() / 2 - (width / 2)
        buttonY = WIN.getHeight() / 3 + (height * idx) + (15 * idx)
        chooseBoard = Rectangle(Point(buttonX, buttonY), Point(buttonX + width, buttonY + height))
        chooseBoard.setFill('blue')
        chooseBoardText = Text(Point(buttonX + (width / 2), buttonY + (height / 2)), all_files[idx])
        chooseBoardText.setTextColor('white')
        chooseBoard.draw(WIN)
        chooseBoardText.draw(WIN)

    string = ''
    while string == '':
        click = WIN.getMouse()
        for idx in range(len(all_files)):
            buttonX = WIN.getWidth() / 2 - (width / 2)
            buttonY = WIN.getHeight() / 3 + (height * idx) + (15 * idx)

            if (buttonX < click.x < buttonX + width):
                if (buttonY < click.y < buttonY + height):
                    index = idx
                    string = 'CHRIST'

    with open(os.path.join('sequences/', all_files[index]), 'rt') as fd:
        sequence = fd.readline()

    clear = Rectangle(Point(0, 0), Point(WIN.getHeight(), WIN.getWidth()))
    clear.setFill('white')
    clear.draw(WIN)

    seq = []
    for idx in sequence:
        if idx == '1':
            seq.append(1)
        elif idx == '0':
            seq.append(0)

    size = int(len(seq)/len(seq))
    # CHANGE THE HARD CODING LATER!


    newSeq = [[0 for i in range(10)] for i in range(10)]
    print(len(newSeq))
    print()
    print()

    list = []
    rowCount = 0
    for idx in range(len(seq)-1):

        list.append(seq[idx])
        if idx > 1 and (idx+1) % 10 == 0:
            print(list)

            for idx2 in range(len(list)):
                newSeq[rowCount][idx2] = list[idx2]

            rowCount += 1
            list.clear()

    print(newSeq)
    print(len(newSeq[0]))

    return newSeq


def main():
    string, WIN = menu()

    if string == 'play':
        seq = selectBoard(WIN)
        #print(seq)
        board = Board(seq)
        board.solutionBoard = seq
        board.userBoard = seq
        board.playMode(seq, WIN)

    #print(seq)

    #if string == 'create':
    #    createboard()
    if string == 'create':
        board = Board()
        windowSize = board.size * board.cellSize + board.offset
        WIN = GraphWin("Game", windowSize, windowSize)

        board.drawBoard(WIN)
        board.creationMode(WIN)
    WIN.getMouse()
    WIN.close()


main()
