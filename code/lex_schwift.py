import ply.lex as lex

__authors__ = 'Alex and *BURP* Thomas'

var_types = {
    'hey',  # int
    'fake',  # float
    'thong',  # string
    'isit',  # bool
    'schmeckle',  # char
    'mpfh',  # void
}

reserved_words = {
    # Conditions
    'got',  # =
    'tiniest',  # <
    'tinier',  # <=
    'fattest',  # >
    'fatter',  # >=
    'is',  # ==
    'isnot',  # !=

    # Var types
    'hey',  # int
    'fake',  # float
    'thong',  # string
    'isit',  # bool
    'schmeckle',  # char
    'mpfh',  # void

    # Structures
    'jeez',  # if
    'schwift',  # switch
    'heyrick',  # case
    'shutupmorty',  # break
    'default',
    'cando',  # do
    'SHOWMEWHATYOUGOT',  # print
    'wubbalubbadubdubs',  # for
    'whale',  # while

    # Methods
    'meeseeks', # function
    'didit',  # return

    # PIF PAF
    'PIF',  # {
    'PAF'  # }
}

tokens = (
             'PROGRAM_SEPARATOR',
             'NUMBER',
             'ADD_OP',
             'MUL_OP',
             'IDENTIFIER'
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '()~:,'


def t_PROGRAM_SEPARATOR(t):
    r'[=]{42}'
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


def t_ADD_OP(t):
    r'\*|/'
    return t


def t_MUL_OP(t):
    r'\+|-'
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()

if __name__ == '__main__':
    import sys

    prog = open(sys.argv[1]).read()
    lex.input(prog)
    while 1:
        tok = lex.token()
        if not tok:
            break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
