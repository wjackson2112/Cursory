#!/usr/bin/env python3

from CLexer import CLexer
import ply

class Token:
    def __init__(self, color, text, lineno, linepos):
        self.color = color
        self.text = str(text)
        self.lineno = lineno
        self.linepos = linepos

    def __str__(self):
    	return "Token({},{},{},{})".format(self.color, self.text, self.lineno, self.linepos)

class Palette:
    def __init__(self, normal, keyword, constant, operator, assignment):
        self.normal = normal
        self.keyword = keyword
        self.constant = constant
        self.operator = operator
       	self.assignment = assignment

class Colorizer:
	def __init__(self, palette=None, file=None):
		self.lexer = CLexer()
		if file:
			self.load(file)
		if not palette:
			self.palette = Palette(0, 2, 3, 4, 4)
		else:
			self.palette = palette
		self.prevLine = 1
		self.offset = 0

	def load(self, file):
		self.lexer.load(file)

	def token(self):
		lexTok = self.lexer.token()
		if lexTok:
			if lexTok.lineno != self.prevLine:
				self.prevLine = lexTok.lineno
				self.offset = lexTok.lexpos
			if lexTok.type == 'TAB':
				# TODO: Tab Width
				self.offset -= 3
			tok = Token(self.palette.normal, str(lexTok.value), lexTok.lineno, lexTok.lexpos - self.offset)
			if lexTok.type == 'KEYWORD':
				tok.color = self.palette.keyword
			if lexTok.type == 'CONSTANT':
				tok.color = self.palette.constant
			if lexTok.type == 'OPERATOR':
				tok.color = self.palette.operator
			if lexTok.type == 'ASSIGNMENT':
				tok.color = self.palette.assignment
			return tok
		else:
			None


	def reset(self):
		self.prevLine = 1
		self.offset = 0
		self.lexer.reset()