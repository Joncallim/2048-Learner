#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:35:25 2020

@author: Jonathan
"""

import gc
import numpy as np
from Game_2048 import Game_2048
from copy import deepcopy



class Search_2048():
    def __init__(self, Board):
        try:
            self.Board = Board
        except:
            type(Board) != np.ndarray
        self.Nodes = {}
        self.GameClass = Game_2048(len(Board))
        pass
    
    # Move function, almost identical to the one within the game, but optimised
    # for use in this function as called for AgentMove
    def AgentMove(self, Direction, Board):
        # Uses the dict of directions to specify a direction to rotate the old
        # board in before the operation continues.
        OldBoard = np.rot90(Board, Direction)
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
        # If there is no change in the board, then it is an invalid move, and
        # the board does not change. Otherwise, adds a new cell.
        if (NewBoard == OldBoard).all():
            return None
        else:
            # Returns the new, shifted Board.
            return np.rot90(NewBoard, -Direction)
        
    def GetAgentMove(self, Board, Layer):
        MaxReward = None
        OptimalMove = None
        for Direction in range(4):
            NewBoard = self.AgentMove(Direction, Board)
            try:
                if NewBoard.any() != False:
                    reward = NewBoard.max()
                    if reward > MaxReward:
                        MaxReward = reward
                        OptimalMove = Direction
                # self.Node[Layer]["board"] = NewBoard
            except:
                type(NewBoard) == bool
        return MaxReward, OptimalMove
    
    # Returns the number of empty spaces. This algorithm currently wants to have
    # fewest empty spaces on the board.
    def EmptySpaces(self, Board):
        EmptySpaces = (2*len(Board)) - np.count_nonzero(Board)
        return EmptySpaces
    
    def BFS(self, Board):
        OptimalMove = 0
        MaxReward = 0
        Move_1 = None
        Reward_1 = 0
        Move_2 = None
        Reward_2 = 0
        Move_3 = None
        Reward_3 = 0
        OrigSpace = self.EmptySpaces(Board)
        # Iterating through each direction possible.
        for Direction in range(4):
            # Gets a new board based on the predicted movement at each stage.
            NewBoard = self.AgentMove(Direction, Board)
            # The Try-Catch statements prevent the "None" returns from being
            # processed. This speeds up later searches when the move is invalid.
            try:
                if NewBoard.all() != None:
                    # If there is no move stored currently, saves the current
                    # move as valid, otherwise does nothing.
                    Move_1 = Direction if (Move_1 is None) else Move_1
                    # If the reward at this state is higher than before (i.e.
                    # if moving in a particular direction gets you a higher 
                    # score, saves that move.)
                    if Reward_1 < NewBoard.max():
                        Reward_1 = NewBoard.max()
                        Move_1 = Direction
                    # If the saved reward is the same in each direction, now
                    # prefers to take a step that will reduce the number of 
                    # empty spaces on the board. (Only checks for the first
                    # move, since next-generation moves are fairly stochastic
                    # by nature)
                    elif Reward_1 == NewBoard.max():
                        if self.EmptySpaces(NewBoard) < OrigSpace:
                            Reward_1 = NewBoard.max()
                            Move_1 = Direction
                    # This is an array of possible random permutations given the
                    # number of possible spaces on the board. The algorithm wants
                    # to maximise the possible score, so a 3-level search is 
                    # performed.
                    PossibleBoards = self.GetChanceBoard(NewBoard)
                    for L2_Board in PossibleBoards:
                        for L2_Direction in range(4):
                            L2_NewBoard = self.AgentMove(L2_Direction, L2_Board)
                            try:
                                if L2_NewBoard.all() != None:
                                    # L2 and L3 are only concerned with the maximum
                                    # possible score. For an even deeper search,
                                    # this stochastic search could possibly
                                    # find the true maximum, but to save on 
                                    # computational power, and since this is just
                                    # a proof-of-concept, I'm stopping at 3 layers.
                                    Move_2 = Direction if (Move_2 is None) else Move_2
                                    if L2_NewBoard.max() > Reward_1:
                                        Reward_2 = L2_NewBoard.max()
                                        Move_2 = Direction
                                    L2_PossibleBoards = self.GetChanceBoard(L2_NewBoard)
                                    for L3_Board in L2_PossibleBoards:
                                        for L3_Direction in range(4):
                                            L3_NewBoard = self.AgentMove(L3_Direction, L3_Board)
                                            try:
                                                if L3_NewBoard.all() != None:
                                                    Move_3 = Direction if (Move_3 is None) else Move_3
                                                    if L3_NewBoard.max() > Reward_2:
                                                        Reward_3 = L2_NewBoard.max()
                                                        Move_3 = Direction
                                            except:
                                                L3_NewBoard == None
                            except:
                                L2_NewBoard == None
            except:
                NewBoard == None
        OptimalMove = Move_1 if Reward_1 < Reward_2 else Move_2
        OptimalMove = OptimalMove if (Reward_1 ** 2) <= Reward_3 else Move_1
        return OptimalMove, MaxReward
    
    def FillBoard_1(self, x, y, Board):
        Output = []
        # For each possible value in the cell, puts and output board in the array
        # of possible board permutations.
        for rnd in range(1,3):
            NewBoard = deepcopy(Board)
            NewBoard[x][y] = 2 ** rnd
            Output.append(NewBoard)
        return Output
    
    # Currently not used.
    def FillBoard_2(self, x, y, i, j, Board):
        Output = []
        for rnd_1 in range(1,3):
            for rnd_2 in range(1,3):
                NewBoard = deepcopy(Board)
                NewBoard[x][y] = 2 ** rnd_1
                NewBoard[i][j] = 2 ** rnd_2
                Output.append(NewBoard)
        return Output
    
    def GetChanceBoard(self, Board):
        PossibleBoards = []
        x,y = (Board == 0).nonzero()
        for n in range(len(x)):
            # if len(x) == 1:
            ''' Temporarily removed the 2nd random cell, so only ever one cell
            is filled per move. Makes it a bit easier to start off with - the 
            number of possibilities otherwise are quite endless. '''
            PossibleBoards.extend(self.FillBoard_1(x[n],y[n],Board))
            # for q in range(len(x)):
            #     if q != n:
            #         PossibleBoards.extend(self.FillBoard_2( x[n],y[n], x[q],y[q], Board ))
        return PossibleBoards
        
    
# Actual Function:
if __name__ == "__main__":
    Game = Game_2048(4)
    Search = Search_2048(Game.Board)
    print("Original:")
    print(Game.Board)
    PreviousTurn = 0
    while Game.Playing:
        Move,_ = Search.BFS(Game.Board)
        Game.Move(Move)
        print(Game.Board, 'Move: ', Move, 'Turn: ', Game.Turns, "Score: ", Game.Board.max())
        # Error check - there was a bug earlier where the algorithm was tryying to 
        # make the same move repeatedly. 
        if PreviousTurn == Game.Turns:
            print("error")
            break
        else:
            PreviousTurn = Game.Turns
            
    print("Score: {}, Turns: {}".format(Game.Board.max(), Game.Turns))