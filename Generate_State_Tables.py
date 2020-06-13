#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:55:23 2020

@author: Jonathan

This function does a little bit of a simple search for the Q-Tables in the game
2048. While unable to actually return any useful values since the state space is
impossibly huge, it demonstrates the principles of searching for the state space
via random iteration.

This code is actually really weak - with a 3x3 grid it learns to get a score of
32 in a vaugely long amount of time, and with a 2x2 grid it basically can't 
exceed 16, except to occasionally get to 32. The stochastic nature of the states
jumping around seems to mess with this a little, and the values of the states 
and rewards don't bode well for it.
"""
from Game_2048 import Game_2048
from random import randint, uniform
import matplotlib.pyplot as plt
import numpy as np
import json
from math import log

''' The Tables class initialises the State Table and Q-Table for use with the
game. It does not generate a list of all possible values since that would be an
array that is over 10 petabytes large. I'm sure it is possible to come up with
some algorithm that works out how the numbers are shifted around, but that's 
not overwhelmingly a priority at the moment - it would be very bespoke code for
a very generalised problem. '''
class Tables():
    def __init__(self, Size):
        ''' Starts the game with a size of 4. Uses the utility functions in the
        Game_2048 class in order to search through the entire state space.'''
        self.Game = Game_2048(Size)
        self.Size = Size
        with open('Files/Q_Table.json', 'r') as file:
            self.Q_Table = json.load(file)
    
    ''' Utility function to reset the Q-Table - goes through each value in the
    Q-Table and resets it to 0 reward for all actions. '''
    def ResetQTable(self):
        for key in self.Q_Table.keys():
            self.Q_Table.update({key: [0,0,0,0]})
        
    
    ''' Given a particular board configuration, gets the key (state) index that
    references the particular board. This could be optimised for speed and memory
    by using 1,2,3,4,5 instead of 2,4,8,16,32 - but it's just a proof of concept
    and I didn't want to think too hard about doing that. '''
    def GetState(self, InputBoard):
        State = ""
        for row in InputBoard:
            for cell in row:
                HexVal = log(cell,2) if cell > 0 else 0.0
                ''' lstrip removes the front-end, and rstrip removes the "L" that
                represents a long number. The if statements makes sure that '0'
                is always added on, so that the correct indices for each cell 
                will always be present.'''
                State += hex(int(HexVal)).lstrip("0x").rstrip("L") if HexVal != 0 else "0"
        if State not in self.Q_Table:
            self.Q_Table.update({State: [0, 0, 0, 0]})
        return State 
    
    def SaveTables(self):
        with open('Files/Q_Table.json', 'w') as f:
            f.write(json.dumps(self.Q_Table, sort_keys=True, indent=4))
    
    ''' Returns an appropriate board for any given input state. '''
    def GetBoard(self, State):
        Board = np.zeros([self.Size, self.Size], dtype = int)
        i = 0
        for x in range(self.Size):
            for y in range(self.Size):
                ''' Generates the int value using the letter value, then converts
                it to the appropriate int value. Since 2^0=1, this is pushed as
                0 if it's a 1. '''
                cell = 2 ** int(State[i], 16)
                Board[x][y] = cell if cell > 1 else 0
                i += 1
        return Board
    
class QLearning():
    def __init__(self, Size):
        ''' Calls the Game class to use some of the utility functions, and to
        actually step through the game. Creates the Tables class which can be
        used to get the State and Q-Tables. '''
        self.Game = Game_2048(Size)
        self.Tables = Tables(Size)
        
    ''' This was a fun little experiment to see how many new states could be 
    discovered with a pure random exploratory protocol - the algorithm just 
    picks a random direction, and if the state is unknown, saves that state to 
    memory. After about 10000 iterations, the "algorithm" is still discovering
    about 500 new states per 10 iterations, despite never exceeding a score of
    128 or 256 in some rare cases.'''
    def FindInitialState(self, iterations = 1000):
        alpha = 0.1
        gamma = 0.8
        print("Searching for random states...")
        ''' This random iteration just happens for as long as you tell it to. '''
        for it in range(iterations):
            self.Game.reset()
            ''' Plays the game to completion each time. '''
            while self.Game.Playing:
                action = randint(0,3)
                state = self.Tables.GetState(self.Game.Board)
                ''' The reward comes from the State Table (obtained from the 
                ValidMoves function in the Game class. '''
                reward = self.Game.ValidMoves(self.Game.Board)[action]
                Old_Val = self.Tables.Q_Table[state][action]
                ''' Whether a random or chosen action was taken, the game moves
                the tiles in that direction. '''
                self.Game.Move(action)
                next_state = self.Tables.GetState(self.Game.Board)
                next_max = np.max(self.Tables.Q_Table[next_state])
                ''' This is the Q-Learning algorithm in all its glory. The 
                calculated value is then saved to the Q-Table. '''
                new_value = (1-alpha) * Old_Val + alpha * (reward + gamma * next_max)
                self.Tables.Q_Table[state][action] = new_value
                ''' Updating the current state and epoch. '''
                state = next_state
            if it % 100 == 0:
                print("{} of {} iterations complete".format(it, iterations))
                print("{} States found.".format(len(self.Tables.Q_Table)))
    
    ''' Search performs the actual Q-Learning. It can be used without knowing
    ANY of the states, since it can create states on the fly and fill them in
    as it goes along. However, this is obviously not ideal, as a search will 
    still take a very long time. '''
    def Search(self, iterations = 100, print_graphs = False):
        print("Training Starting...")
        ''' Hyperparameters - see notes for more info '''
        alpha = 0.1
        gamma = 0.7
        epsilon = 0.1
        decay = 0.9999999
        HighScore, MaxScore, MaxReward = 0,0,0
        all_epochs, all_scores, all_rewards, all_max_tile = [], [], [], []
        for it in range(iterations):
            epsilon *= 1.0000001
            alpha *= decay
            gamma *= decay
            ''' Resetting values every time the game ends. '''
            self.Game.reset()
            state = self.Tables.GetState(self.Game.Board)
            epochs, reward = 0, 0
            while self.Game.Playing:
                ''' If the random generated number is less than epsilon, it will
                take a random step (exploration) '''
                if uniform(0,1) < epsilon:
                    action = randint(0,3)
                    ''' Otherwise, uses the best-known step from the Q-Table, 
                    as it already knows (exploitation). '''
                else:
                    action = np.argmax(self.Tables.Q_Table[state])
                ''' The reward comes from the State Table (obtained from the 
                ValidMoves function in the Game class. '''
                reward = self.Game.ValidMoves(self.Game.Board)[action]
                Old_Val = self.Tables.Q_Table[state][action]
                ''' Whether a random or chosen action was taken, the game moves
                the tiles in that direction. '''
                self.Game.Move(action)
                next_state = self.Tables.GetState(self.Game.Board)
                next_max = np.max(self.Tables.Q_Table[next_state])
                ''' This is the Q-Learning algorithm in all its glory. The 
                calculated value is then saved to the Q-Table. '''
                new_value = (1-alpha) * Old_Val + alpha * (reward + gamma * next_max)
                self.Tables.Q_Table[state][action] = new_value
                ''' Updating the current state and epoch. '''
                state = next_state
                epochs += 1
                MaxReward = reward if reward > MaxReward else MaxReward
            HighScore = self.Game.Score if self.Game.Score > HighScore else HighScore
            MaxScore = self.Game.Board.max() if self.Game.Board.max() > MaxScore else MaxScore
            all_epochs.append(epochs)
            all_scores.append(self.Game.Score)
            all_rewards.append(reward)
            all_max_tile.append(self.Game.Board.max())
            if it % 100 == 0:
                print("{} of {} iterations complete. {} States found.".format(it, iterations, len(self.Tables.Q_Table)))
                print('High Score: {}; Max Tile: {}; Max Reward: {}\n'.format(HighScore, MaxScore, MaxReward))
                HighScore, MaxScore, MaxReward = 0,0,0
        if print_graphs:
            plt.title("Epochs")
            plt.plot(all_epochs)
            plt.show()
            plt.title("Scores")
            plt.plot(all_scores)
            plt.show()
            plt.title("Rewards")
            plt.plot(all_rewards)
            plt.show()
            plt.title("Maximum Tile")
            plt.plot(all_max_tile)
            plt.show()
        
    def Q_Move(self, iterations = 100):
        state = self.Tables.GetState(self.Game.Board)
        all_scores, max_tile = 0, 0
        for i in range(iterations):
            self.Game.reset()
            while self.Game.Playing:
                action = np.argmax(self.Tables.Q_Table[state]) if np.max(self.Tables.Q_Table[state]) != 0 else np.argmax(self.Game.ValidMoves(self.Game.Board))
                self.Game.Move(action)
                state = self.Tables.GetState(self.Game.Board)
            all_scores += self.Game.Score
            max_tile = self.Game.Board.max() if self.Game.Board.max() > max_tile else max_tile
        print("Tested over {} Iterations: Average Score: {}; Maximum Tile: {}".format(iterations, int(all_scores/iterations), max_tile))
        pass

if __name__ == '__main__':
    ''' Can try out different board sizes and training configurations - a list
    of 3 and upwards will essentially never find optimum since it's basically 
    impossible to find the entire search space in a relatively short amount of
    time and with limited memory. '''
    QLearning = QLearning(4)
    QLearning.FindInitialState(100)
    QLearning.Search(iterations=100,
                      print_graphs = False)
    QLearning.Tables.SaveTables()
    QLearning.Q_Move()