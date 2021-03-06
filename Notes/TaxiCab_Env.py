#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 18:18:02 2020

@author: Jonathan

# ============================== INTRODUCTION =============================== #
Some really useful env .methods:

env.reset: Resets the environment and returns a random initial state.
env.step(action): Step the environment by one timestep. Returns:
    - observation: Observations of the environment.
    - reward: If your action was beneficial or not.
    - done: Indicates if we have successfully picked up and dropped off a 
    passenger, also called an episode.
info: Additional info such as performance and latency for debugging purposes.
env.render: Renders one frame of the environment (for visualization)

For the Taxi environment being used here: The problem statment as laid out by
the Gym docs is: "There are 4 locations (labeled by different letters), and our 
job is to pick up the passenger at one location and drop him off at another. We 
receive +20 points for a successful drop-off and lose 1 point for every time-
step it takes. There is also a 10 point penalty for illegal pick-up and drop-
off actions."

# ================================ RENDERING ================================ #
When env.render() is called:
    - The filled square represents the taxi, which is yellow without a passenger 
    and green with a passenger.
    - The pipe ("|") represents a wall which the taxi cannot cross.
    - R, G, Y, B are the possible pickup and destination locations. The blue 
    letter represents the current passenger pick-up location, and the purple 
    letter is the current destination.
These change every time env.reset is called.

# =============================== STATE SPACE =============================== #
- By calling env.action_space, it can be found that there is an action space of 
6. The possible actions are:
    0 = south
    1 = north
    2 = east
    3 = west
    4 = pickup
    5 = dropoff
- the env.action_space.sample() command can be also used to select a random 
action from the set of all possible actions.

- Calling env.observation_space shows that there are 500 possible states. This
corresponds to an encoding of the taxi's location, the passenger's location, 
and the destination location.

- States can be encoded using env.encode([taxi row], [taxi column], [passenger 
index],[destination index])

RL should then find the optimum path to take in order to maximise the long-term
rewards, by considering the environment.

# ================================= REWARDS ================================= #
A Reward Table can be called using env.P[state]. When the game is first started
an arbitrary reward table is created, with the number of states (s) as rows, and
the number of actions (a) as columns (i.e. an s x a matrix)

The reward table (P) is a dictionary with the following format:
    { action: [(probability, nextstate, reward, done)] }
    
    - The 0-5 corresponds to the actions (south, north, east, west, pickup, 
    dropoff) the taxi can perform at our current state in the illustration.
    - In this env, probability is always 1.0.
    - The "nextstate" is the state we would be in if we take the action at this 
    index of the dict.
    - All the movement actions have a -1 reward and the pickup/dropoff actions 
    have -10 reward in this particular state. If we are in a state where the 
    taxi has a passenger and is on top of the right destination, we would see 
    a reward of 20 at the dropoff action (5)
    - "done" is used to tell us when we have successfully dropped off a 
    passenger in the right location. Each successfull dropoff is the end of an 
    episode.

