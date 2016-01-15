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


# PROGRAMS
@addToClass(AST.ProgramNode)
def compile(self):
    c_code = ""
    for c in self.children:
        if c.type == 'program_statement':
            c_code += "int main()\n{\n"
        c_code += c.compile()
        if c.type == 'program_statement':
            c_code += "\n\treturn 0;\n}"
    return c_code


@addToClass(AST.ProgramMeeseeksNode)
def compile(self):
    c_code = "#include <stdio.h>\n\n"
    for c in self.children:
        c_code += c.compile()
    return c_code


@addToClass(AST.ProgramStatementNode)
def compile(self):
    c_code = ""
    for c in self.children:
        c_code += "\t" + c.compile()
    c_code += ""
    return c_code


# Meeseeks
@addToClass(AST.MeeseeksNode)
def compile(self):
    c = self.children
    return_type = vartypes[c[4].compile()]
    c_code = "{} {}({})\n".format(return_type, c[0].compile(), c[1].compile())
    c_code += "{{\n\t{}\n}}\n\n".format(c[2].compile(), c[3].compile())
    return c_code


@addToClass(AST.MeeseeksParamNode)
def compile(self):
    c = self.children
    c_code = "{} {}".format(vartypes[c[0].compile()], c[1].compile())
    if len(c) > 2:
        c_code += ", {}".format(c[2].compile())
    return c_code


@addToClass(AST.MeeseeksCallNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "{}({});\n".format(c[0], c[1])


@addToClass(AST.MeeseeksCallParamNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    c_code = "{}".format(c[0])
    if len(c) > 1:
        c_code += ", {}".format(c[1].compile())
    return c_code


# STATEMENTS
@addToClass(AST.AssignNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "{} {} = {};\n".format(c[0], c[1], c[2])


@addToClass(AST.ReAssign)
def compile(self):
    return "{} = {};\n".format(self.children[0].compile(), self.children[0].compile())


@addToClass(AST.SHOWMEWHATYOUGOTNode)
def compile(self):
    return "printf({});".format(self.children[0].compile())


# STRUCTURES
@addToClass(AST.JeezNode)
def compile(self):
    c = self.children
    return "if({})\n{{\t{}\n}}\n\n".format(c[0].compile(), c[1].compile())


@addToClass(AST.WhaleNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "whale({})\n{{\t{}\n}}\n\n".format(c[0], c[1])


@addToClass(AST.CandoNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "do\n{{\t{}\n}}while({});\n\n".format(c[0], c[1])


@addToClass(AST.WubbalubbadubdubsNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "for({};{};{})\n{{\n\t{}\n}}\n\n".format(c[0], c[1], c[2], c[3])


@addToClass(AST.SchwiftNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "switch({})\n{{\n\t{}\n}}\n\n".format(c[0], c[1])


@addToClass(AST.CaseNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    c_code = "case {}:\n".format(c[0])
    c_code += "\t\t{}\n".format(c[1])
    c_code += "\t\tbreak;\n"
    c_code += "\t{}".format([2])
    return c_code


@addToClass(AST.CaseDefaultNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "case default:\n\t\t{}\n\t\tbreak;\n}}".format(c[0])


@addToClass(AST.TokenNode)
def compile(self):
    # if isinstance(self.tok, str):
    #     try:
    #         return vars[self.tok]
    #     except KeyError:
    #         print("*** Error: variable %s undefined!" % self.tok)
    return self.tok


@addToClass(AST.OpNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "{} {} {}".format(c[1], c[0], c[2])


@addToClass(AST.SHOWMEWHATYOUGOTNode)
def compile(self):
    return "printf(\"{}\")".format(self.children[0].compile());


@addToClass(AST.ConditionNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "{} {} {}".format(c[0], c[1], c[2])


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
