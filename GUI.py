from tkinter import *
import numpy as np
from Board import Board
import types

MODE = 1
BOARD_SIZE = 500
GAME_SIZE = 4
DEPTH = 4
MINMAX = 'MINMAX'
ALPHA_BETA_PRUNING = 'ALPHA_BETA_PRUNING'
ALGORITHM = MINMAX


class Radiobar(Frame):
    def __init__(self, parent=None, picks=[], fill=X, labelText='', anchor=W):
        Frame.__init__(self, parent)
        self.var = IntVar()
        self.var.set(MODE)
        label = Label(self, text=labelText)
        label.pack(fill=fill, anchor=anchor, expand=YES)
        for pick in picks:
            rad = Radiobutton(self, text=pick[0], value=pick[1], variable=self.var, command=self.changeMode)
            rad.pack(anchor=anchor, expand=YES)

    def state(self):
        return self.var.get()

    def changeMode(self):
        global MODE
        MODE = self.var.get()

class RadiobarAlgorithm(Frame):
    def __init__(self, parent=None, picks=[], fill=X, labelText='', anchor=W):
        Frame.__init__(self, parent)
        self.var = StringVar()
        self.var.set(ALGORITHM)
        label = Label(self, text=labelText)
        label.pack(fill=fill, anchor=anchor, expand=YES)
        for pick in picks:
            rad = Radiobutton(self, text=pick[0], value=pick[1], variable=self.var, command=self.changeMode)
            rad.pack(anchor=anchor, expand=YES)

    def state(self):
        return self.var.get()

    def changeMode(self):
        global ALGORITHM
        ALGORITHM = self.var.get()

