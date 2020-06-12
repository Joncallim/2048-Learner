# Getting The Game's State

## Hexadecimal and Integer Representation

Searching through the state space is incredibly time-consuming. So, I've decided to use a 16-letter Hexadecimal representation for the state space representation.

- This is fairly simple, with each cell represented by a single digit in the Hexadecimal number. This will scale up easily for any size of board, and helps with search speed immensely since the keys are being searched (which are hashed) instead of the values.
- This means that the search is O(1), and board can be converted to Hexadecimal and vice versa fairly quickly.