
from . import codegen

import ast


木兰预置函数映射表 = {
    'println': 'print',
    'tuple': '',
    'char': 'chr',
    'isa': 'isinstance',
    'ceil': 'math.ceil',
    'floor': 'math.floor',
    'fabs': 'math.fabs',
    'sqrt': 'math.sqrt',
    'log': 'math.log',
    'log10': 'math.log10',
    'exp': 'math.exp',
    'pow': 'math.pow',
    'sin': 'math.sin',
    'cos': 'math.cos',
    'tan': 'math.tan',
    'asin': 'math.asin',
    'acos': 'math.acos'
}


class 代码生成器(codegen.SourceGenerator):
    def __init__(self):
        super().__init__('  ', False)

    def write(self, x):
        if self.new_lines:
            if self.result:
                self.result.append('\r\n' * self.new_lines)
            self.result.append(self.indent_with * self.indentation)
            self.new_lines = 0
        self.result.append(x)

    def visit_arg(self, arg):
        super().write(arg.arg)

    def visit_AnnAssign(self, node):
        self.newline(node)
        self.visit(node.target)
        self.write(' : ')
        self.visit(node.annotation)
        self.write(' = ')
        self.visit(node.value)

    def visit_Name(self, node):
        if node.id == 'PI':
            self.write('pi')
        else:
            super().visit_Name(node)

    def visit_NameConstant(self, node):
        if node.value == None:
            self.write('None')
        elif node.value:
            self.write('True')
        else:
            self.write('False')

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in 木兰预置函数映射表:
                node.func.id = 木兰预置函数映射表[node.func.id]
        super().visit_Call(node)

    def visit_With(self, node):
        self.newline(node)
        self.write('with ')

        for idx, item in enumerate(node.items):
            if idx > 0:
                self.write(', ')
            self.visit(item)

        self.write(':')
        self.body(node.body)

    def visit_ExtSlice(self, node):
        for idx, s in enumerate(node.dims):
            if idx != 0:
                self.write(', ')
            self.visit(s)

    def visit_withitem(self, node):
        self.visit(node.context_expr)
        
        if node.optional_vars is not None:
            self.write(' as ')
            self.visit(node.optional_vars)

    def visit_ImportFrom(self, node):
        self.newline(node)
        if node.module:
            self.write('from %s%s import ' % ('.' * node.level, node.module))
        else:
            self.write('from %s import ' % ('.' * node.level))

        for idx, item in enumerate(node.names):
            if idx:
                self.write(', ')
            self.visit(item)

    def signature(self, node):
        want_comma = []

        def write_comma():
            if want_comma:
                self.write(', ')
            else:
                want_comma.append(True)

        padding = [None] * (len(node.args) - len(node.defaults))

        for arg, default in zip(node.args, padding + node.defaults):
            write_comma()
            self.visit(arg)
            if default is not None:
                self.write('=')
                self.visit(default)

        if node.vararg is not None:
            write_comma()
            self.write('*' + node.vararg.arg)

        if node.kwarg is not None:
            write_comma()
            self.write('**' + node.kwarg.arg)

    def 得到源码(self, node):
        self.visit(node)

        self.result.insert(
            0, 'import sys\r\nfrom math import *\r\nARGV = sys.argv[1:]\r\n')
        
        return ''.join(self.result) + '\r\n'

