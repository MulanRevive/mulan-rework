
import codegen
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

    def write(self, 内容):
        if self.new_lines:
            if self.result:
                self.result.append('\r\n' * self.new_lines)
            self.result.append(self.indent_with * self.indentation)
            self.new_lines = 0
        self.result.append(内容)

    def visit_arg(self, 参数节点):
        super().write(参数节点.arg)

    def visit_ClassDef(self, 节点):
        有形式参数 = []

        def 得到括号或逗号():
            nonlocal 有形式参数
            if 有形式参数:
                self.write(', ')
            else:
                有形式参数.append(True)
                self.write('(')

        self.newline(extra=2)
        self.decorators(节点)
        self.newline(节点)
        self.write('class %s' % 节点.name)

        for 基类 in 节点.bases:
            得到括号或逗号()
            self.visit(基类)

        if hasattr(节点, 'keywords'):
            for 关键字参数 in 节点.keywords:
                得到括号或逗号()
                self.write(关键字参数.arg + '=')
                self.visit(关键字参数.value)
        self.write(有形式参数 and '):' or ':')
        self.body(节点.body)

    def visit_AnnAssign(self, 节点):
        self.newline(节点)
        self.visit(节点.target)
        self.write(' : ')
        self.visit(节点.annotation)
        self.write(' = ')
        self.visit(节点.value)

    def visit_Name(self, 节点):
        if 节点.id == 'PI':
            self.write('pi')
        else:
            super().visit_Name(节点)

    def visit_NameConstant(self, 节点):
        if 节点.value == None:
            self.write('None')
        elif 节点.value:
            self.write('True')
        else:
            self.write('False')

    def visit_Call(self, 节点):
        if isinstance(节点.func, ast.Name):
            if 节点.func.id in 木兰预置函数映射表:
                节点.func.id = 木兰预置函数映射表[节点.func.id]
        
        需要逗号 = []
        def 写逗号至结果():
            if 需要逗号:
                self.write(', ')
            else:
                需要逗号.append(True)

        self.visit(节点.func)
        self.write('(')
        for 参数节点 in 节点.args:
            写逗号至结果()
            self.visit(参数节点)
        for 关键字参数节点 in 节点.keywords:
            写逗号至结果()
            self.write(关键字参数节点.arg + '=')
            self.visit(关键字参数节点.value)
        self.write(')')

    def visit_With(self, 节点):
        self.newline(节点)
        self.write('with ')

        for 索引, 项 in enumerate(节点.items):
            if 索引 > 0:
                self.write(', ')
            self.visit(项)

        self.write(':')
        self.body(节点.body)

    def visit_ExtSlice(self, 节点):
        for 索引, 切片项 in enumerate(节点.dims):
            if 索引 != 0:
                self.write(', ')
            self.visit(切片项)

    def visit_withitem(self, 节点):
        self.visit(节点.context_expr)
        
        if 节点.optional_vars is not None:
            self.write(' as ')
            self.visit(节点.optional_vars)

    def visit_ImportFrom(self, 节点):
        self.newline(节点)
        if 节点.module:
            self.write('from %s%s import ' % ('.' * 节点.level, 节点.module))
        else:
            self.write('from %s import ' % ('.' * 节点.level))

        for 索引, 项 in enumerate(节点.names):
            if 索引:
                self.write(', ')
            self.visit(项)

    def signature(self, 节点):
        需要逗号 = []

        def 写逗号至结果():
            if 需要逗号:
                self.write(', ')
            else:
                需要逗号.append(True)

        对齐辅助列表 = [None] * (len(节点.args) - len(节点.defaults))

        for 参数, 默认项 in zip(节点.args, 对齐辅助列表 + 节点.defaults):
            写逗号至结果()
            self.visit(参数)
            if 默认项 is not None:
                self.write('=')
                self.visit(默认项)

        if 节点.vararg is not None:
            写逗号至结果()
            self.write('*' + 节点.vararg.arg)

        if 节点.kwarg is not None:
            写逗号至结果()
            self.write('**' + 节点.kwarg.arg)

    def 得到源码(self, 节点):
        self.visit(节点)

        self.result.insert(
            0, 'import sys\r\nfrom math import *\r\nARGV = sys.argv[1:]\r\n')
        
        return ''.join(self.result) + '\r\n'

