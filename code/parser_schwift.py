__author__ = 'Alex'

import ply.yacc as yacc
from lex_schwift import tokens

operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'big+' : lambda x,y: x*y,
	'big-' : lambda x,y: x/y,
}

vars = {}

def p_program_statement(p):
	''' program : statement '''
	p[0] = p[1]

def p_program_recursive(p):
	''' program : statement '\n' program '''
	p[1] = p[2] + p[3]