"""

from pprint import pprint # Makes nice dict outputs
import gym
import random
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
from time import sleep

def print_frames(frames):
    for i, frame in enumerate(frames):
        clear_output(wait=True)
        print(frame['frame'])
        print(f"Timestep: {i + 1}")
        print(f"State: {frame['state']}")
        print(f"Action: {frame['action']}")
        print(f"Reward: {frame['reward']}")
        sleep(.1)
        
''' This section performs completely random actions at each state, and performs
incredibly poorly because the "agent" is just moving around aimlessly and also
incurring massive penalties. '''
def RandomMovement():
    ''' The core gym interface is env, which is the unified environment interface. 
    The .env on the end of .make avoid training stopping at 200 iterations, which 
    is default for the new version of Gym.
    (https://stackoverflow.com/questions/42787924/why-is-episode-done-after-200-time-steps-gym-environment-mountaincar/42802225#42802225). '''
    env = gym.make("Taxi-v3").env
    ''' This just makes the starting state the exact same state for every single
    iteration. env.envode is in the format: taxi row, taxi column, passenger
    index, dest. index.'''
    state = env.encode(3, 1, 0, 2)
    print("State:", state)
    ''' Pushing the generated state to the environment '''
    env.s = state
    ''' Rendering the current environment '''
    env.render()
    epochs = 0
    penalties, reward = 0, 0
    ''' Nice little Tuple for animation. '''
    frames = []
    done = False
    while not done:
        ''' Picking a random action from the list, and executing that action.'''
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        ''' This just counts the penalties (i.e. the number of bad pickups and
        drop-offs that occurred. '''
        if reward == -10:
            penalties += 1
        ''' This is storing all the rendered states into a nice little dict for
        animation. The scene is rendered repeatedly for every state that the 
        (completely random) agent enters into. '''
        frames.append({
            'frame': env.render(mode='ansi'),
            'state': state,
            'action': action,
            'reward': reward
            }
        )
        # Counts up for every epoch
        epochs += 1
    print_frames(frames)
    ''' Finally, displays the number of steps taken and how many bad moves were
    incurred by the (admittedly random) agent. '''
    print("Timesteps taken: {}".format(epochs))
    print("Penalties incurred: {}".format(penalties))

def QLearning():
    env = gym.make("Taxi-v3").env
    q_table = np.zeros([env.observation_space.n, env.action_space.n])
    ''' Hyperparameters. Remember that alpha and gamma are used in the Q-learning
    equation, and epsilon is the delay, essentially. '''
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1
    ''' Easy way to plot metrics later on. '''
    all_epochs = []
    all_penalties = []
    ''' This is just training the model 100,000 times. '''
    for i in range(1, 100001):
        ''' Resetting all variables. '''
        state = env.reset()
        epochs, penalties, reward, = 0, 0, 0
        done = False
        while not done:
            ''' First, decide whether to pick a random action or to use already
            computed Q-values. Smply uses the epsilon value and compares it to 
            the random.uniform(0, 1) function, which returns an arbitrary number 
            between 0 and 1. '''
            if random.uniform(0, 1) < epsilon:
                action = env.action_space.sample() # Explore action space
            else:
                action = np.argmax(q_table[state]) # Exploit learned values
            ''' The particular chosen action is taken to get the next_state and
            the reward table for that state. Then, the maximum Q-Value for the
            action corresponding to S' is calculated, and the Q-Value can easily
            be updated to new_q_value'''
            next_state, reward, done, info = env.step(action) 
            ''' First gets the old Q-Value from the Q-Table, then using the next
            state's highest reward (from the Q-Table), obtains the '''
            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])
            ''' Q-learning equation, works quite nicely to teach the agent. Then
            updates the q_table with the new Q-value. '''
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state, action] = new_value
            if reward == -10:
                penalties += 1
            state = next_state
            epochs += 1
        all_epochs.append(epochs)
        all_penalties.append(penalties)
        if i % 1000 == 0:
            clear_output(wait=True)
            print(f"Episode: {i}")
    print("Training finished.\n")
    plt.subplot(2,1,1)
    plt.plot(all_epochs)
    plt.ylabel('Number of Epochs')
    plt.subplot(2,1,2)
    plt.plot(all_penalties)
    plt.ylabel('Number of Penalties')
    plt.xlabel('Training Episode')
    plt.show()
    return env, q_table
    
def Eval(env, q_table):
    ''' Evaluate agent's performance after Q-learning. Does this 100 times so 
    that the average can be taken. '''
    total_epochs, total_penalties = 0, 0
    episodes = 100
    for _ in range(episodes):
        ''' Resets the state to a random variable. '''
        state = env.reset()
        epochs, penalties, reward = 0, 0, 0
        done = False
        ''' Uses the Q-Table values (and the Q-Table values alone) to evaluate
        the effectiveness of the model '''
        while not done:
            action = np.argmax(q_table[state])
            state, reward, done, info = env.step(action)
            if reward == -10:
                penalties += 1
            epochs += 1
        total_penalties += penalties
        total_epochs += epochs
    print(f"Results after {episodes} episodes:")
    print(f"Average timesteps per episode: {total_epochs / episodes}")
    print(f"Average penalties per episode: {total_penalties / episodes}")

def UseQTable(env, q_table):
    ''' Resets the state to a random variable. '''
    state = env.reset()
    epochs, penalties, reward = 0, 0, 0
    frames = []
    done = False
    ''' Uses the Q-Table values (and the Q-Table values alone) to evaluate
    the effectiveness of the model '''
    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, info = env.step(action)
        if reward == -10:
            penalties += 1
        frames.append({
            'frame': env.render(mode='ansi'),
            'state': state,
            'action': action,
            'reward': reward
            }
        )
        epochs += 1
    print_frames(frames)
    
def DeepQLearning():
    env = gym.make("Taxi-v3").env
    agent = DeepLearning()
    ''' Easy way to plot metrics later on. '''
    all_epochs = []
    all_penalties = []
    ''' This is just training the model 100,000 times. '''
    for eps in range(1, 100001):
        ''' Resetting all variables. '''
        state = env.reset()
        epochs, penalties, reward, = 0, 0, 0
        done = False
        while not done:
            ''' First, gets the next agent according to the deep learning agent.
            This can either be a random action or one that exploits the Q-values.'''
            action = agent.GetNextAction(state)
            ''' The particular chosen action is taken to get the next_state and
            the reward table for that state '''
            next_state, reward, done, info = env.step(action)
            ''' The agent then evaluates if the step taken was a good step, and
            updates its weights to reflect that. Training happens inside this
            function, effectively. '''
            agent.Update(state, next_state, action, reward)
            if reward == -10:
                penalties += 1
            state = next_state
            epochs += 1
            if done:
                print(done)
        all_epochs.append(epochs)
        all_penalties.append(penalties)
        if eps % 10 == 0:
            clear_output(wait=True)
            print(f"Episode: {eps}")
    print("Training finished.\n")
    plt.subplot(2,1,1)
    plt.plot(all_epochs)
    plt.ylabel('Number of Epochs')
    plt.subplot(2,1,2)
    plt.plot(all_penalties)
    plt.ylabel('Number of Penalties')
    plt.xlabel('Training Episode')
    plt.show()
    return env

from keras.models import Sequential
from keras.layers import Dense, InputLayer


class DeepLearning:
    def __init__(self, learning_rate=0.5, discount=0.95, exploration_rate=1.0, iterations=1000):
        self.learning_rate = learning_rate
        self.discount=discount
        self.exploration_rate = exploration_rate
        '''This represents the shift from exploration to exploitation'''
        self.exploration_delta = 1.0 / iterations
        self.DataSize = 501
        self.DefineModel()
        
    def DefineModel(self):
        self.model = Sequential()
        ''' The input is an array of a single item - the state. The input is two
        dimensional due to the posibility of batched training, but that is not
        used in this particular example. '''
        self.model.add(InputLayer(batch_input_shape=(1, self.DataSize)))
        ''' This creates the actual neural network: two layers with 32 hidden 
        nodes each, with the sigmoud activation intialised to 0 (which keeps it
        stable). '''
        self.model.add(Dense(1024, activation='sigmoid'))
        self.model.add(Dense(512, activation='sigmoid'))
        self.model.add(Dense(256, activation='sigmoid'))
        self.model.add(Dense(128, activation='sigmoid'))
        self.model.add(Dense(64, activation='sigmoid'))
        self.model.add(Dense(32, activation='sigmoid'))
        self.model.add(Dense(16, activation='sigmoid'))
        ''' The output is defined for all possible actions - Q for possible
        actions. This can also work with batched training, but this current
        model assumes no batching. '''
        self.model.add(Dense(6, activation='linear'))
        self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    
    ''' Given a particular state, this uses the model to estimate the Q value
    by inference. '''
    def GetQ(self, state):
        ''' Here, the model's input is an array of a single item - the state.
        The output is an Array of Q values for that state, for each possible
        action that can be taken. the identity matrix is used to one-hot encode
        the 500-length identity matrix, and the state:state+1 term is used to 
        make it an array. '''
        return self.model.predict(np.identity(self.DataSize)[state:state+1])
    
    def GetNextAction(self, state):
        if random.random() > self.exploration_rate:
            return self.Exploit(state)
        else:
            return self.Explore()
    
    ''' Exploitation uses the highest Q value as estimated by the model. Argmax
    returns the index of the highest Q, corresponding to the appropriate action
    that the model should take. '''
    def Exploit(self, state):
        return np.argmax(self.GetQ(state))
    
    def Explore(self):
        return random.randint(0,5)
    
    def Train(self, state, action, reward, new_state):
        ''' First, getting the Q values for the current state by inference, then
        does the same thing for the next state. '''
        state_Q_values = self.GetQ(state)[0]
        new_state_Q_values = self.GetQ(new_state)[0]
        ''' Now gets the real Q values for the action just taken, which is the
        Q values that should be trained towards. '''
        state_Q_values[action] = reward + self.discount * np.amax(new_state_Q_values)
        ''' Setting up various training data bits, then training the model.'''
        training_input = np.identity(self.DataSize)[state:state+1]
        ''' Reshapes the array for input into the neural net. '''
        target_output = state_Q_values.reshape(-1,6)
        self.model.fit(training_input, target_output, epochs=1, verbose=0)
    
    def Update(self, state, new_state, action, reward):
        ''' First, training the model with the newly-obtained data. '''
        self.Train(state, action, reward, new_state)
        ''' Shift exploration rate (epsilon) downwards, so more exploitation
        will progressively happen. '''
        if self.exploration_rate > 0:
            self.exploration_rate *= 0.999999999

if __name__ == "__main__":
    # env, q_table = QLearning()
    # Eval(env, q_table)
    DeepQLearning()