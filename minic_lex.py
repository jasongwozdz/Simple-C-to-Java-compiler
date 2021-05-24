# Lexer for Cuppa4

import re
from ply import lex

reserved = {
    'print'   : 'PRINT',
    'if'      : 'IF',
    'else'    : 'ELSE',
    'while'   : 'WHILE',
    'for'     : 'FOR',
    'not'     : 'NOT',
    'int'     : 'INTEGER_TYPE',
    'float'   : 'FLOAT_TYPE',
    'string'  : 'STRING_TYPE',
}

literals = [',',';','=','(',')','{','}', '[',']']

tokens = [
          'PLUS','MINUS','TIMES','DIVIDE',
          'EQ','LE',
          'INTEGER', 'FLOAT', 'STRING', 'ID',
          ] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQ      = r'=='
t_LE      = r'<='

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'([0-9]*[.])?[0-9]+'
    t.type = 'FLOAT' if '.' in t.value else 'INTEGER'
    return t

def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1] # strip the quotes
    return t

def t_COMMENT(t):
    r'//.*'
    pass

def t_NEWLINE(t):
    r'\n'
    pass

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# build the lexer
lexer = lex.lex(debug=0)
