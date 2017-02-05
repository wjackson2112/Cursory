#!/usr/bin/env python3

# C Port of the ANSI C grammar
# www.lysator.liu.se/c/ANSI-C-grammar-l.html

import ply.lex as lex
from ply.lex import TOKEN


class CLexer:
    D  = r'[0-9]'
    L  = r'[a-zA-Z_]'
    H  = r'[a-fA-F0-9]'
    E  = r'[Ee][+-]?{D}+'
    FS = r'(f|F|l|L)'
    IS = r'(u|U|l|L)*'

    identifier = "{}({}|{})*".format(L, L, D)

    keywords = ('AUTO',
                'BREAK',
                'CASE',
                'CHAR',
                'CONST',
                'CONTINUE',
                'DEFAULT',
                'DO',
                'DOUBLE',
                'ELSE',
                'ENUM',
                'EXTERN',
                'FLOAT',
                'FOR',
                'GOTO',
                'IF',
                'INT',
                'LONG',
                'REGISTER',
                'RETURN',
                'SHORT',
                'SIGNED',
                'SIZEOF',
                'STATIC',
                'STRUCT',
                'SWITCH',
                'TYPEDEF',
                'UNION',
                'UNSIGNED',
                'VOID',
                'VOLATILE',
                'WHILE'
                )

    # Operators
    operators = (
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
        'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
        'LOR', 'LAND', 'LNOT',
        'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

        # Increment/decrement
        'PLUSPLUS', 'MINUSMINUS',

        # Structure dereference (->)
        'ARROW',

        # Conditional operator (?)
        'CONDOP',
        )

    # Assignments
    assignments = (
        # Assignment
        'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',
        'PLUSEQUAL', 'MINUSEQUAL',
        'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL',
        'OREQUAL',
        )

    keyword_map = {}
    for keyword in keywords:
      keyword_map[keyword.lower()] = keyword

    # List of token names.   This is always required
    tokens = keywords + operators + assignments + (
        # Identifiers
        'ID',

        # Type identifiers (identifiers previously defined as
        # types with typedef)
        'TYPEID',

        # constants
        # 'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX', 'INT_CONST_BIN',
        # 'FLOAT_CONST', 'HEX_FLOAT_CONST',
        # 'CHAR_CONST',
        # 'WCHAR_CONST',
        'CONSTANT',

        # String literals
        'STRING_LITERAL',
        'WSTRING_LITERAL',

        # Delimeters
        'LPAREN', 'RPAREN',         # ( )
        'LBRACKET', 'RBRACKET',     # [ ]
        'LBRACE', 'RBRACE',         # { }
        'COMMA', 'PERIOD',          # . ,
        'SEMI', 'COLON',            # ; :

        # Ellipsis (...)
        'ELLIPSIS',

        # pre-processor
        'PPHASH',       # '#'
        'PPPRAGMA',     # 'pragma'
        'PPPRAGMASTR',

        'TAB',
        'SPACE'
    )

    # Regular expression rules for simple tokens

    # Operators
    t_PLUS              = r'\+'
    t_MINUS             = r'-'
    t_TIMES             = r'\*'
    t_DIVIDE            = r'/'
    t_MOD               = r'%'
    t_OR                = r'\|'
    t_AND               = r'&'
    t_NOT               = r'~'
    t_XOR               = r'\^'
    t_LSHIFT            = r'<<'
    t_RSHIFT            = r'>>'
    t_LOR               = r'\|\|'
    t_LAND              = r'&&'
    t_LNOT              = r'!'
    t_LT                = r'<'
    t_GT                = r'>'
    t_LE                = r'<='
    t_GE                = r'>='
    t_EQ                = r'=='
    t_NE                = r'!='

    # Assignment operators
    t_EQUALS            = r'='
    t_TIMESEQUAL        = r'\*='
    t_DIVEQUAL          = r'/='
    t_MODEQUAL          = r'%='
    t_PLUSEQUAL         = r'\+='
    t_MINUSEQUAL        = r'-='
    t_LSHIFTEQUAL       = r'<<='
    t_RSHIFTEQUAL       = r'>>='
    t_ANDEQUAL          = r'&='
    t_OREQUAL           = r'\|='
    t_XOREQUAL          = r'\^='

    # Increment/decrement
    t_PLUSPLUS          = r'\+\+'
    t_MINUSMINUS        = r'--'

    # ->
    t_ARROW             = r'->'

    # ?
    t_CONDOP            = r'\?'

    # Delimeters
    t_LPAREN            = r'\('
    t_RPAREN            = r'\)'
    t_LBRACKET          = r'\['
    t_RBRACKET          = r'\]'
    t_COMMA             = r','
    t_PERIOD            = r'\.'
    t_SEMI              = r';'
    t_COLON             = r':'
    t_ELLIPSIS          = r'\.\.\.'

    t_LBRACE            = r'\{'
    t_RBRACE            = r'\}'
    t_TAB               = r'\t'
    # t_SPACE             = r' '

    # A regular expression rule with some action code
    def t_CONSTANT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    @TOKEN(identifier)
    def t_ID(self, t):
        # r'{[a-zA-Z_]}({[a-zA-Z_]}|{[0-9]})*'
        # r'[a-zA-Z_]([a-zA-Z_])*'
        t.type = self.keyword_map.get(t.value, "ID")
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' '

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    # # Build the lexer
    # lexer = lex.lex()


    def __init__(self):
        self.lexer = lex.lex(object=self)

    def load(self, file):
        self.file = file
        with open(self.file, 'r') as f:
            data = f.read()

        self.lexer.input(data)

    def token(self):
        tok = self.lexer.token()
        if tok:
            if tok.type in self.keywords:
                tok.type = 'KEYWORD'
            if tok.type in self.operators:
                tok.type = 'OPERATOR'
            if tok.type in self.assignments:
                tok.type = 'ASSIGNMENT'
            return tok
        else:
            return None

    def reset(self):
        self.lexer.lineno = 1
        self.load(self.file)