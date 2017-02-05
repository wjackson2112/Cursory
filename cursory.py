#!/usr/bin/env python3

import curses
import argparse

from Editor import Editor

def init_colors():
	curses.init_pair(1, curses.COLOR_BLACK,   curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLUE,    curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_CYAN,    curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_GREEN,   curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(6, curses.COLOR_RED,     curses.COLOR_BLACK)
	curses.init_pair(7, curses.COLOR_WHITE,   curses.COLOR_BLACK)
	curses.init_pair(8, curses.COLOR_YELLOW,  curses.COLOR_BLACK)

def main(stdscr, args):
	quit = False
	ch = -1

	init_colors()

	file = None
	if len(args.files) > 0:
		file = args.files[0]

	editor = Editor(file, curses.LINES, curses.COLS, 0, 0)

	while not editor.shouldClose():
		editor.refresh()
		editor.update(ch)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='A text editor for me')
	parser.add_argument('files', nargs='*')
	args = parser.parse_args()

	curses.initscr()
	# print("{}".format(curses.COLORS))
	curses.wrapper(main, args)

	# colorizer = Colorizer(file=args.files[0])
	# while True:
	# 	token = colorizer.token()
	# 	if token:
	# 		print(token)
	# 	else:
	# 		break