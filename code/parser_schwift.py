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

structs = {
    'while': lambda x: AST.WhileNode(x)
}

vars = {}


def p_program_statement(p):
    """ program : statement '~'
     | statement '~' program"""
    try:
        p[0] = AST.ProgramNode([p[1]] + p[3].children)
    except IndexError:
        p[0] = AST.ProgramNode(p[1])


def p_statement(p):
    """statement : assignation
    | structure
    | SHOWMEWHATYOUGOT expression"""
    try:
        p[0] = AST.PrintNode(p[2])
    except IndexError:
        p[0] = p[1]


def p_structure(p):
    """structure: WHILE expression PIF program PAF
    | JEEZ PIF program PAF
    | WUBBALUBBADUBDUBS PIF program PAF"""


def p_assign(p):
    '''assignation : IDENTIFIER got expression '~' '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_structure_inner(p):
    """ kek """
