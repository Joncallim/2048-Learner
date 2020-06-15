# Getting The Game's State

## Hexadecimal and Integer Representation

Searching through the state space is incredibly time-consuming. So, I've decided to use a 16-letter Hexadecimal representation for the state space representation.

- This is fairly simple, with each cell represented by a single digit in the Hexadecimal number. This will scale up easily for any size of board, and helps with search speed immensely since the keys are being searched (which are hashed) instead of the values.
- This means that the search is O(1), and board can be converted to Hexadecimal and vice versa fairly quickly.

It's still faster to iterate through the board in order to determine reward rather than perform a search for the entire state table, especially as the table gets bigger and bigger. So to bring the size down to O(1) again, I've gone that way. Searching for the Q_Values, however, will have to continue until I implement DQN.

