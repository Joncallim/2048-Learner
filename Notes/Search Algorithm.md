# Search Algorithms
## Reinforcement Learning for 1-Player Game


### Minimax (Also MinMax Search)

For any game with multiple paths, there is a game tree that shows the maximum and minimum algorithm. This usually applies to a 2-player game, where the *min* agent is playing logically, and trying to maximise its own score as well.

There are three primary components to this:

1. The Value, *V*
2. The Alpha value, *α*
3. The Beta value, *ß*

![Game Tree](Images/Game_Tree.png?raw=true "MinMax Search Algorithm")

The algorithm for this is mutually recursive (i.e. the *Max-Value* algorithm pulls the *Min-Value* algorithm, and vice-versa).

Alpha-Beta pruning can help to dramatically speed up the search. In the tree shown, there are a very limited number of nodes, but when there are 4 moves per possible node, then the number of nodes that need to be searched goes up very quickly, and this pruning is necessary.

#### Max-Value Algorithm (*state*, *α*, *ß*)
```
- if terminal(state), return U(state)
- V = -∞
- for c in next-state (s):
	- V' = Min-Value(C, α, ß)
	- if V' > V, V = V'
	- if V' ≥ ß, return V
	- if V' > α, α = V'
- return V

```



#### Min-Value Algorithm (*state*, *α*, *ß*)
```
- if terminal(state), return U(state)
- V = +∞
- for c in next-state (s):
	- V' = Max-Value(C, α, ß)
	- if V' < V, V = V'
	- if V' ≤ α, return V
	- if V' < ß, ß = V'
- return V
```


As the search is performed, the Value starts from the bottom and the tree is searched upwards. Without alpha-beta pruning, the search tree will look like this:

![Minimax without Alpha Beta Pruning](Images/Game_Tree_Searched.png?raw=true "MinMax Search without Alpha-Beta Pruning")

Using Alpha-Beta Pruning now, each branch has a value of alpha or beta included. Effectively, if pruning is performed, then the search at 12 does not need to be performed, since it already knows that, when 10 is encountered, the value at that max node will never be lower than the already-lower minimum value at the min node.

![Alpha Beta Pruning](Images/Pruned.png?raw=true "Alpha-Beta Pruning")

This will also continue to hold true on the other side of the search tree, where alpha pruning can be performed (as a maximum value instead of a minimum value). This is all very useful since it helps to vastly reduce the search space.

### Expectiminimax 

The expectiminimax algorithm is a variation of the minimax algorithm, typically used in AI systems that play 2-player zero-sum games, where the outcome depends on both the player's skill as well as some random elements. In addition to the minimum and maximum nodes, expectiminimax also considers the expected value of a random event. These "random" nodes take a weighted average of the max and min nodes, with the weight being the probability that the child is reached.

Interleaving depends on the game - each turn of the game is evaluated as a "max" node, and a "min" or "chance" node represents the (potentially-optimal) opponent's move, or random effect (particularly for the game 2048, where the "*opponent moves*" are essentially the randomly-added values to the search space.

While a game with 2 players and a die throw would ordinarily have a "*chance*", "*min*", and "*max*" node, the game 2048 would only have a "*max*" and "*chance*" nodes.


#### Expectiminimax Algorithm (*state*, *depth*, *α*)
```
- if terminal(state) or depth = 0, return U(state)
- if opponent move:
	- let α = +∞
	- for each child:
		- α = min(α, expectiminimax(child, depth-1)
- else if own move:
	- let α = -∞
	- for each child:
		- α = max(α, expectiminimax(child, depth-1)
- else if random event:
	- let α = 0
	- for each child:
		- α = α + (Probability(child) x expectiminimax(child, depth-1))
return α
```

For random nodes, there *must* be a known probability of reaching each child. (For most games, child nodes are equally weighted, meaning the return value can just be the average of all child values)