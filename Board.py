import sys
import numpy as np
if sys.version_info >= (3, 0):
  from tkinter import *
else:
  from Tkinter import *
from copy import deepcopy
from GUI import *
class Board:
  
  def __init__(self,other=None):
    self.player = 1
    self.opponent = -1
    self.empty = 0
    self.size = 4
    self.fieldsNr = self.size*self.size
    self.fields = np.zeros((self.size, self.size), dtype=int)
    if other:
      self.__dict__ = deepcopy(other.__dict__)

  def move(self,x,y):
    board = Board(self)
    board.fields[x][y] = board.player
    (board.player,board.opponent) = (board.opponent,board.player)
    return board
  
  def __minimax(self, player, depth):
    gameSize=self.size
    if self.won():
      if player:
        return (-1,None)
      else:
        return (+1,None)
    elif self.tied():
      return (0,None)
    elif player:        # kiedy jaa
      best = (-2, None)
      if (depth != 0):
          for x in range(gameSize):
              for y in range(gameSize):
                if self.fields[x][y]==self.empty:
                  value = self.move(x,y).__minimax(not player, depth - 1)[0]
                  if value>best[0]:
                    best = (value,(x,y))
      if best[1] == None:
          best = (best[0], self.findEmpty())
      return best
    else:           # kiedy przeciwnik
      best = (+2, None)
      if (depth != 0):
          for x in range(gameSize):
              for y in range(gameSize):
                if self.fields[x][y]==self.empty:
                  value = self.move(x,y).__minimax(not player, depth - 1)[0]
                  if value<best[0]:
                    best = (value,(x,y))
      if best[1] == None:
          best = (best[0], self.findEmpty())
      return best
  
  def best(self, depth):
    return self.__minimax(True, depth)[1]
  
  def tied(self):
      gameSize = self.size
      for x in range(gameSize):
          for y in range(gameSize):
            if self.fields[x][y]==self.empty:
                return False
      return True

  def findEmpty(self):
      gameSize = self.size
      for x in range(gameSize):
          for y in range(gameSize):
              if self.fields[x, y] == self.empty:
                  return (x, y)
      return None
  def won(self):
    # horizontal
    for y in range(self.size):
      winning = []
      for x in range(self.size):
        if self.fields[x,y] == self.opponent:
          winning.append((x, y))
      if len(winning) == self.size:
        return winning
    # vertical
    for x in range(self.size):
      winning = []
      for y in range(self.size):
        if self.fields[x,y] == self.opponent:
          winning.append((x, y))
      if len(winning)  == self.size:
        return winning
    # diagonal
    winning = []
    for y in range(self.size):
      x = y
      if self.fields[x,y] == self.opponent:
        winning.append((x, y))
        if len(winning)  == self.size:
          return winning
    # other diagonal
    winning = []
    for y in range(self.size):
      x = self.size-1-y
      if self.fields[x,y] == self.opponent:
        winning.append((x, y))
    if len(winning) == self.size:
      return winning
    # default
    return None
  
  # def __str__(self):
  #   string = ''
  #   for y in range(self.size):
  #     for x in range(self.size):
  #       string+=self.fields[x,y]
  #     string+="\n"
  #   return string



if __name__ == '__main__':
  GUI().mainloop()