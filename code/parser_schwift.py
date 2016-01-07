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

conditions = {
    'FATTEST': lambda x, y: x > y,
    'FATTER': lambda x, y: x >= y,
    'TINIEST': lambda x, y: x < y,
    'TINIER': lambda x, y: x <= y,
    'IS': lambda x, y: x == y,
    'ISNOT': lambda x, y: x != y,
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
    """structure : WHALE '(' condition ')' PIF program PAF
    | JEEZ '(' condition ')' PIF program PAF"""


def p_structure_for(p):
    """structure : WUBBALUBBADUBDUBS '(' assignation '~' condition '~' expression ')' PIF program PAF"""
    p[0] = AST.WubbalubbadubdubsNode([p[3], p[5], p[7], p[10]])


def p_structure_do(p):
    """structure : CANDO PIF condition PAF WHALE '(' condition ')'"""
    p[0] = AST.CandoNode([p[7], p[3]])


def p_structure_switch(p):
    """structure : SCHWIFT '(' IDENTIFIER ')' PIF cases PAF"""
    p[0] = AST.SchwiftNode([p[3], p[5]])


def p_structure_cases(p):
    """cases : DEFAULT ':' program SHUTUPMORTY '~'
    | HEYRICK expression ':' program SHUTUPMORTY '~' cases"""
    p[0] = AST.CaseNode([p[2], p[4], p[7]])


def p_condition(p):
    """condition : expression FATTEST expression
    | expression FATTER expression
    | expression TINIEST expression
    | expression TINIER expression
    | expression IS expression
    | expression ISNOT expression"""
    p[0] = conditions[p[2]](p[1], p[3])


# EXPRESSIONS #
def p_expression_op(p):
    """expression : expression ADD_OP expression
            | expression MUL_OP expression"""
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_number_or_identifier(p):
    """expression : NUMBER
        | IDENTIFIER"""
    p[0] = AST.TokenNode(p[1])


def p_expression_paren(p):
    """expression : '(' expression ')' """
    p[0] = p[2]


def p_expression_minus(p):
    """expression : ADD_OP expression %prec UMINUS"""
    p[0] = AST.OpNode(p[1], [p[2]])


# ASSIGNATION #
def p_assign(p):
    """assignation : HEY IDENTIFIER GOT expression '~'
    | THONG IDENTIFIER GOT expression '~'
    | ISIT IDENTIFIER GOT expression '~'
    | SCHMECKLE IDENTIFIER GOT expression '~'
    | MPFH IDENTIFIER GOT expression '~'
    | FAKE IDENTIFIER GOT expression '~'"""
    p[0] = AST.AssignNode([AST.TokenNode(p[2]), p[4]])


def p_reassign(p):
    """assignation : IDENTIFIER GOT expression '~' """
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


# PRECEDENCES #
precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS')
)


# YACC UTILS #
def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    yacc.errok()


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == '__main__':
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    print(result)

    import os

    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
    graph.write_pdf(name)
    print("wrote ast to", name)
