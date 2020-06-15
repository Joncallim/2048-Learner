# Deep Q-Learning or Reinforcement Learning

### Introduction

When using a Q-Table, memory requirements are `states x actions`. While this is easy for a small state space, it is much harder to do for a very large board. In the game 2048, as mentioned several times in the other notes, this comes up to easily `10,000,000,000 x 4` (at least).

In order to scale the size of the Q-Table, some accuracy can be traded for compression. In media, storing a 1080p video at 60fps lossless uses approximates 1GB per second. A similar video can be stored with a bit of loss for 0.00001 of that storage. In Deep Learning, something similar is acceptable - "Good Enough" or "Better than Human" are all acceptable states.

![](Images/dqn-qn.png?raw=true)

Image from: [valohai.com](https://blog.valohai.com/reinforcement-learning-tutorial-basic-deep-q-learning?hsCtaTracking=8d695af6-7c26-45af-b4e0-3eea19acc471%7Cdefc83b7-2f34-4629-a3fb-512fad652bbd)

---

### The Deep Reinforcement Learning Equation

Instead of obtaining a perfect value from the Q-Table stored after lots and lots of iterations, a neural net is trained to estimate what the table output should be - adjusting the weights and biases appropriately. This is essentially using a Neural Network to perform compression on some data.

The equation used to perform training for a Neural Net is slightly different, and is given by:

	Q(s,a) <- r' + γ * argmax(Q(s',a))
		where: s is the state
		       a is the action taken
		       r is the reward
		       γ is the discount factor
		       
This is considerably simpler than the Q-Learning algorithm. The learning rate, `α`, is no longer needed, since a backpropagation optimizing algorithm would automatically take care of that. Once `α` is removed, two of the `Q(s,a)` terms can also be removed, since they cancel each other out if the learning rate is removed.

While Reinforcement Learning does not use any "training data" like in supervised learning, it does create "training data" while exploring the state space, and uses this quite similarly to optimise its weights and biases. As an agent explores the state space, it **records experiences**:

	Single Experience = (s, a, r, s')
	
Training a model using a single experience:

1. Estimate Q-Values of current state, `s`.
2. Estimate Q-Values of the next state, `s'`.
3. Calculate the new target Q-Value for the action using a known reward.
4. Train the model with `input = s, output = target Q values`

The network doesn't receive the `s,a` combination that a Q-Learning function does - Only a Q-Table is replicated, not the entire Q-Learning paradigm. The input to a Neural Network is just the state, and the output are the Q-Values for all possible actions (0,1,2,3 for left, right, up, down or some other moves) for that state.

--- 

### Batch Learning

When a model or agent is retrained after each step of the simulation with one experience at a time, it is called **online training**.

A more popular approach to DRL training is to collect all or many of the experiences into a memory log. The model is then trained against multiple experiences taken randomly from this log as a batch. This is called **batch** or **mini-batch training**. It is not only more efficient, but often provides more stable training results overall to reinforcement learning. 