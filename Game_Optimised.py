#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 10:19:47 2020

@author: Jonathan

New experiment to minimise the arithmetic operations - can help to optimise 
iteration speed, and clean up some class functions.
"""
import numpy as np
from random import randint

class Game():
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.Board = np.zeros([4,4], dtype = int)
        self.FillBoard()
        self.Playing = True
        
    def FillBoard(self, Board = False):
        Board = self.Board if (type(Board) == bool) else Board
        ''' Getting empty spaces by finding all nonzeros and taking all cells 
        that are NOT not zeros. '''
        x, y = (Board == 0).nonzero()
        ''' Only fills one cell at a time. Previous experiments show that the 
        state space for more than one new cell at a time makes it a lot harder 
        to achieve 2048, even for a human agent. '''
        if len(np.unique(Board)) == (len(Board) ** 2):
            Board[x[0]][y[0]] = np.unique(Board)[1]
        else:
            rnd = randint(0,len(x)-1)
            Board[x[rnd]][y[rnd]] = randint(1,2)
        ''' If a board was input, this will return the newly shifted board, but
        otherwise the self.Board assignments should just work. '''
        if type(Board) == bool:
            return Board
    
    ''' This function moves the board from right to left. This is used for all
    versions of movement, and np.rot90 is used to rotate the board for different
    directional movements. '''
    def MoveBoard(self, Board = False):
        ''' The score for each move is the total new tiles created from that 
        move (not the random tiles created). '''
        score = 0
        Board = self.Board if (type(Board) == bool) else Board
        ''' Iterating through each row one at a time with the new zeros array
        that is essentially the output board. '''
        NewBoard = np.zeros([len(Board), len(Board)], dtype=int)
        for row, col in enumerate(Board):
            newRow = np.zeros(len(col), dtype = col.type)
            j = 0
            ''' "previous" stores the last-seen value, and checks if the new
            cell that's being looked at should be either the sum of two values
            or just a new value moved over. '''
            previous = None
            for i in range(col.size):
                ''' If it is not the cell's value is 0, skips the cell. '''
                if col[i] != 0:
                    if previous == None:
                        previous = col[i]
                        ''' If the previous value seen is the same at the new 
                        one, it will merge the cells! '''
                    elif previous == col[i]:
                        newRow[j] = 2 * col[i]
                        score += newRow[j]
                        j += 1
                        previous = None
                        ''' If the new value is different to the old value, then
                        just slides the value over.'''
                    else:
                        newRow[j] = previous
                        j += 1
                        previous = col[i]
            ''' If there is still a value stored when the iterations are over
            for a given row, pushes that value to the last known cell. '''
            if previous != None:
                newRow[j] = previous
            NewBoard[row] = newRow
        return NewBoard, score
    
    def fill(self, Board = False):
        Board = self.Board if (type(Board) == bool) else Board
        x,y = (self.Board == 0).nonzero()
        uniques = np.unique(self.Board)
        if len(uniques) == 16:
            Board[x[0]][y[0]] = uniques[1]
        else:
            rnd = randint(0,len(x)-1)
            Board[x[rnd]][y[rnd]] = 2 ** randint(1,2)
        self.CheckGameEnd()
        return Board
    
    def getAdj(self, x, y):
        # Excludes all -ve values or values that exceed the maximum.
        if x == 0:
            xRange = (0,1)
        elif x == self.Board.shape[0] - 1:
            xRange = (-1, 0)
        else:
            xRange = (-1, 0, 1)
        if y == 0:
            yRange = (0,1)
        elif y == self.Board.shape[0] - 1:
            yRange = (-1, 0)
        else:
            yRange = (-1, 0, 1)
        # This just excludes all the centre values so it will check AROUND the 
        # main cell only, and only adjacent cells (L=1 and not L=2 manhattan
        # distance).
        adjacency = [(i,j) for i in xRange for j in yRange if not ((i == j) | (i == -1) & (j == 1)) | ((i == 1) & (j == -1))]
        return adjacency
    
    def CheckGameEnd(self, Board = False):
        Board = self.Board if (type(Board)==bool) else Board
        if (Board != 0).all():
            for x in range(Board.shape[0]):
                for y in range(self.Board.shape[1]):
                    adj = self.getAdj(x,y)
                    for i,j in adj:
                        if Board[x][y] == self.board[x+i][y+j]:
                            return False
        return True
    
    def step(self, action):
        OldBoard = np.rot90(self.Board, action)
        NewBoard, score = self.MoveBoard(OldBoard)
        if (NewBoard == OldBoard).all():
            pass
        else:
            self.Score += score
            self.Board = NewBoard
            self.fill()
            self.turns += 1
            done = self.CheckGameEnd()
        return NewBoard, done
    
    def DrawBoard(self, print_now = True, Board = False):
        Board = self.Board if (type(Board) == bool) else Board
        length = len(str(2 ** Board.max())) if len(str(2 ** Board.max())) > 2 else 2
        ''' This divider can be reused multiple times, makes things a bit easier
        when building the entire printed board.'''
        Divider = ""
        for _ in range(len(Board)):
            Divider += "+"
            for _ in range(length):
                Divider += "-"
        Divider += "+\n"
        DrawnBoard = ""
        for row in self.Board:
            DrawnBoard += Divider
            for cell in row:
                DrawnBoard += "|"
                ''' Converts the integer 1234 into 2,4,8,16, making sure to 
                consider the 0-case.'''
                cellVal = 2 ** cell if cell > 0 else 0
                for _ in range(length - len(str(cellVal))):
                    DrawnBoard += " "
                DrawnBoard += str(cellVal)
            DrawnBoard += "|\n"
        DrawnBoard += Divider
        if print_now:
            print(DrawnBoard)
        else:
            return DrawnBoard
        
if __name__ == '__main__':
    Game = Game(4)
    Game.DrawBoard()
    
    print(Game.Board)