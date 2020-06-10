# Reinforcement Learning

## Introduction

There are a few critical elements to reinforcement learning. They are:

1. The **agent**, exposed to an **environment**. This environment are the programs that the algorithms operate in. This can be a game, a control method in a factory, or something else altogether.
2. The **state**, which is the overall situation encountered. In a game of chess, this would be the current arrangement of pieces on the board. Obviously, there are lots of possible states.
3. An **action**, which the agent uses to transition from one state to another (this can be no-action, if that action is allowed)
4. A **reward** or **penalty**, as a result of taking the aforementioned action.
5. The **policy**, or strategy, of choosing an action with a given state, expecting a better overall reward or outcome.

Reinforcement Learning lies somewhere between Supervised and Unsupervised Training. While the exact output isn't always known, there is a goal to achieve - The maximum "reward." There are a few important things to note:

1. Being *greedy* doesn't always work - sometimes the agents must accept a little delayed gratification in order to get the maximum possible reward.
2. *Sequence* matters. Unlike standard Supervised/Unsupervised Models, RL is time-dependent, and looks at the past history of states, and could even consider the future states.

![Animation of Reinforcement Learning](Images/RL_Animated.gif?raw=true)

Image from: [LearnDataScience](https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/)

RL helps to make optimal decisions using past experiences. It involves some really simple steps:

1. **Observation** of the **environment**.
2. **Deciding** on how to act, using some **policy**, and then **acting** accordingly.
3. Receiving an appropriate **penalty** or **reward**.
4. **Learning** from experience, and refining the policy.
5. **Iterate** until an **optimal strategy** can be found.

## The Reward Table

For every possible *state*, there has to be a number of possible rewards and actions. It is essentially has the number of states as rows, and number of actions per state as columns (i.e. a matrix of dimensions state x actions)

This reward table will tell the agent what rewards can be gotten in the short term for each action, and should also indicate which state will be entered into for each action taken. This does not, however, show *future* rewards or penalties, but will enable the agent to learn from present experience to inform future decisions.

## Q-Learning

Q-Learning allows an agent to use rewards to learn (over time), the best action to take, given a particular state. For any given reward table, the agent can learn from it by looking to receive a reward for taking an action in the current state, then updating a Q-value to remember that the particular action was beneficial. 

The values stored in the Q-table are called Q-values, and are mapped to a (state, action) combination.

The Q-value for any particular state-action combination represents the "quality" of an action taken from that particular state. A higher Q-value implies a better chance of getting a greater reward.

Q-values are initially arbitrary, and as the agent exposes itself to the environment, it receives differnet rewards by executing different action and then updating the Q-values using:

`Q(s, a) ← (1-α)Q(s, a) + α(reward + γ max(a)Q(next s, all a))`

- Where:
	- `*s*` and `*a*` are the *state* and *action*, respectively
	- `α` is the learning rate (`0 < α ≤ 1`). As in supervised learning with gradients being stepped over, α determines how quickly the Q-values are updated.
	- `γ` is the discount factor (`0 ≤ γ ≤ 1`). This determines how important *future* rewards are compared to immediate rewards (i.e. a higher discount factor makes it *less greedy*)


This assigns, or updates, the Q-value of the agent's current state and action by first taking a weight (`1 - α`) of the old Q-value, then adding the newly-learned value. This value is a combination of the reward for taking the current action in the current state, and hte discounted maximum reward from the next state that will be entered into.

In other words, the agent is learning the proper action to take in the current state by looking at the reward for the current state/action combination, and the maximum rewards for the next state. This eventually causes the agent to take the best course of action with the highest rewards strung together. 

The Q-value of any state-action pair is the sum of the instant reward and the discounted future reward of the resulting state. This way, Q-values can be stored for each state and action by means of a Q-table.

## Q-Table

The Q-table is a matrix where we have a row for every state (500) and a column for every action (6). It's first initialized to 0, and then values are updated after training. Note that the Q-table has the same dimensions as the reward table, but it has a completely different purpose.

First, the Q-Table initialised to 0:

| |Action 1|Action 2|Action 3|Action 4|
|---|---|---|---|---|
|State 0| | | | |
|State 1|0|0|0|0|
|...| | | | |
|State n| | | | |

After training the agent, the new Q-Table will look more like:

| |Action 1|Action 2|Action 3|Action 4|
|---|---|---|---|---|
|State 0|2.443|1.243|2.341|1.221|
|State 1|0.443|3.444|1.223|2.334|
|...| | | | |
|State n|1.233|2.652|2.822|3.214|

A Q-table has the same dimensions as a reward table, but serves a very different purpose.

## Q-Learning (A Summary)

The steps involved in Q-Learning are:

1. Initialize the Q-table to all zeros.
2. Begin exploratory actions: For every state, select any one amongst all possible actions for the current state (S).
3. Move to next state (S') as a result of that action (a).
4. For all possible actions from the state (S') select the one with the highest Q-value.
5. Update Q-table values using the equation.
6. Set the next state as the current state.
7. If goal state is reached, then end and repeat the process.


## Using Learned Values

After sufficient iterations, the Q-values will tend to converge, giving the agent an action-value function that can be used to choose the best move given the current state.

There is a trade-off between exploration (choosing a random action) and exploitation (choosing actions based on already learned Q-Values). The agent needs to be prevented from constantly choosing the same route and overfitting, so a new parameter, `ϵ`, is used during training.

Instead of selecting the best learned Q-Value action, the agent will sometimes choose a random value instead. A lower value of ϵ will allow more training epochs to occur with higher penalties (because it is exploring and making random decisions).

## Q-Learning vs Reinforcement Learning

A Q-Learning agent commits a lot more errors during its initial exploration, but once it has explored most of the states, it can act much more quickly to maximise rewards. As can be seen, the training initially starts with lots of epochs, and drops over time so that the goal can be achieved much more quickly (i.e. it stops being just random movements).

![](Images/Q_training.png?raw=true)

Agents are evaluated according to the following metrics:

- Average penalties per episode. The lower the penalties the better.
- Average number of timesteps. Fewer steps per training episode are desirable (i.e. the shortest path to the goal).
- Average rewards per move. A larger the reward indicates that the agent is taking the right actions, so deciding reward factors are crucial to RL.

## Hyperparameter Optimizations

Values of `α`, `γ`, and `ϵ` are typically based on intuition and some "trial and error" in most cases, but there are optimal ways to set them. Ideally, all three values should decrease over time as the agent learns, but actually builds up some relilience over time:

- `α` should decrease as the knowledge base increases over time
- `γ` should decrease as the agent gets closer to the deadline - meaning that the preference for a short-term reward will increase.
- `ϵ` should *increase*, since a more developed policy means that there is less exploration needed, and more exploitation of the policy can be used.

The simplest way (programmatically) to optimised the hyperparameters is to create a comprehensive search function (like a grid search) that selects the parameters that will results in the best reward-to-time-step ratio. This will aid in selecting parameters that can get the maximum reward in as short a time as possible.

The number of penalties corresponding to the hyperparameters value combination can also be tracked as well, since this can be a deciding factor. Genetic algorithms can be also used to optimise the hyperparameter values - But that may beyond the scope of this short write-up.