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
        c_code += "\t" + "kek"  # c.compile()
    c_code += ""
    return c_code


@addToClass(AST.MeeseeksNode)
def compile(self):
    c = self.children
    c_code = "{} {}({})\n".format(c[4].compile(), c[0].compile(), c[1].compile())
    c_code += "{{\n\t{}\n}}\n\n".format(c[2].compile(), c[3].compile())
    return c_code


@addToClass(AST.MeeseeksParamNode)
def compile(self):
    c = self.children0
    c_code = "{} {}".format(c[0].compile(), c[1].compile())
    if len(c) > 2:
        c_code += ", {}".format(c[2].compile())
    return c_code


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
    args = [c.compile() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


@addToClass(AST.AssignNode)
def compile(self):
    vars[self.children[0].tok] = self.children[1].compile()


@addToClass(AST.SHOWMEWHATYOUGOTNode)
def compile(self):
    return "printf(\"{}\")".format(self.children[0].compile());


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
