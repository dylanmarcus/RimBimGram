from graphics import *
import numpy as np
import math as math
import os


class Board:
    def __init__(self, solution=[[]], size=10, cellSize=20, offset=100):
        self.size = size
        self.cellSize = cellSize
        self.offset = offset
        self.cells = [[Cell(r, c, cellSize) for r in range(self.size)] for c in range(self.size)]
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

    def countCol(self, col):
        count1 = 0
        count2 = 0

        for idx in range(len(self.userBoard)):
            if self.userBoard[idx][col] == 1:
                count1 += 1

        for idx in range(len(self.solutionBoard)):
            if self.solutionBoard[idx][col] == 1:
                count2 += 1

        return count1 >= count2


    def colorCol(self, col, WIN, flag):
        greyRect = Rectangle(Point(self.cellSize * col + self.offset, 0),
                             Point(self.cellSize * col + (self.offset + self.cellSize),
                                   self.offset - 1))
        if flag == 1:
            greyRect.setFill(color_rgb(218, 218, 218))
            greyRect.setOutline(color_rgb(218, 218, 218))
        else:
            greyRect.setFill(color_rgb(240, 240, 240))
            greyRect.setOutline(color_rgb(240, 240, 240))

        greyRect.draw(WIN)

    def countRow(self, row):
        count1 = 0
        count2 = 0

        for idx in range(len(self.userBoard)):
            if self.userBoard[row][idx] == 1:
                count1 += 1

        for idx in range(len(self.solutionBoard)):
            if self.solutionBoard[row][idx] == 1:
                count2 += 1

        return count1 >= count2


    def colorRow(self, row, WIN, flag):
        greyRect = Rectangle(Point(0, self.cellSize * row + self.offset),
                             Point(self.offset - 1,
                                   self.cellSize * row + (self.offset + self.cellSize)))
        if flag == 1:
            greyRect.setFill(color_rgb(218, 218, 218))
            greyRect.setOutline(color_rgb(218, 218, 218))
        else:
            greyRect.setFill(color_rgb(240, 240, 240))
            greyRect.setOutline(color_rgb(240, 240, 240))

        greyRect.draw(WIN)


    def click(self, WIN):
        playing = True
        click = WIN.getMouse()
        if WIN.checkKey() == 'x':
            crossOut = True
        else:
            crossOut = False
        for row in range(self.size):
            for column in range(self.size):
                p1, p2 = self.getPoints(row, column)
                index = self.getIndex(click)

                if click.x > p1.x and click.x < p2.x and click.y > p1.y and click.y < p2.y:
                    if self.cells[row][column].state == 'blank':
                        if crossOut:
                            self.cells[row][column].state = 'crossedOut'
                        else:
                            self.cells[row][column].state = 'filled'
                            self.userBoard[row][column] = 1

                    elif self.cells[row][column].state == 'filled':
                        self.cells[row][column].state = 'blank'
                        self.userBoard[row][column] = 0

                    elif self.cells[row][column].state == 'crossedOut':
                        self.cells[row][column].state = 'blank'

                    self.cells[row][column].drawCell(p1, p2, WIN)


                    if len(self.solutionBoard) != 0:
                        if self.countCol(column):
                            self.colorCol(column, WIN, 1)
                        else:
                            self.colorCol(column, WIN, 0)

                        if self.countRow(row):
                            self.colorRow(row, WIN, 1)
                        else:
                            self.colorRow(row, WIN, 0)

                        self.columnSequence(WIN)
                        self.rowSequence(WIN)


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


        # print(self.userBoard)
        self.playMode(self.userBoard, WIN)

    def playMode(self, solution, WIN):
        self.solutionBoard = self.userBoard
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
                p1, p2 = self.getPoints(row, column)
                if self.cells[row][column].state == 'filled':
                    self.cells[row][column].state = 'blank'
                    self.cells[row][column].drawCell(p1, p2, WIN)

        playing = True

        self.userBoard = [[0 for i in range(self.size)] for i in range(self.size)]

        while playing:
            playing = self.click(WIN)


    def rowSequence(self, WIN):
        rowCount = 0
        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append(self.solutionBoard[r][c])
            sequence = self.sequence(row)


            anchor = self.offset - (len(sequence) * 3 + 5)
            halfCell = int(self.cellSize/2)

            rowText = Text(
                Point(anchor, self.cellSize * rowCount + (self.offset + halfCell)),
                sequence)

            if sequence == [0]:
                greyRect = Rectangle(Point(0, self.cellSize * rowCount + self.offset),
                                     Point(self.offset - 1, self.cellSize * rowCount + (self.offset + self.cellSize)))
                greyRect.setFill(color_rgb(218, 218, 218))
                greyRect.setOutline(color_rgb(218, 218, 218))
                greyRect.draw(WIN)

            rowText.setSize(halfCell)
            rowText.draw(WIN)
            rowCount += 1

    def columnSequence(self, WIN):
        colCount = 0
        for r in range(self.size):
            column = []
            for c in range(self.size):
                column.append(self.solutionBoard[c][r])
            sequence = self.sequence(column)

            halfCell = int(self.cellSize / 2)
            anchor = self.offset - (len(sequence) * self.cellSize) + halfCell
            for idx in range(len(sequence)):
                rowText = Text(
                    Point(self.cellSize * colCount + (self.offset + halfCell),
                          anchor + self.cellSize * idx),
                    sequence[idx])

                if sequence == [0]:
                    greyRect = Rectangle(Point(self.cellSize * colCount + self.offset, 0),
                                         Point(self.cellSize * colCount + (self.offset + self.cellSize),
                                               self.offset-1))
                    greyRect.setFill(color_rgb(218, 218, 218))
                    greyRect.setOutline(color_rgb(218, 218, 218))
                    greyRect.draw(WIN)

                rowText.setSize(halfCell)
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

    def showSolution(self, WIN):
        for x in range(len(self.solutionBoard)):
            for y in range(len(self.solutionBoard)):
                if self.solutionBoard[y][x] == 1:
                    p1, p2 = self.getPoints(x, y)
                    self.cells[x][y].state = 'filled'
                    self.userBoard[x][y] = 1
                    self.cells[x][y].drawCell(p1, p2, WIN)