class Scalebar(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.var = IntVar()
        scale = Scale(self, from_=3, to=50, label='Rozmiar planszy',
                      orient=HORIZONTAL, command=self.changeBoardSize, variable=self.var)
        scale.pack(expand=1, fill=X, pady=10, padx=5)

    def changeBoardSize(self, *args):
        global GAME_SIZE
        GAME_SIZE = self.var.get()

    def setScaleValue(self, value):
        self.var.set(value)

class ButtonField(Frame):
    def __init__(self, parent, width, height, command):
        Frame.__init__(self, parent, width=width, height=height)
        self.pack_propagate(0)
        self.button = Button(self, command=command)
        self.button.pack(fill=BOTH, expand=1)


class GUI:
    def __init__(self):
        self.app = Tk()
        self.app.title('Stratego')
        self.app.resizable(width=False, height=False)
        self.app.geometry('1000x500')
        self.myPoints = 0
        self.opponentPoints = 0
        self.initBoard()
        self.initGameWithMode(MODE)
        self.update()

    def initBoard(self):
        self.board = Board(None, GAME_SIZE, DEPTH)
        self.buttons = np.zeros((GAME_SIZE, GAME_SIZE), dtype=object)
        self.app.grid_columnconfigure(0, weight=0)
        self.app.grid_columnconfigure(1, weight=0)

        self.frameBoard = Frame(self.app, width=BOARD_SIZE, height=BOARD_SIZE)
        self.frameSettings = Frame(self.app, width=BOARD_SIZE, height=BOARD_SIZE)

        self.frameBoard.grid(row=0, column=0, sticky="nsew")
        self.frameSettings.grid(row=0, column=1, sticky="nsew")
        self.frameBoard.grid_propagate(False)

        self.frameSettings.grid_propagate(False)
        self.frameSettings.grid_columnconfigure(0, weight=1)
        self.frameSettings.grid_columnconfigure(1, weight=1)
        handler = lambda: self.reset()
        button = Button(self.frameSettings, text='reset', command=handler)
        button.grid(row=2, column=1, sticky="WE", padx=20, pady=20)

        radioOptions = [('Człowiek - Człowiek', 1), ('Człowiek  - Komputer', 2), ('Komputer - Komputer', 3)]
        radiobar = Radiobar(self.frameSettings, radioOptions, labelText='Tryb gry')
        radiobar.grid(row=0, column=0, sticky="WE", padx=20, pady=20)
        scalebar = Scalebar(self.frameSettings)
        scalebar.setScaleValue(GAME_SIZE)
        scalebar.grid(row=2, column=0, sticky="WE", padx=20, pady=20)

        radiobarAlgorithm = RadiobarAlgorithm(self.frameSettings, [(MINMAX, MINMAX), (ALPHA_BETA_PRUNING, ALPHA_BETA_PRUNING)], labelText='Algorytm')
        radiobarAlgorithm.grid(row=0, column=1, sticky="WE", padx=20, pady=20)

        resultsLabel = Label(self.frameSettings, text="Wynik gry dla graczy", font=("Helvetica", 16))
        humanScoreLabel = Label(self.frameSettings, text="Gracz 1: ")
        computerScoreLabel = Label(self.frameSettings, text="Gracz 2: ")
        self.humanScore = Label(self.frameSettings, text="0")
        self.computerScore = Label(self.frameSettings, text="0")
        resultsLabel.grid(row=3, columnspan=2, padx=20, pady=20)
        humanScoreLabel.grid(row=4, column=0, padx=20, pady=20)
        computerScoreLabel.grid(row=4, column=1, padx=20, pady=20)
        self.humanScore.grid(row=5, column=0, padx=20, pady=20)
        self.computerScore.grid(row=5, column=1, padx=20, pady=20)

    def initGameWithMode(self, mode=MODE, algorithm=MINMAX):
        gameSize = self.board.size
        modeHandler = None
        for x in range (gameSize):
            for y in range (gameSize):
                if mode == 1:
                    modeHandler = lambda x=x, y=y: self.moveHumanHuman(x, y, True)
                elif mode == 2:
                    modeHandler = lambda x=x, y=y: self.moveHumanComp(x, y, algorithm)

                handler = modeHandler
                buttonSize =  int(BOARD_SIZE/self.board.size)
                f = ButtonField(self.frameBoard, buttonSize, buttonSize, handler)
                f.grid(row=x, column=y)
                self.buttons[x][y] = f
        if mode == 3:
            self.moveCompComp(self.board.fieldsNr, True, algorithm)

    def reset(self):
        self.initBoard()
        self.myPoints = 0
        self.opponentPoints = 0
        self.initGameWithMode(MODE, ALGORITHM)
        self.update()

    def moveHumanHuman(self, x, y, player):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x, y)
        if player:
            self.myPoints += self.board.countPoints((x, y))
        else:
            self.opponentPoints += self.board.countPoints((x, y))

        self.update()
        self.app.config(cursor="")

    def moveCompComp(self, fieldsNr, player, algorithm):
        if(algorithm == MINMAX):
            move = self.board.best(self.board.depth)
        else:
            move = self.board.bestwithpruning(self.board.depth)

        if move:
            self.app.update()
            self.board = self.board.move(*move, None)
            if player:
                self.myPoints += self.board.countPoints(move)
            else:
                self.opponentPoints += self.board.countPoints(move)

        self.update()
        if fieldsNr > 0:
            self.moveCompComp(fieldsNr - 1, not player, algorithm)

    def moveHumanComp(self, x, y, algorithm):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x, y, None)
        self.myPoints += self.board.countPoints((x, y))
        self.update()
        if (algorithm == MINMAX):
            move = self.board.best(self.board.depth)
        else:
            move = self.board.bestwithpruning(self.board.depth)
        if move:
            self.board = self.board.move(*move, None)
            self.opponentPoints +=  self.board.countPoints(move)
            self.update()
        self.app.config(cursor="")

    def updatePoints(self, humanPoints, compPoints):
        humanPoints.config(text=str(self.myPoints))
        compPoints.config(text=str(self.opponentPoints))

    def update(self):
        gameSize = self.board.size
        for x in range(gameSize):
            for y in range(gameSize):
                boardField = self.board.fields[x][y]
                if boardField == 1:
                    self.buttons[x][y].button.configure(bg='Blue')
                elif boardField == -1:
                    self.buttons[x][y].button.configure(bg='Pink')
                if boardField == self.board.empty:
                    self.buttons[x][y].button['state'] = 'normal'
                else:
                    self.buttons[x][y].button['state'] = 'disabled'

        self.updatePoints(self.humanScore, self.computerScore)
            # winning = self.board.won()
            # if winning:
            #     for x, y in winning:
            #         self.buttons[x][y].button.configure(bg='purple')
            #     for x in range(gameSize):
            #         for y in range(gameSize):
            #             self.buttons[x][y].button['state'] = 'disabled'
            # for x in range(gameSize):
            #     for y in range(gameSize):
            #         self.buttons[x][y].button.update()

    def mainloop(self):
        self.app.mainloop()