# 2048-Learner

Trying my hand out at Reinforcement Learning with the game 2048

---

The first component of this game, is of course - the actual implementation of the game 2048. I've written some code that will play the game, along with a few testbench functions, and a GUI-console-based implementation (because who doesn't like a cool game they can push buttons on)

If you want to give this all a go, you'll have to have Python 3, Numpy, and Curses installed. If you have pip installed, Curses is a simple

`pip3 install curses --upgrade` 

or

`pip install curses --upgrade`

`git clone` this library to your computer, and you can take a look at whatever has gone on in here.

Run the GUI with `python3 play_2048` once you have navigated to the directory.

![GUI Implementation](Images/GUI_Game_Over.png?raw=true "Game Over GUI Implementation")

You can also run it in a standard console (and print over everything) 

---

While the GUI implementation is not scalable (It'll go up to 4 digits then break), and you can't resize the board, the actual implementation of the game in `Game_2048` will work for any length of side of game board. This can be useful to expand the board for more RL searches in the future.

---
### Pseudocode
1. Initialise board with size *nxn*. Randomly seed this board so that it will place 1 or 2 random values of 2,4 or 8 on the board.
2. Move the board. The same "Move Left" iteration is reused for all directions, and the Numpy `rot90` function is called to change the direction for movements in different directions.
	- For each row, iterate through each column, store a "previous" value that starts as "None".
		- If a non-zero value is encountered, and "previous" is "None", replace the "previous" value with that value.
		- If a non-zero value is encountered that matches the previous value, sum them and save that value, and replace "previous" with "None".
		- If a non-zero value is encountered that matches the previous value, save the old previous value and replace it with the new value.
		- If a zero-value is encountered, skip that cell.
	- Save new values incrementally to a new list, starting from 0 and only incrementing when a new value is saved to it.
	- If the moved board matches the previous state, it is not a valid move, and nothing happens after this.
3. Fill any empty cells (zeros) with randomly-generated 2,4, or 8.
4. Check if game has ended:
	- Check if any empty cells left.
	- Check if any adjacent cells are identical. If no identical cells left, game is over.
5. Score = Maximum tile on boards.
6. Number of Turns = Number of valid moves made.

---
### NN Implementation:

Yet to do, will use a RL algorithm and mess around until I'm happy.