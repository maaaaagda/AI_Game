import sys
import numpy as np
import math

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
    self.size = 3
    self.depth = 4
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
    elif depth == 0:
        if player:
            return (0, self.findEmpty())
        else:
            return (0, self.findEmpty())
    elif self.tied():
      return (0,None)
    elif player:        # kiedy ja
      best = (-math.inf, None)
      if (depth != 0):
          for x in range(gameSize):
              for y in range(gameSize):
                if self.fields[x][y]==self.empty:
                   value = self.move(x,y).__minimax(not player, depth - 1)[0]
                   if value>best[0]:
                     best = (value,(x,y))

      return best
    else:           # kiedy przeciwnik
      best = (+math.inf, None)
      if (depth != 0):
          for x in range(gameSize):
              for y in range(gameSize):
                if self.fields[x][y]==self.empty:
                  value = self.move(x,y).__minimax(not player, depth - 1)[0]
                  if value<best[0]:
                      best = (value,(x,y))

      return best

  def __minimaxwithpruning(self, player, depth, alfa, beta, move):
    gameSize=self.size
    if move != None:
      points = self.countPoints(move)
      if player:
        return (-points, None)
      else:
        return (+points, None)
    elif depth == 0:
        if player:
            return (0, self.findEmpty())
        else:
            return (0, self.findEmpty())
    elif self.tied():
      return (0,None)
    elif player:        # kiedy ja
      best = (-math.inf, None)
      if (depth != 0):
          for x in range(gameSize):
              for y in range(gameSize):
                if self.fields[x][y]==self.empty:
                   value = self.move(x,y).__minimaxwithpruning(not player, depth - 1, alfa, beta, (x, y))[0]
                   if value>best[0]:
                     best = (value,(x,y))
                   if value > alfa:
                       alfa = value
                   if beta <= alfa:
                       break
      return best
    else:           # kiedy przeciwnik
      best = (+math.inf, None)
      if (depth != 0):
          for x in range(gameSize):
              for y in range(gameSize):
                if self.fields[x][y]==self.empty:
                  value = self.move(x,y).__minimaxwithpruning(not player, depth - 1, alfa, beta, (x, y))[0]
                  if value<best[0]:
                      best = (value,(x,y))
                  if value < beta:
                      beta = value
                  if beta <= alfa:
                      break

      return best

  def best(self, depth):
    return self.__minimax(True, depth)[1]

  def bestwithpruning(self, depth):
    return self.__minimaxwithpruning(True, depth, -math.inf, +math.inf, None)[1]

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

  def countPoints(self, move):
      (x, y) = move
      gameSize = self.size
      points = 0

      x1 = x
      y1 = y
      corners =  x1 == 0 and y1 == 0 or x1 == gameSize-1 and y1 == gameSize-1 or x1 == 0 and y1 == gameSize -1 or x1 == gameSize -1 and y1 == 0
      # print(self.fields)
      # print(move)
      points += (0 if gameSize-np.count_nonzero(self.fields[x][:]) != 0 else gameSize)
      points += (0 if gameSize-np.count_nonzero(self.fields[:, y]) != 0 else gameSize)
      # print(points)
      diagonalPoints = 0
      while x1 + 1 < gameSize and y1 + 1 < gameSize:
          if (self.fields[x1 + 1][y1 + 1] == 0):
              diagonalPoints = 0
              break
          else:
              diagonalPoints += 1
              x1 += 1
              y1 += 1

      # print('++', diagonalPoints)
      if(diagonalPoints != 0 or x == gameSize-1 or y == gameSize -1):
          x1 = x
          y1 = y
          while x1 - 1 >= 0 and y1 - 1 >= 0:
              if (self.fields[x1 - 1][y1 - 1] == 0):
                  diagonalPoints = 0
                  break
              else:
                  diagonalPoints += 1
                  x1 -= 1
                  y1 -= 1

      # print('--', diagonalPoints)
      points += diagonalPoints + 1 if diagonalPoints != 0 else 0
      # print(points)

      x1 = x
      y1 = y
      diagonalPoints = 0
      while x1 + 1 < gameSize and y1 - 1 >= 0:
          if (self.fields[x1 + 1][y1 - 1] == 0):
              diagonalPoints = 0
              break
          else:
              diagonalPoints += 1
              x1 += 1
              y1 -= 1
      # print('+-', diagonalPoints)
      if (diagonalPoints != 0 or y == 0 or x == gameSize -1):
          x1 = x
          y1 = y
          while x1 - 1 >= 0 and y1 + 1 < gameSize:
              if (self.fields[x1 - 1][y1 + 1] == 0):
                  diagonalPoints = 0
                  break
              else:
                  diagonalPoints += 1
                  x1 -= 1
                  y1 += 1

      # print('-+', diagonalPoints)
      points += diagonalPoints + 1 if diagonalPoints != 0 else 0
      # print(points)
      return points

if __name__ == '__main__':
  GUI().mainloop()