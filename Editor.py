#!/usr/bin/env python3

import curses
import linecache
from Colorizer import Colorizer

from time import sleep
from keys import Key

class Editor():

	def __init__(self, file, height, width, originy, originx):
		self.closed = False

		self.file = file

		with open(self.file) as f:
			self.line_len = len(str(f.readline()))
			for i, l in enumerate(f):
				pass
		self.file_len = i + 1

		self.colorizer = Colorizer(file=self.file)

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
		if self.cursor[0] < self.line_len:
			self.cursor[0] += 1

	def cursorUp(self):
		if self.cursor[1] - 1 <= self.originy and self.topLine <= 1:
			return

		if self.cursor[1] - 1 <= self.originy:
			self.topLine -= 1
		else:
			self.cursor[1] -= 1

		try:
			line = linecache.getline(self.file, self.cursor[1])
		except:
			line = ""
		self.line_len = len(line)
		self.line_len += line.count('\t') * 3


	def cursorDown(self):
		if self.cursor[1] + 1 > self.height + self.originy and self.topLine >= self.file_len:
			return

		if self.cursor[1] + 1 > self.height + self.originy:
			self.topLine += 1
		else:
			self.cursor[1] += 1

		try:
			line = linecache.getline(self.file, self.cursor[1])
			self.line_len = len(line)
			self.line_len += line.count('\t') * 3
		except:
			self.line_len == 0


	def placeCursor(self):
		if self.line_len == 0:
			self.editorWin.move(self.cursor[1] - 1, 0)
		elif self.cursor[0] > self.line_len-1:
			self.editorWin.move(self.cursor[1] - 1, self.line_len-1)
		else:
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
		curses.curs_set(0)
		self.editorWin.erase()
		self.lineNumWin.erase()

		for i in range(self.topLine, self.topLine + self.height):
			self.lineNumWin.addstr(i - self.topLine, self.lineNumWidth - 1 - len(str(i)), str(i), curses.color_pair(8))

		self.colorizer.reset()
		prevLine = self.topLine
		offset = 0
		while True:
			token = self.colorizer.token()
			if token == None:
				break
			if token.lineno < self.topLine:
				continue
			elif token.lineno >= self.topLine + self.height:
				break
			else:
				self.editorWin.addstr(token.lineno - self.topLine, token.linepos - offset, str(token.text), curses.color_pair(token.color))


		self.editorWin.refresh()
		self.lineNumWin.refresh()
		self.placeCursor()

		curses.curs_set(1)

	def shouldClose(self):
		return self.closed