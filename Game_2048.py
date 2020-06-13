#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 17:51:00 2020

@author: Jonathan


This is the code to run the actual Game 2048. Used in conjunction with all the 
other algorithmic and RL functions, and to display some pretty code that can be
used for Curses or as a standalone display with this function. Use inputs() to
get the directions...
"""


import numpy as np
from random import randint
from IPython.display import clear_output
from time import sleep
from math import log
from copy import deepcopy

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
        self.Score = 0
    
    def MoveBoard(self, OldBoard):
        ScoreToAdd = 0
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
                        # Adds the score for every tile combined - note that the
                        # game does not score new tiles just just.. appear - it
                        # gives you a higher score every time you merge tiles.
                        # so rewards go up exponentially over time.
                        ScoreToAdd += NewRow[j]
                        j += 1
                        Prev = None
                        # Adding the score to the total score.
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
        return NewBoard, ScoreToAdd
    
    # This counts the number of appropriately-ordered numbers in descending 
    # sequence there are.
    def GetSequence(self, TestBoard):
        Board = deepcopy(TestBoard)
        MaxInCorner = False
        # Rotating the board until the max tile is in corner. This will run 
        # indefinitely if the function calling it is not careful.
        while not MaxInCorner:
            Board = np.rot90(Board)
            x,y = np.where(Board == Board.max())
            if (x[0] == 0) & (y[0] == 0):
                MaxInCorner = True
        # First iteration using the horizontal counts.
        Count = [0, 0]
        for i in range(2):
            Count[i] = 0
            PreviousCell = Board.max()
            Column = 0
            OddRow = False
            StopCounting = False
            for row in Board:
                for _ in range(len(Board)):
                    cell = row[Column]
                    if (cell <= PreviousCell) & (cell > 0):
                        if not StopCounting:
                            PreviousCell = cell
                            Count[i] += 1
                    else:
                        StopCounting = True
                        break
                    # On even-numbered rows, (i.e. row 0,2, will count down,
                    # otherwise counts up.)
                    Column = Column + 1 if not OddRow else Column - 1
                # resets the counts at the end of each row, then flips the toggle
                # for OddRow.
                Column = len(row) - 1 if not OddRow else 0
                OddRow = not OddRow
                if StopCounting:
                    break
            # Second iteration, making the second copy and using it.
            Board = np.transpose(Board)
        return max(Count)
    
    def ValidMoves(self, Board):
        # Returns all possible moves, and the rewards associated with that move.
        Moves = []
        OldMax = Board.max()
        for Direction in range(4):
            OldBoard = np.rot90(Board, Direction)
            NewBoard, NewScore = self.MoveBoard(OldBoard)
            # If the move is to make a no-change move, the algorithm REALLY doesn't
            # want this to happen, so very heavily weights a penalty.
            if (NewBoard == OldBoard).all():
                Moves.append(-NewBoard.max())
            else:
                # First if the move keeps the max-value tile in a corner, gives
                # it a much higher weighting.
                x, y = np.where(Board == Board.max())
                if (x[0] == 0 | x[0] == len(Board)) & (y[0] == 0 | y[0] == len(Board)):
                    # The game always prefers getting a higher score overall, so
                    # an immediate action that will increase the maximum possible
                    # score, while keeping the max tile in the corner, is the 
                    # most prefered move.
                    if NewBoard.max() > OldMax:
                        Moves.append(NewScore + log(NewBoard.max(), 2) + self.GetSequence(NewBoard))
                    # Still, if it's a good move, it's a good move.. Awards points
                    # for keeping tiles in the corner, as usual.
                    else:
                        Moves.append(NewScore + self.GetSequence(NewBoard))
                # Finally, if the max-value tile moves out of the corner, the
                # algorithm loses a FEW points.
                else:
                    if NewScore == 0:
                        Moves.append(2)
                    else:    
                        Moves.append(0.5 * NewScore)
        return Moves
    
    # 0: Left, 1: Up, 2: Right, 3: Down
    def Move(self, Direction):
        # Uses the dict of directions to specify a direction to rotate the old
        # board in before the operation continues.
        OldBoard = np.rot90(self.Board, Direction)
        NewBoard, ScoreToAdd = self.MoveBoard(OldBoard)
        # If there is no change in the board, then it is an invalid move, and
        # the board does not change. Otherwise, adds a new cell.
        if (NewBoard == OldBoard).all():
            pass
        else:
            # Assigns the New Board to the stored Board, overwriting the older 
            # array. Uses the opposite rotation so that values will not be 
            # overwritten.
            self.Score += ScoreToAdd
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
        '''
        # Since a check for all non-zeros has already been conducted, this just
        # makes sure that there are enough empty cells to fill up. If there are
        # only 2 cell to fill, it will not do this action, and instead fill only
        # 1 cell so a player has a chance to win.
        if len(x) > 2:
        # Picking a random value from the list so that there can be either 1 or
        # 2 new numbers added to the board.
            for _ in range(randint(1,2)):
                # Picks a random index from the possible indices in the cell's x and
                # y indices.
                Rnd = randint(0, len(x) - 1)
                self.Board[x[Rnd]][y[Rnd]] = 2 ** randint(1,2)
        # This condition triggers whenever there is only 1 space left on the board.
        else:
        '''
        # If there are n-1 unique values on the board and there is 1 empty
        # space, it could be very well that a player has done really well and
        # arrange all the tiles so that there are just exactly enough spaces
        # to keep winning, so the program will reward him/her. 
        Uniques = np.unique(self.Board)
        if len(Uniques) == (self.Size * self.Size):
            self.Board[x[0]][y[0]] = Uniques[1]
        else:
            Rnd = randint(0,len(x)-1)
            self.Board[x[Rnd]][y[Rnd]] = 2 ** randint(1,2)
        # Checking if the game should end - if the newly added tiles have killed
        # the game...
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
    
    def DrawBoard(self, Board = None):
        Board = self.Board if Board == None else Board
        # This sets all tiles to be at least 2-std-width, just looks a little 
        # prettier than a single-width tile.
        TileLength = len(str(self.Board.max())) if len(str(self.Board.max())) > 2 else 2
        # Creates the diver that is used repeatedly for each row.
        Divider = ""
        for _ in range(self.Size):
            Divider += "+"
            for _ in range(TileLength):
                Divider += "-"
        Divider += "+\n"
        # Drwaing the actual board.
        DrawnBoard = ""
        for row in self.Board:
            DrawnBoard += Divider
            for cell in row:
                DrawnBoard += "|"
                # Adding some spaces in front of every number so that it's nice
                # and padded.
                for _ in range(TileLength - len(str(cell))):
                    DrawnBoard += " "
                DrawnBoard += str(cell)
            DrawnBoard += "|\n"
        DrawnBoard += Divider
        print(DrawnBoard)
        print("Total Score: ", self.Score)
        print("Maximum Tile: ", self.Board.max())
        print("Total Moves: ", self.Turns)
    
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
    while Game.Playing:
        clear_output(wait = True)
        Direction = randint(0,3)
        Game.Move(Direction)
        Game.DrawBoard()
        sleep(0.1)
    print("Game Over. Score: {}. Turns: {}".format(Game.Board.max(), Game.Turns))
