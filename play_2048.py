#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 16:50:46 2020

@author: Jonathan
"""

import curses
from curses import wrapper
from Game_2048 import Game_2048


def DrawDivider(Board):
    TileLength = len(str(Board.max())) if len(str(Board.max())) > 2 else 3
    Divider = "\u2560"
    for _ in range(len(Board)):
        for _ in range(TileLength):
            Divider += "\u2550"
        Divider += "\u256C"
    Divider = Divider[:len(Divider) - 1] 
    Divider += "\u2563"
    return Divider

def DrawTopRow(Board):
    TileLength = len(str(Board.max())) if len(str(Board.max())) > 2 else 3
    Pipes = "\u2554"
    for _ in range(len(Board)):
        for _ in range(TileLength):
            Pipes += "\u2550"
        Pipes += "\u2566"
    Pipes = Pipes[:len(Pipes) - 1] 
    Pipes += "\u2557"
    return Pipes

def DrawBottomRow(Board):
    TileLength = len(str(Board.max())) if len(str(Board.max())) > 2 else 3
    Pipes = "\u255A"
    for _ in range(len(Board)):
        for _ in range(TileLength):
            Pipes += "\u2550"
        Pipes += "\u2569"
    Pipes = Pipes[:len(Pipes) - 1] 
    Pipes += "\u255C"
    return Pipes

def DrawRows(Board):
    TileLength = len(str(Board.max())) if len(str(Board.max())) > 2 else 3
    Rows = []
    for _ in range(len(Board)):
        Rows.append([])
    for i,row in enumerate(Board):
        Rows[i] = "\u2551"
        for cell in row:
            for _ in range(TileLength - len(str(cell))):
                Rows[i] += " "
            Rows[i] += str(cell)
            Rows[i] += "\u2551"
    return Rows

def Draw_Game(stdscr):
    Game = Game_2048(5)
    Key = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (Key != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        if Game.Playing:
            if (Key == curses.KEY_DOWN) | (Key == ord('s')):
                Game.Move(3)
            elif (Key == curses.KEY_UP) | (Key == ord('w')):
                Game.Move(1)
            elif (Key == curses.KEY_RIGHT) | (Key == ord('d')):
                Game.Move(2)
            elif (Key == curses.KEY_LEFT) | (Key == ord('a')):
                Game.Move(0)

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)
        
        
        # Declaration of strings
        title = "2048 - GUI Implementation"[:width-1]
        if Game.Playing:
            subtitle = "Use the Arrow Keys or WASD to move. Score: {}".format(Game.Score)[:width-1]
        else:
            subtitle = "Game Over! Score: {}, Moves: {}".format(Game.Board.max(), Game.Turns)[:width-1]
        TopBound = DrawTopRow(Game.Board)[:width-1]
        Divider = DrawDivider(Game.Board)[:width-1]
        BottomBound = DrawBottomRow(Game.Board)[:width-1]
        Rows = DrawRows(Game.Board)
        statusbarstr = "Press 'q' to exit | Maximum Score: {} | Turns: {}".format(Game.Board.max(), Game.Turns)


        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_GameBoard = int((width // 2) - (len(TopBound) // 2) - len(TopBound) % 2)
        start_y = int((height // 3) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y +  1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y +  3, (width // 2) - 2, '-' * 4)
        yCount = 5
        stdscr.addstr(start_y +  yCount, start_x_GameBoard, TopBound)
        yCount += 1
        for i in range(len(Game.Board)):
            stdscr.addstr(start_y + yCount, start_x_GameBoard, Rows[i][:width-1])
            yCount += 1
            if i != len(Game.Board) - 1:
                stdscr.addstr(start_y + yCount, start_x_GameBoard, Divider)
                yCount += 1
        stdscr.addstr(start_y + yCount, start_x_GameBoard, BottomBound)
        stdscr.move(height-1, width-1)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        Key = stdscr.getch()
        
def main():
    wrapper(Draw_Game)
    
if __name__ == "__main__":
    main()