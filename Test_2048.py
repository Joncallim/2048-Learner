#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:48:09 2020

@author: Jonathan
"""

import numpy as np
from Game_2048 import Game_2048

# This function checks the the adjacency check is working properly. Returns 
# True if it is working correctly, and False if not.
def test_adjacency(Game):
    Pass = True
    # This board should return True, since all the tiles are non-identical
    GameOverBoard = np.array([[1,2,3,4],[4,3,2,1],[1,2,3,4],[4,3,2,1]])
    # This board will return False, since all are identical.
    GameOKBoard = np.array([[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2]])
    # Assign the original board to the Game's Board.
    Game.Board = GameOverBoard
    if Game.CheckAdjacent() != True:
        print("Error with Game Over state")
        Pass = False
    Game.Board = GameOKBoard
    if Game.CheckAdjacent() != False:
        print("Error with Game Continue state")
        Pass = False
    return Pass
    
def test_adjacency_getter(Game):
    Pass = True
    if Game.GetAdjacency(0,0) != [(0,1), (1,0)]:
        print("Error with Coordinates 0,0")
        Pass = False
    if Game.GetAdjacency(0,1) != [(0, -1), (0, 1), (1, 0)]:
        print("Error with Coordinates 0,1")
        Pass = False
    if Game.GetAdjacency(1,0) != [(-1, 0), (0, 1), (1, 0)]:
        print("Error with Coordinates 0,1")
        Pass = False
    if Game.GetAdjacency(0,Game.Board.shape[0] - 1) != [(0, -1), (1, 0)]:
        print("Error with Coordinates 0,max")
        Pass = False
    if Game.GetAdjacency(0,Game.Board.shape[0] - 1) != [(0, -1), (1, 0)]:
        print("Error with Coordinates max,0")
        Pass = False
    if Game.GetAdjacency(1,1) != [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        print("Error with Coordinates max,0")
        Pass = False
    else:
        return Pass
    
if __name__ == "__main__":
    Game = Game_2048(4)
    print("CheckAdjacent Test OK: ", test_adjacency(Game))
    print("GetAdjacency Test OK: ", test_adjacency_getter(Game))