class Cell:
    def __init__(self, row, column, size=20, state='blank'):
        self.state = state
        self.row = row
        self.column = column
        self.size = size

    def drawCell(self, p1, p2, WIN):
        cell = Rectangle(p1, p2)
        textPoint = Point(p1.x + self.size/2, p1.y + self.size/2)
        crossOutText = Text(textPoint, '')
        crossOutText.setSize(self.size)
        if self.state == 'filled':
            cell.setFill('green')
            crossOutText.setText('')
        elif self.state == 'crossedOut':
            crossOutText.setText('X')
        else:
            cell.setFill('white')
            crossOutText.setText('')

        crossOutText.draw(WIN)
        cell.draw(WIN)



def menu(WIN):

    width = int(WIN.getHeight()/2)
    height = int(WIN.getWidth()/10)
    buttonX = WIN.getWidth()/2 - (width / 2)
    buttonY = WIN.getHeight()/2

    playBoard = Rectangle(Point(buttonX, buttonY), Point(buttonX + width, buttonY + height))
    playBoard.setFill('blue')
    playBoardText = Text(Point(buttonX + (width / 2), buttonY + (height / 2)), 'PLAY')
    playBoardText.setTextColor('white')
    playBoard.draw(WIN)
    playBoardText.draw(WIN)

    newY = buttonY + height + 10

    createBoard = Rectangle(Point(buttonX, newY), Point(buttonX + width, newY + height))
    createBoard.setFill('blue')
    createBoardText = Text(Point(buttonX + (width/2), newY + (height/2)), 'CREATE')
    createBoardText.setTextColor('white')
    createBoard.draw(WIN)
    createBoardText.draw(WIN)

    newY = newY + height + 10

    uploadImage = Rectangle(Point(buttonX, newY), Point(buttonX + width, newY + height))
    uploadImage.setFill('blue')
    uploadImageText = Text(Point(buttonX + (width / 2), newY + (height / 2)), 'IMAGE')
    uploadImageText.setTextColor('white')
    uploadImage.draw(WIN)
    uploadImageText.draw(WIN)

    string = ''
    while string == '':
        click = WIN.getMouse()

        if buttonX < click.x < buttonX + width:
            if buttonY < click.y < buttonY + height:
                value = 'play'

        newY = buttonY + height + 10

        if buttonX < click.x < buttonX + width:
            if buttonY + height + 10 < click.y < newY + height:
                value = 'create'


        newY = newY + height + 10

        if buttonX < click.x < buttonX + width:
            if buttonY + ((height + 10) * 2) < click.y < newY + height:
                value = 'image'
                WIN.close()


        createBoard.undraw()
        createBoardText.undraw()
        playBoard.undraw()
        playBoardText.undraw()
        uploadImage.undraw()
        uploadImageText.undraw()
        return value

