# Optimizers
## Used for Stochastic Gradient Descent (SGD) in Neural Networks


### Momentum
- Momentum helps SGD to navigate along relevant directions and softens oscillations in irrelevant directions. Simply adds a fraction of the direction of the previous step to a current step, which amplifies speed in the correct direction and reduces oscillation in any wrong direction. This fraction is usually in the (0, 1) range. 
- Also uses adaptive momentum, starting with small movement and slowly getting faster. However, this can cause oscillations near the end-goal since the steps taken there will be much larger.

### Nesterov Accelerated Gradient
- NAG overcomes this problem slightly by slowing down early. Instead of computing gradient then taking a step (amplified by any previous momentum), NAG takes a step first, then calculates the gradient and makes a small correction. In practice, this greatly improves performance.


### AdaGrad (Adaptive Gradient)
- AdaGrad allows learning rates to adapt based on various parameters. For very infrequency parameters, learning rates are changed by a larger amount, and similarly for frequent parameters - a smaller amount. This makes it particularly well suited for NLP or Image Recognition tasks (which are sparse-data tasks by nature).
- A further advantage of AdaGrad is that it eliminates the need to tune the learning rate, since each parameter has its own learning rate, which is monotonically decreasing. However, this decrease causes the system to eventually stop learning after a certain amount of time.
- The learning rate is approximately `1/sum(sqrts)`. At each stage, another `sqrt` is added to the sum, decreasing the overall learning rate.

### AdaDelta
- AdaDelta overcomes the limitations of Adagrad by calculating the learning rate using a sliding window, which prevents the sum from decreasing too much.

### RMS Prop
- RMS Prop is very similar to AdaDelta. It is still quite popular with Reinforcement Learning tasks, and there are some arguments that it can be better suited for non-stationary learning problems that crop up in RL tasks due to an Agent adapting behaviour over time.

### ADAM (ADAptive Momentum)
- An algorithm similar to AdaDelta, but additionally stores momentum changes seperately to learning rates for each parameter. This is the most commonly-used optimizer in RL research. This is relatively newer, (and isn't included in the nice visualisation linked here), but is very popular.

These are all more sophisticated than a simple gradient descent, and can be much more useful for optimisation in loss search spaces that are not smooth. This helps to overcome small imperfections in a gradient slope, since the momentum term "remembers" that the overall direction should go in a certain direction.

Visualisations: Taken from [Ruder.io](https://ruder.io/optimizing-gradient-descent/index.html#visualizationofalgorithms)

![SGD Optimization on Loss Surface Contours](Images/qAx2i.gif?raw=true)

Above, it is obvious that even though SGD takes a shorter path, it is much, much slower than the momentum-based options. Below, it cannot even resolve the additional downward slope (since it has already found the minima relative to its original direction of travel).

![SGD Optimization on Saddle Point](Images/1obtV.gif?raw=true)

Further Reading: 
[Sebastian Ruder: An overview of gradient descent optimization algorithms](https://ruder.io/optimizing-gradient-descent/index.html#visualizationofalgorithms)
