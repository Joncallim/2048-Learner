#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 16:50:46 2020

@author: Jonathan
"""

import curses
from curses import wrapper
from Game_2048 import Game_2048


def Draw_Rows(Row):
    StringRow = []
    for value in Row:
        cell = ''
        value = str(value)
        if len(value) < 4:
            for _ in range(4-len(value)):
                cell += " "
            cell += value
        StringRow.append(cell)
    Output = "\u2551".join(StringRow)
    return "{}{}{}".format("\u2551", Output, "\u2551")

def Draw_Game(stdscr):
    Game = Game_2048(4)
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
            subtitle = "Use the Arrow Keys or WASD to move"[:width-1]
        else:
            subtitle = "Game Over! Score: {}, Moves: {}".format(Game.Board.max(), Game.Turns)[:width-1]
        TopBound = "\u2554\u2550\u2550\u2550\u2550\u2566\u2550\u2550\u2550\u2550\u2566\u2550\u2550\u2550\u2550\u2566\u2550\u2550\u2550\u2550\u2557"[:width-1]
        Divider = "\u2560\u2550\u2550\u2550\u2550\u256C\u2550\u2550\u2550\u2550\u256C\u2550\u2550\u2550\u2550\u256C\u2550\u2550\u2550\u2550\u2563"[:width-1]
        BottomBound = "\u255A\u2550\u2550\u2550\u2550\u2569\u2550\u2550\u2550\u2550\u2569\u2550\u2550\u2550\u2550\u2569\u2550\u2550\u2550\u2550\u255C"[:width-1]
        Row1 = Draw_Rows(Game.Board[0])[:width-1]
        Row2 = Draw_Rows(Game.Board[1])[:width-1]
        Row3 = Draw_Rows(Game.Board[2])[:width-1]
        Row4 = Draw_Rows(Game.Board[3])[:width-1]
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
        stdscr.addstr(start_y +  5, start_x_GameBoard, TopBound)
        stdscr.addstr(start_y +  6, start_x_GameBoard, Row1)
        stdscr.addstr(start_y +  7, start_x_GameBoard, Divider)
        stdscr.addstr(start_y +  8, start_x_GameBoard, Row2)
        stdscr.addstr(start_y +  9, start_x_GameBoard, Divider)
        stdscr.addstr(start_y + 10, start_x_GameBoard, Row3)
        stdscr.addstr(start_y + 11, start_x_GameBoard, Divider)
        stdscr.addstr(start_y + 12, start_x_GameBoard, Row4)
        stdscr.addstr(start_y + 13, start_x_GameBoard, BottomBound)
        stdscr.move(height-1, width-1)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        Key = stdscr.getch()
        
def main():
    wrapper(Draw_Game)
    
if __name__ == "__main__":
    main()