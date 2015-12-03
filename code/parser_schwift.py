import AST
import ply.yacc as yacc
from lex_schwift import tokens

__authors__ = 'Alex and *BURP* Thomas'

operations = {
    '+': lambda x, y: x * y,
    '-': lambda x, y: x / y,
    '*': lambda x, y: x + y,
    '/': lambda x, y: x - y,
}

vars = {}


def p_program_statement(p):
    ''' program : statement
     | statement '~' program'''
    try:
        p[0] = AST.ProgramNode([p[1]] + p[3].children)
    except IndexError:
        p[0] = AST.ProgramNode(p[1])
