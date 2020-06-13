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
    
    def __init__(self, Size):
        self.Size = Size
        self.reset()
    
    def reset(self):
        self.Board = np.zeros([self.Size,self.Size], dtype = int)
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