from tkinter import *
import numpy as np
from Board import Board
import types

MODE = 1
BOARD_SIZE = 500
GAME_SIZE = 4

class Radiobar(Frame):
    def __init__(self, parent=None, picks=[], fill=X, labelText='', anchor=W, ref=NONE):
        Frame.__init__(self, parent)
        self.resetOptions = types.MethodType(ref.reset.__func__, ref)
        self.var = IntVar()
        self.var.set(picks[0][1])
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
        self.resetOptions()

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
        self.board = Board()
        self.myPoints = 0
        self.opponentPoints = 0
        self.changeGameSize()
        self.initGameWithMode(MODE)
        self.update()

    def changeGameSize(self):
        self.board.size = GAME_SIZE
        self.board.fieldsNr = self.board.size * self.board.size
        self.board.fields = np.zeros((self.board.size, self.board.size), dtype=int)
        self.buttons = np.zeros((GAME_SIZE, GAME_SIZE), dtype=object)
        self.app.grid_columnconfigure(0, weight=0)
        self.app.grid_columnconfigure(1, weight=0)

        self.frameBoard = Frame(self.app, background="Blue", width=BOARD_SIZE, height=BOARD_SIZE)
        self.frameSettings = Frame(self.app, width=BOARD_SIZE, height=BOARD_SIZE)

        self.frameBoard.grid(row=0, column=0, sticky="nsew")
        self.frameSettings.grid(row=0, column=1, sticky="nsew")
        self.frameBoard.grid_propagate(False)

        self.frameSettings.grid_propagate(False)
        self.frameSettings.grid_columnconfigure(0, weight=1)
        self.frameSettings.grid_columnconfigure(1, weight=1)
        handler = lambda: self.reset()
        button = Button(self.frameSettings, text='reset', command=handler)
        button.grid(row=0, column=1, sticky="WE", padx=20, pady=20)

        radioOptions = [('Człowiek - Człowiek', 1), ('Człowiek  - Komputer', 2), ('Komputer - Komputer', 3)]
        radiobar = Radiobar(self.frameSettings, radioOptions, labelText='Tryb gry', ref=self)
        radiobar.grid(row=0, column=0, sticky="WE", padx=20, pady=20)
        scalebar = Scalebar(self.frameSettings)
        scalebar.setScaleValue(GAME_SIZE)
        scalebar.grid(row=2, columnspan=2, sticky="WE", padx=20, pady=20)

    def initGameWithMode(self, mode=MODE):
        gameSize = self.board.size
        for x in range (gameSize):
            for y in range (gameSize):
                if mode == 1:
                    modeHandler = lambda x=x, y=y: self.moveHumanHuman(x, y)
                elif mode == 2:
                    modeHandler = lambda x=x, y=y: self.moveHumanComp(x, y)
                else:
                    modeHandler = lambda x=x, y=y: self.moveCompComp(self.board.fieldsNr)
                handler = modeHandler
                buttonSize =  int(BOARD_SIZE/self.board.size)
                f = ButtonField(self.frameBoard, buttonSize, buttonSize, handler)
                f.grid(row=x, column=y)
                self.buttons[x][y] = f
        if mode == 3:
            self.moveCompComp(self.board.fieldsNr)

    def reset(self):
        self.board = Board()
        self.changeGameSize()
        self.initGameWithMode(MODE)
        self.myPoints = 0
        self.opponentPoints = 0
        self.update()

    def moveHumanHuman(self, x, y):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x, y)
        self.update()
        self.app.config(cursor="")

    def moveCompComp(self, fieldsNr):
        move = self.board.best(self.board.depth)
        if move:
            self.board = self.board.move(*move)
            self.update()
        self.app.config(cursor="")
        if fieldsNr > 0:
            self.moveCompComp(fieldsNr - 1)

    def moveHumanComp(self, x, y):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x, y)
        self.myPoints += self.board.countPoints((x, y))
        print('ja:', self.myPoints, ' komp:', self.opponentPoints)
        self.update()
        move = self.board.bestwithpruning(self.board.depth)
        #move = self.board.best(self.board.depth)
        if move:
            self.board = self.board.move(*move)
            self.opponentPoints +=  self.board.countPoints((x, y))
            print('ja:', self.myPoints, ' komp:', self.opponentPoints)
            self.update()
        self.app.config(cursor="")

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