def selectBoard(WIN):
    home = Rectangle(Point(0, 0), Point(40, 20))
    home.setFill('green')
    home.setOutline('green')
    homeText = Text(Point(20, 10), "HOME")
    homeText.setSize(10)
    homeText.setTextColor('white')
    home.draw(WIN)
    homeText.draw(WIN)


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

        if 0 < click.x < 40:
            if 0 < click.y < 20:
                clear = Rectangle(Point(0, 0), Point(WIN.getHeight(), WIN.getWidth()))
                clear.setFill('white')
                clear.draw(WIN)
                menu(WIN)

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

    WIN.close()
    return newSeq

def imageToBoard():
    mona = Image(Point(0, 0), "mona.gif")
    avgColor = []

    for width in range(mona.getWidth()):
        for height in range(mona.getHeight()):
            list = mona.getPixel(width, height)
            sum = 0
            for val in list:
                sum += val
            sum /= 3
            if sum > 255/2:
                avgColor.append(0)
            else:
                avgColor.append(1)

    newSeq = [[0 for i in range(100)] for i in range(100)]

    list = []
    rowCount = 0
    for idx in range(len(avgColor)-1):

        list.append(avgColor[idx])
        if idx > 1 and (idx+1) % 100 == 0:
            #print(list)

            for idx2 in range(len(list)):
                newSeq[rowCount][idx2] = list[idx2]

            rowCount += 1
            list.clear()

    #print(newSeq)
    #print(len(newSeq[1]))

    return newSeq

def numToString(num):
    switcher = {
        0: "10 x 10",
        1: "15 x 15",
        2: "20 x 20",
        3: "25 x 25",
        4: "100 x 100"
    }
    return switcher.get(num)

def idxToSize(num):
    switcher = {
        0: 5,
        1: 10,
        2: 15,
        3: 20,
        4: 25,
        5: 100
    }
    return switcher.get(num)

def createMenu(WIN):

    home = Rectangle(Point(0, 0), Point(40, 20))
    home.setFill('green')
    home.setOutline('green')
    homeText = Text(Point(20, 10), 'HOME')
    homeText.setSize(10)
    homeText.setTextColor('white')
    home.draw(WIN)
    homeText.draw(WIN)

    width = 150
    height = 30
    buttonX = WIN.getWidth() / 2 - (width / 2)
    buttonY = WIN.getHeight() / 5

    button = Rectangle(Point(buttonX, buttonY), Point(buttonX + width, buttonY + height))
    button.setFill('blue')
    buttonText = Text(Point(buttonX + (width / 2), buttonY + (height / 2)), '5 X 5')
    buttonText.setTextColor('white')
    button.draw(WIN)
    buttonText.draw(WIN)

    for idx in range(5):
        cloneB = button.clone()
        cloneT = buttonText.clone()
        cloneB.move(0, (idx+1)*(height+10))
        cloneT.move(0, (idx+1)*(height+10))
        string = numToString(idx)
        cloneT.setText(string)
        cloneB.draw(WIN)
        cloneT.draw(WIN)


    string = ''
    while string == '':
        click = WIN.getMouse()
        if 0 < click.x < 40:
            if 0 < click.y < 20:
                clear = Rectangle(Point(0, 0), Point(WIN.getHeight(), WIN.getWidth()))
                clear.setFill('white')
                clear.draw(WIN)
                menu(WIN)

        for idx in range(6):
            if buttonX < click.x < buttonX + width:
                if buttonY + idx*(height+10) < click.y < (buttonY + idx*(height+10)) + height:
                    string = idxToSize(idx)

    WIN.close()
    return string


def main():
    WIN = GraphWin('Menu', 300, 300)
    string = menu(WIN)

    if string == 'play':
        seq = selectBoard(WIN)
        board = Board(seq)
        board.solutionBoard = seq
        board.userBoard = seq

        windowSize = board.size * board.cellSize + board.offset
        WIN = GraphWin('Game', windowSize, windowSize)
        board.drawBoard(WIN)

        board.playMode(seq, WIN)

    if string == 'create':
        size = createMenu(WIN)
        board = Board([], size)
        #board.size = size
        windowSize = board.size * board.cellSize + board.offset
        WIN = GraphWin("Game", windowSize, windowSize)
        board.drawBoard(WIN)
        print(board.size)
        print(len(board.userBoard))
        board.creationMode(WIN)

    if string == 'image':
        seq = imageToBoard()
        print(seq)
        board = Board(seq, 100, 10, 500)
        windowSize = board.size * board.cellSize + board.offset
        WIN = GraphWin('Game', windowSize, windowSize)
        board.size = 100
        board.solutionBoard = seq
        board.cellSize = 10
        board.offset = 500
        board.drawBoard(WIN)
        board.userBoard = seq
        board.showSolution(WIN)

        board.playMode(seq, WIN)

    WIN.getMouse()
    WIN.close()


main()
