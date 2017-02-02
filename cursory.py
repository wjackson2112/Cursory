#!/usr/bin/python3

import curses
import argparse
import linecache
from time import sleep
from keys import Key

def init_colors():
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

class Editor():

	def __init__(self, file, height, width, originy, originx):
		self.closed = False

		self.file = file

		self.topLine = 1
		self.originx = originx
		self.originy = originy
		self.height = height
		self.width = width

		self.lineNumWidth = 6
		self.cursor = [1, 1]

		self.lineNumWin = curses.newwin(height, self.lineNumWidth, originy, originx)
		self.lineNumWin.clear()
		self.lineNumWin.keypad(1)

		self.editorWin = curses.newwin(height,width - self.lineNumWidth, originy, originx + self.lineNumWidth)
		self.editorWin.clear()
		self.editorWin.keypad(1)

		self.refresh()

	def cursorLeft(self):
		if self.cursor[0] > 1:
			self.cursor[0] -= 1

	def cursorRight(self):
		if self.cursor[0] < curses.COLS:
			self.cursor[0] += 1

	def cursorUp(self):
		if self.cursor[1] - 1 <= self.originy and self.topLine <= 1:
			return

		if self.cursor[1] - 1 <= self.originy:
			self.topLine -= 1
		else:
			self.cursor[1] -= 1

	def cursorDown(self):
		if self.cursor[1] + 1 > self.height + self.originy and self.topLine + self.height > file_len(self.file):
			return

		if self.cursor[1] + 1 > self.height + self.originy:
			self.topLine += 1
		else:
			self.cursor[1] += 1

	def placeCursor(self):
		self.editorWin.move(self.cursor[1] - 1, self.cursor[0] - 1)

	def parseInput(self, ch):
		#TODO: Bounds checking on these cursor moves
		if ch == Key.UP.value:
			self.cursorUp()

		if ch == Key.DOWN.value:
			self.cursorDown()

		if ch == Key.LEFT.value:
			self.cursorLeft()

		if ch == Key.RIGHT.value:
			self.cursorRight()

		if ch == Key.ESCAPE.value:
			self.closed = True

	def update(self, ch):
		ch = self.editorWin.getch()
		self.parseInput(ch)
		self.placeCursor()

	def refresh(self):
		self.editorWin.clear()
		self.lineNumWin.clear()

		for i in range(self.topLine, self.topLine + self.height):
			self.lineNumWin.addstr(i - self.topLine, self.lineNumWidth - 1 - len(str(i)), str(i), curses.color_pair(2))

		for i in range(self.topLine, self.topLine + self.height - 1):
			self.editorWin.addstr(i - self.topLine, 0, linecache.getline(self.file, i))

		self.editorWin.refresh()
		self.lineNumWin.refresh()

		self.placeCursor()

	def shouldClose(self):
		return self.closed

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

	# print(args)
	curses.wrapper(main, args)