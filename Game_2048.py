#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 17:51:00 2020

@author: Jonathan
"""


import numpy as np
from random import randint

class Game_2048():
    def __init__(self, Size):
        self.Size = Size
        # Uses the reset function to create all the necessary bitsw
        self.reset()
        
    def reset(self):
        # Creates an empty board the size that has been specified.
        self.Board = np.zeros([self.Size,self.Size], dtype=int)
        # Randomly fills up the board now, setting self.Board to a nicely-filled
        # array.
        self.FillBoard()
        self.Playing = True
        self.Turns = 0
    
    def MoveBoard(self, OldBoard):
        NewBoard = np.zeros([len(OldBoard),len(OldBoard)], dtype=int)
        # Iterates through each row one at a time. For every row, will iterate
        # through each column.
        for Row,Col in enumerate(OldBoard):
            # First creates a new row of empty 0s the length of the original row
            NewRow = np.zeros(len(Col), dtype=Col.dtype)
            # 'j' is an iterator that will count from the left-most cell and move
            # along as it fills up.
            j = 0
            # Using 'Prev', the last-seen value can be used to check if the next
            # 'New' cell should be the sum of 2 values, or just the last value 
            # slid over from the right, or other direction.
            Prev = None
            for i in range(Col.size):
                # If the column is a zero, then the cell will be skipped over, 
                # since all zeros are basically ignored...
                if Col[i] != 0:
                    # If there is no previous value stored, this will pull the
                    # next seen value and store it.
                    if (Prev == None):
                        Prev = Col[i]
                    # Now, if the next cell matches the Previously-seen value,
                    # The two values will be added and the value saved to the 
                    # next "New" value seen.
                    elif Prev == Col[i]:
                        NewRow[j] = 2 * Col[i]
                        j += 1
                        Prev = None
                    # Finally, if the previous value looks wildly different, it
                    # will just push the previous value into the new row's cell.
                    else:
                        NewRow[j] = Prev
                        j += 1
                        Prev = Col[i]
            # If there is still a value stored as "Previous" in the original set,
            # it will push that last stored value into the new row's cell.
            if Prev != None:
                NewRow[j] = Prev
            # Finally, pushes the new Row into the new board array.
            NewBoard[Row] = NewRow
        return NewBoard
    
    # 0: Left, 1: Up, 2: Right, 3: Down
    def Move(self, Direction):
        # Uses the dict of directions to specify a direction to rotate the old
        # board in before the operation continues.
        OldBoard = np.rot90(self.Board, Direction)
        NewBoard = self.MoveBoard(OldBoard)
        # If there is no change in the board, then it is an invalid move, and
        # the board does not change. Otherwise, adds a new cell.
        if (NewBoard == OldBoard).all():
            pass
        else:
            # Assigns the New Board to the stored Board, overwriting the older 
            # array. Uses the opposite rotation so that values will not be 
            # overwritten.
            self.Board = np.rot90(NewBoard, -Direction)
            self.FillBoard()
            self.Turns += 1

    def CountSpaces(self):
        # Counts the number of elements in the entire array - this is generalised
        # so that the function will work for any size of matrix, including a 3D
        # array.
        Size = 1
        for Dimension in np.shape(self.Board): Size *= Dimension
        # Counting the empty spaces (Zero-spaces) by counting any non-zeros and 
        # subtracting from the total size of the array.
        EmptySpaces = Size - np.count_nonzero(self.Board)
        return EmptySpaces
    
    def FillBoard(self):
        # Gets all empty cells (cells that = 0) in the array. Essentially finds
        # any cell that is 0, which makes it 1, and all non-zero cells will be 
        # 0. nonzero() then takes only the cells that are NOT zero... So 0s.
        x, y = (self.Board == 0).nonzero()
        # Since a check for all non-zeros has already been conducted, this just
        # makes sure that there are enough empty cells to fill up, otherwise
        # doesn't.
        # NewValues = randint(1, (2 if (len(x) > 1) else 1))
        NewValues = 1
        for _ in range(NewValues):
            # Picks a random index from the possible indices in the cell's x and
            # y indices.
            Rnd = randint(0, len(x) - 1)
            self.Board[x[Rnd]][y[Rnd]] = 2 #** randint(1,2)
        if self.EndGame() == True:
            self.Playing = False

    def GetAdjacency(self, x, y):
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

    def CheckAdjacent(self):
        # First obtaining the x and y dimensions and using them to iterated over
        # the entire board.
        for x in range(self.Board.shape[0]):
            for y in range(self.Board.shape[1]):
                # Gets the adjacency arrays (essentially cleaning up the code
                # nicely) so that only valid cells will be searched. You don't
                # want to overflow into -ve values, so these prevent that from
                # happening.
                Adjacency = self.GetAdjacency(x,y)
                for i,j in Adjacency:
                    if self.Board[x][y] == self.Board[x+i][y+j]:
                        return False
        return True
    
    # This function starts the end-of-game checks. In order to make sure that
    # the search isn't performed every single time (because that would take a 
    # pretty long time), this only happens when there are no empty spaces left.
    def EndGame(self):
        if self.CountSpaces() == 0:
            if self.CheckAdjacent() == True:
                return True
        else:
            return False

Rotation = {"a": 0, "w": 1, "d": 2, "s": 3}
# Test code for running the 2048 code as a standalone
if __name__ == "__main__":
    Game = Game_2048(4)
    print("Original Board:\n", Game.Board)
    while Game.Playing:
        # Direction = Rotation[input()]
        Direction = randint(0,3)
        Game.Move(Direction)
        print(Game.Board)
    print("Game Over. Score: {}. Turns: {}".format(Game.Board.max(), Game.Turns))
