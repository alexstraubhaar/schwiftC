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


@addToClass(AST.ProgramStatementNode)
def compile(self):
    for c in self.children:
        c.compile()


@addToClass(AST.TokenNode)
def compile(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print("*** Error: variable %s undefined!" % self.tok)
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
    print(self.children[0].compile())


if __name__ == '__main__':
    from parser_schwift import parse
    import sys
    import os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    compiled = ast.compile()
    name = os.path.splittext(sys.argv[1])[0] + '.c'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print("Wrote output to", name)
