# coding latin-1
import AST
import ply.yacc as yacc
from lex_schwift import tokens

__authors__ = 'Alex and *BURP* Thomas'


# PROGRAMS
def p_program(p):
    """program : program_meeseeks PROGRAM_SEPARATOR program_statement"""
    p[0] = AST.ProgramNode([p[1], p[3]])


def p_program_meeseeks(p):
    """program_meeseeks : meeseek '~'
    | meeseek '~' program_meeseeks"""
    try:
        p[0] = AST.ProgramMeeseeksNode([p[1]] + p[3].children)
    except IndexError:
        p[0] = AST.ProgramMeeseeksNode(p[1])


def p_program_statement(p):
    """program_statement : statement '~'
    | statement '~' program_statement"""
    try:
        p[0] = AST.ProgramStatementNode([p[1]] + p[3].children)
    except IndexError:
        p[0] = AST.ProgramStatementNode(p[1])


# MEESEEKS
def p_meeseeks(p):
    """meeseek : MEESEEKS IDENTIFIER meeseeks_params PIF program_statement DIDIT IDENTIFIER '~' PAF vartype"""
    p[0] = AST.MeeseeksNode([AST.TokenNode(p[2]), p[3], p[5], AST.TokenNode(p[7]), p[10]])


def p_meeseeks_params(p):
    """meeseeks_params : vartype IDENTIFIER
    | vartype IDENTIFIER ',' meeseeks_params"""
    try:
        p[0] = AST.MeeseeksParamNode([p[1], AST.TokenNode(p[2]), p[4]])
    except IndexError:
        p[0] = AST.MeeseeksParamNode([p[1], AST.TokenNode(p[2])])


# STATEMENTS
def p_statement(p):
    """statement : assignation
    | structure
    | SHOWMEWHATYOUGOT '(' expression ')'"""
    try:
        p[0] = AST.SHOWMEWHATYOUGOTNode(AST.TokenNode(p[3]))
    except IndexError:
        p[0] = p[1]


# STRUCTURE
def p_structure_meeseeks_call(p):
    """structure : IDENTIFIER '(' meeseeks_call_param ')'"""
    p[0] = AST.MeeseeksCallNode([AST.TokenNode(p[1]), p[3]])


def p_meeseeks_call_params(p):
    """meeseeks_call_param : IDENTIFIER
    | IDENTIFIER ',' meeseeks_call_param"""
    try:
        p[0] = AST.MeeseeksCallParamNode([AST.TokenNode(p[1]), p[3]])
    except IndexError:
        p[0] = AST.MeeseeksCallParamNode(AST.TokenNode(p[1]))


def p_structure_whale(p):
    """structure : WHALE '(' condition ')' PIF program_statement PAF"""
    p[0] = AST.WhaleNode([p[3], p[6]])


def p_structure_jeez(p):
    """structure : JEEZ '(' condition ')' PIF program_statement PAF"""
    p[0] = AST.JeezNode([p[3], p[6]])


def p_structure_wldd(p):
    """structure : WUBBALUBBADUBDUBS '(' assignation '~' condition '~' assignation ')' PIF program_statement PAF"""
    p[0] = AST.WubbalubbadubdubsNode([p[3], p[5], p[7], p[10]])


def p_structure_cando(p):
    """structure : CANDO PIF program_statement PAF WHALE '(' condition ')'"""
    p[0] = AST.CandoNode([p[7], p[3]])


def p_structure_schwift(p):
    """structure : SCHWIFT '(' IDENTIFIER ')' PIF cases PAF"""
    p[0] = AST.SchwiftNode([AST.TokenNode(p[3]), p[6]])


def p_structure_cases(p):
    """cases : DEFAULT ':' program_statement SHUTUPMORTY '~'
    | HEYRICK expression ':' program_statement SHUTUPMORTY '~' cases"""
    try:
        p[0] = AST.CaseNode([p[2], p[4], p[7]])
    except IndexError:
        p[0] = AST.CaseDefaultNode(p[3])


def p_condition(p):
    """condition : expression FATTEST expression
    | expression FATTER expression
    | expression TINIEST expression
    | expression TINIER expression
    | expression IS expression
    | expression ISNOT expression"""
    p[0] = AST.ConditionNode([p[1], AST.TokenNode(p[2]), p[3]])


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
    """assignation : vartype IDENTIFIER GOT expression"""
    p[0] = AST.Assign([p[1], AST.TokenNode(p[2]), p[4]])


def p_reassign(p):
    """assignation : IDENTIFIER GOT expression"""
    p[0] = AST.ReAssign([AST.TokenNode(p[1]), p[3]])


def p_vartype(p):
    """vartype : HEY
    | THONG
    | ISIT
    | SCHMECKLE
    | MPFH
    | FAKE"""
    p[0] = AST.TokenNode(p[1])


# PRECEDENCES #
precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS')
)


# YACC UTILS #
def p_error(p):
    print("Syntax error in line {} => ({})".format(p.lineno, p))
    p.lexer.skip(1)


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
