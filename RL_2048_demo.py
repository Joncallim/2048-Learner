#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 18:25:21 2020

@author: Jonathan
"""

import matplotlib.pyplot as plt
import numpy as np
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, InputLayer
from Game_2048 import Game_2048
import tensorflow as tf
from random import randint, random


episodes = 1000

class Model(tf.keras.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.Dense = [[],[],[],[],[]]
        self.Dense[0] = tf.keras.layers.Dense(64, activation = tf.nn.relu)
        self.Dense[1] = tf.keras.layers.Dense(32, activation = tf.nn.relu)
        self.Dense[2] = tf.keras.layers.Dense(16, activation = tf.nn.relu)
        self.Dense[3] = tf.keras.layers.Dense(8, activation = tf.nn.relu)
        self.Dense[4] = tf.keras.layers.Dense(4, activation = tf.nn.softmax)
        self.Dropout = tf.keras.layers.Dropout(0.5)

    def Call(self, inputs, training = False):
        x = self.Dense[0](inputs)
        for i in range(1,5):
            if training:
                x = self.Dropout(x, training = training)
            x = self.Dense[i](x)
        return x
    
model = Model()
model.compile(loss='categorical_crossentropy',
              optimizer='adam')


# now execute the q learning
Game = Game_2048(4)
y = 0.95
eps = 0.5
decay_factor = 0.999
r_avg_list = []
model.fit(Game.Board, 
          [0.25, 0.25, 0.25, 0.25], 
          epochs=1, 
          verbose=0)
for i in range(episodes):
    Game.reset()
    eps *= decay_factor
    if i % 100 == 0:
        print("Episode {} of {}".format(i + 1, episodes))
        print("Score: {}".format(Game.Board.max()))
    r_sum = 0
    while Game.Playing:
        if random() < eps:
            Direction = randint(0, 3)
        else:
            Pred = model.predict(Game.Board)
            Direction = np.argmax(model.predict(Game.Board))
            print(Pred)
        target_vec = model.predict(Game.Board)
        # Using the square root so the score doesn't go up too fast
        Game.Move(Direction)
        r = Game.Board.max()
        target = r + y * np.max(model.predict(Game.Board))
        target_vec[Direction] = target
        model.fit(Game.Board, target_vec, epochs=1, verbose=0)
        r_sum += r
    r_avg_list.append(r_sum / 1000)
    
plt.plot(r_avg_list)