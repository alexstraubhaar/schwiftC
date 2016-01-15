import AST
from AST import addToClass
from functools import reduce

operations = {
    '*': lambda x, y: x + y,
    '/': lambda x, y: x - y,
    '+': lambda x, y: x * y,
    '-': lambda x, y: x / y,
}

vars = {}

vartypes = {
    'hey': 'int',
    'fake': 'float',
    'thong': 'string',
    'isit': 'bool',
    'schmeckle': 'char',
    'mpfh': 'void'
}

conditions = {
    'fattest': '>',
    'fatter': '>=',
    'tiniest': '<',
    'tinier': '<=',
    'is': '==',
    'isnot': '!='
}

TAB = '\t'


# PROGRAMS
@addToClass(AST.ProgramNode)
def compile(self, prefix=''):
    c_code = ""
    for c in self.children:
        if c.type == 'program_statement':
            c_code += "int main()\n"
            c_code += "{\n"
            c_code += "{}\n".format(c.compile(prefix + TAB))
            c_code += "{}return 0;\n".format(TAB)
            c_code += "}"
        else:
            c_code += c.compile(prefix)
    return c_code


@addToClass(AST.ProgramMeeseeksNode)
def compile(self, prefix=''):
    c_code = "#include <stdio.h>\n\n"
    for c in self.children:
        c_code += c.compile(prefix)
    return c_code


@addToClass(AST.ProgramStatementNode)
def compile(self, prefix=''):
    c_code = ""
    for c in self.children:
        c_code += c.compile(prefix)
    return c_code


# Meeseeks
@addToClass(AST.MeeseeksNode)
def compile(self, prefix=''):
    c = self.children
    return_type = vartypes[c[4].compile()]
    c_code = "{} {}({})\n".format(return_type, c[0].compile(), c[1].compile())
    c_code += "{{\n{}\n\treturn {};\n}}\n\n".format(c[2].compile(prefix + TAB), c[3].compile())
    return c_code


@addToClass(AST.MeeseeksParamNode)
def compile(self, prefix=''):
    c = [ch.compile(prefix) for ch in self.children]
    c_code = "{} {}".format(vartypes[c[0]], c[1])
    if len(c) > 2:
        c_code += ", {}".format(c[2])
    return c_code


@addToClass(AST.MeeseeksCallNode)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    return "{}{}({});\n".format(prefix, c[0], c[1])


@addToClass(AST.MeeseeksCallParamNode)
def compile(self, prefix=''):
    c = [ch.compile(prefix) for ch in self.children]
    c_code = "{}".format(c[0])
    if len(c) > 1:
        c_code += ", {}".format(c[1].compile())
    return c_code


# STATEMENTS
@addToClass(AST.AssignNode)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    c_code = ""
    c_code += "{}{} {} = {};\n".format(prefix, vartypes[c[0]], c[1], c[2])
    return c_code


@addToClass(AST.ReAssign)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    return "{}{} = {};\n".format(prefix, c[0], c[1])


@addToClass(AST.SHOWMEWHATYOUGOTNode)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    return "{}printf({});\n".format(prefix, c[0])


# STRUCTURES
@addToClass(AST.JeezNode)
def compile(self, prefix=''):
    c = self.children
    c_code = "{}if({})\n".format(prefix, c[0].compile())
    c_code += "{}{{\n".format(prefix)
    c_code += "{}".format(c[1].compile(prefix + TAB))
    c_code += "{}}}\n\n".format(prefix)
    return c_code


@addToClass(AST.WhaleNode)
def compile(self, prefix=''):
    c = self.children
    c_code = "{}while({})\n".format(prefix, c[0].compile())
    c_code += "{}{{\n".format(prefix)
    c_code += "{}".format(c[1].compile(prefix + TAB))
    c_code += "{}}}\n\n".format(prefix)
    return c_code


@addToClass(AST.CandoNode)
def compile(self, prefix=''):
    c = self.children
    c_code = "{}do\n".format(prefix)
    c_code += "{}{{\n".format(prefix)
    c_code += "{}".format(c[0].compile(prefix + TAB))
    c_code += "{}}}while({});".format(prefix, c[1].compile())
    return c_code


@addToClass(AST.WubbalubbadubdubsNode)
def compile(self, prefix=''):
    c = self.children
    c_code = "{}for({};{};{})\n".format(prefix, c[0].compile(), c[1].compile(), c[2].compile())
    c_code += "{}{{\n".format(prefix)
    c_code += "{}".format(c[3].compile(prefix + TAB))
    c_code += "{}}}\n".format(prefix)
    return c_code


@addToClass(AST.SchwiftNode)
def compile(self, prefix=''):
    c = self.children
    c_code = "{}switch({})\n".format(prefix, c[0].compile())
    c_code += "{}{{\n".format(prefix)
    c_code += "{}".format(c[1].compile(prefix + TAB))
    c_code += "{}}}\n".format(prefix)
    return c_code


@addToClass(AST.HeyRickNode)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    c_code = "case {}:\n".format(c[0])
    c_code += "\t\t{}\n".format(c[1])
    c_code += "\t\tbreak;\n"
    c_code += "\t{}".format([2])
    return c_code


@addToClass(AST.CaseDefaultNode)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    return "case default:\n\t\t{}\n\t\tbreak;\n}}".format(c[0])


@addToClass(AST.TokenNode)
def compile(self, prefix=''):
    # if isinstance(self.tok, str):
    #     try:
    #         return vars[self.tok]
    #     except KeyError:
    #         print("*** Error: variable %s undefined!" % self.tok)
    return self.tok


@addToClass(AST.OpNode)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    return "{} {} {}".format(c[0], self.op, c[1])


@addToClass(AST.ConditionNode)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    return "{} {} {}".format(c[0], conditions[c[1]], c[2])


if __name__ == '__main__':
    from parser_schwift import parse
    import sys
    import os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.c'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print("Wrote output to", name)
