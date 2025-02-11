from ast import *
from 木兰.分析器.语法树 import 语法树

'''
注释"研究"的待进一步揣摩
'''
一元操作符 = {
    Not: '!',
    USub: '-',
}
二元操作符 = {
    Add: '+',
    Sub: '-',
    Mult: '*',
    Div: '/',
    FloorDiv: '/',
    Mod: '%',
    Pow: '^',
}
布尔操作符 = {
    And: 'and',
    Or: 'or',
}
比较操作符 = {
    Eq: '==',
    NotEq: '!=',
    Is: '===',
    IsNot: '!==',
    LtE: "<=",
    Lt: '<',
    In: 'in',
    NotIn: "not in",
    GtE: '>=',
    Gt: '>',
}


def 转源码(节点, 缩进量="  "):
    """
    本方法由语法树生成木兰源码，可用于实现 Python 到木兰源码的简单转换工具。
    """
    自述 = "/* 本文件由命令 `木兰 -兰 ` 自动生成. */\n"
    生成器 = 木兰生成器(缩进量, 头部=自述)
    生成器.visit(节点)
    return "".join(生成器.结果)


# TODO: 将各 visit_ 方法名中的术语中文化（方法赋值）
class 木兰生成器(NodeVisitor):

    def __init__(self, 缩进量, 头部=None):
        self.调试 = False
        self.结果 = []
        self.缩进量 = 缩进量
        self.缩进 = 0
        self.行数 = 0
        self.所有类型 = []
        if 头部 is not None:
            self.结果.append(头部)

    def 记录(self, 信息):
        if self.调试:
            print(信息)

    def 编写(self, 文本):
        if not isinstance(文本, str):
            raise AssertionError("未正确处理节点：" + repr(文本))
        if self.行数:
            if self.结果:
                self.结果.append('\n' * self.行数)
            self.结果.append(self.缩进量 * self.缩进)
            self.行数 = 0
        self.结果.append(文本)

    # 待加行号信息
    def 另起一行(self, 节点=None, 额外=0):
        self.行数 = max(self.行数, 1 + 额外)

    def 主体(self, 所有声明):
        self.编写(' {')
        self.缩进 += 1
        for 声明 in 所有声明:
            self.visit(声明)

        self.缩进 -= 1
        self.另起一行()
        self.编写('}')

    def 类型主体(self, 所有声明):
        self.编写(' {')
        self.缩进 += 1
        变量声明 = []

        for 声明 in 所有声明:
            if isinstance(声明, FunctionDef) or isinstance(声明, ClassDef):
                if 变量声明:
                    self.另起一行()
                    self.主体(变量声明)
                    变量声明 = []
                self.visit(声明)
            else:
                变量声明.append(声明)

        if 变量声明:
            self.另起一行()
            self.主体(变量声明)
        self.缩进 -= 1
        self.另起一行()
        self.编写('}')

    def visit_Assign(self, 节点):
        self.另起一行(节点)

        for 索引, 目标 in enumerate(节点.targets):
            if 索引 > 0:
                self.编写(', ')
            self.visit(目标)

        self.编写(' = ')
        self.visit(节点.value)

    def visit_AugAssign(self, 节点):
        self.另起一行(节点)
        self.visit(节点.target)
        self.编写(' ' + 二元操作符[type(节点.op)] + '= ')
        self.visit(节点.value)

    def 形参(self, 节点):
        # TODO: 与 visit_call 内重复，待清理
        需逗号 = []

        def 写逗号():
            if 需逗号:
                self.编写(', ')
            else:
                需逗号.append(True)

        空档 = [None] * (len(节点.args) - len(节点.defaults))
        for 形参, 默认值 in zip(节点.args, 空档 + 节点.defaults):
            写逗号()
            self.visit(形参)
            if 默认值 is not None:
                self.编写("=")
                self.visit(默认值)

        # 实际上木兰的变长形参并非用 * 声明，不知此段何用
        '''
        if 节点.vararg is not None:
            写逗号()
            self.编写('*' + 节点.vararg)
        if 节点.kwarg is not None:
            写逗号()
            self.编写("**" + 节点.kwarg)
        '''

    def visit_FunctionDef(self, 节点):
        self.另起一行(额外=1)
        self.另起一行(节点)

        取值 = False
        赋值 = False
        if 节点.decorator_list:

            # 研究：此处会报错，应为 节点.decorator_list
            for 修饰 in decorator_list:
                print(修饰)
                if isinstance(修饰, Name) and 修饰.id == 'property':
                    取值 = True
                elif isinstance(修饰, Attribute) and 修饰.attr == "setter":
                    赋值 = True
        if 取值:
            assert not 赋值
        if len(self.所有类型) > 0:
            if len(节点.args.args) > 0:
                if 节点.args.args[0].arg == 'self':
                    节点.args.args = 节点.args.args[1:]
                    if 节点.name == '__init__':
                        节点.name = self.所有类型[-1]
                    节点.name = '$' + 节点.name
        if 取值 or 赋值:
            self.编写('attr ')
        else:
            self.编写('func ')

        self.编写('%s%s(' % (节点.name, ' = ' if 赋值 else ''))
        self.visit(节点.args)
        self.编写(')')
        self.主体(节点.body)

    def visit_ClassDef(self, 节点):
        self.所有类型.append(节点.name)
        self.另起一行(额外=2)
        self.另起一行(节点)
        self.编写('type %s' % 节点.name)
        for 基类 in 节点.bases:
            if 基类 != 节点.bases[0]:
                self.编写(', ')
            else:
                self.编写(' : ')
            self.visit(基类)

        self.类型主体(节点.body)

        # 研究：为何不 :-1 ？
        self.所有类型 = self.所有类型[:-2]

    def visit_If(self, 节点):
        self.另起一行(节点)
        self.编写('if ')
        self.visit(节点.test)
        self.主体(节点.body)
        while True:
            否则 = 节点.orelse
            if len(否则) == 0:
                break
            elif len(否则) == 1 and isinstance(否则[0], If):
                节点 = 否则[0]
                self.编写(' elif ')
                self.visit(节点.test)
                self.主体(节点.body)
            else:
                self.编写(' else')
                self.主体(否则)
                break

    def visit_For(self, 节点):
        self.另起一行(节点)
        self.编写('for ')
        self.visit(节点.target)
        self.编写(' in ')
        self.visit(节点.iter)
        self.主体(节点.body)

    def visit_While(self, 节点):
        self.另起一行(节点)
        self.编写('while ')
        self.visit(节点.test)
        self.主体(节点.body)

    def visit_Tuple(self, 节点):
        if isinstance(节点.ctx, Load):
            self.编写('tuple(')
        for 索引, 元素 in enumerate(节点.elts):
            if 索引:
                self.编写(', ')
            self.visit(元素)

        if isinstance(节点.ctx, Load):
            self.编写(')')

    def visit_Try(self, 节点):
        self.另起一行(节点)
        self.编写('try')
        self.主体(节点.body)
        for handler in 节点.handlers:
            self.visit(handler)

        # TODO: final

    def visit_Return(self, 节点):
        self.另起一行(节点)
        self.编写('return')
        if 节点.value is not None:
            self.编写(' ')
            self.visit(节点.value)

    def visit_Attribute(self, 节点):
        if isinstance(节点.value, Name) and 节点.value.id == 'self':
            self.编写('$%s' % 节点.attr)
        elif isinstance(节点.value, Call) and isinstance(节点.value.func, Name) and 节点.value.func.id == 'super':
            self.编写('super')
            if 节点.attr != '__init__':
                self.编写('.' + 节点.attr)
        else:
            self.visit(节点.value)
            self.编写('.' + 节点.attr)

    def visit_Call(self, 节点):
        需逗号 = []

        def 写逗号():
            if 需逗号:
                self.编写(', ')
            else:
                需逗号.append(True)

        self.visit(节点.func)
        self.编写('(')
        for 实参 in 节点.args:
            写逗号()
            self.visit(实参)

        for 关键词 in 节点.keywords:
            写逗号()
            self.编写(关键词.arg + '=')
            self.visit(关键词.value)

        self.编写(')')

    def visit_Name(self, 节点):
        self.记录("Name: " + 节点.id)
        if 节点.id == 'print':
            self.编写('println')
        elif 节点.id == 'chr':
            self.编写('char')
        else:
            self.编写(节点.id)

    def visit_Str(self, 节点):
        self.编写(repr(节点.s))

    def visit_Num(self, 节点):
        self.编写(repr(节点.n))

    def 序列(左括号, 右括号):
        def visit(self, 节点):
            self.编写(左括号)
            for 索引, 项 in enumerate(节点.elts):
                if 索引:
                    self.编写(', ')
                self.visit(项)

            self.编写(右括号)

        return visit

    visit_List = 序列('[', ']')

    def visit_Dict(self, 节点):
        self.编写('{')
        为空 = True
        for 序号, (键, 值) in enumerate(zip(节点.keys, 节点.values)):
            为空 = False
            if 序号:
                self.编写(', ')
            self.visit(键)
            self.编写(': ')
            self.visit(值)

        if 为空:
            self.编写(':')
        self.编写('}')

    def visit_BinOp(self, 节点):
        
        if isinstance(节点.left, BinOp):
            self.编写('(')
            self.visit(节点.left)
            self.编写(')')
        else:
            self.visit(节点.left)
        self.编写(' %s ' % 二元操作符[type(节点.op)])
        if isinstance(节点.right, BinOp):
            self.编写('(')
            self.visit(节点.right)
            self.编写(')')
        else:
            self.visit(节点.right)

    def visit_BoolOp(self, 节点):
        self.编写('(')
        for 索引, 值 in enumerate(节点.values):
            if 索引:
                self.编写(' %s ' % 布尔操作符[type(节点.op)])
            self.visit(值)

        self.编写(')')

    def visit_Compare(self, 节点):
        self.编写('(')
        左边 = 节点.left
        已开头 = False
        for 操作符, 右边 in zip(节点.ops, 节点.comparators):
            if 已开头:
                self.编写(' and ')
            操作符 = 比较操作符[type(操作符)]
            if 'in' in 操作符:
                if "not" in 操作符:
                    self.编写("!")
                self.visit(右边)
                self.编写('.__contains__(')
                self.visit(左边)
                self.编写(')')
            else:
                self.visit(左边)
                self.编写(' %s ' % 操作符)
                self.visit(右边)
            左边 = 右边
            已开头 = True

        self.编写(')')

    # 在 Python3.8 中 Num, Str, NameConstant 节点
    # 统一被 Constant 节点代替，所以使用一个
    # visit_Constant 方法来统一处理三个情况
    def visit_Constant(self, 节点):
        if 语法树.节点为空(节点):
            self.编写('nil')
        elif 语法树.节点为真假值(节点):
            if literal_eval(节点):
                self.编写('true')
            else:
                self.编写('false')
        elif 语法树.节点为字符串(节点):
            self.编写(repr(literal_eval(节点)))
        elif 语法树.节点为数字(节点):
            self.编写(repr(literal_eval(节点)))
        else:
            assert False, "未知的 Constant 节点类型" + repr(节点)

    def visit_UnaryOp(self, 节点):
        self.编写("(")
        操作符 = 一元操作符[type(节点.op)]
        self.编写(操作符)
        self.visit(节点.operand)
        self.编写(")")

    def visit_Subscript(self, 节点):
        self.visit(节点.value)
        self.编写('[')
        self.visit(节点.slice)
        self.编写(']')

    def visit_Slice(self, 节点):
        if 节点.lower is not None:
            self.visit(节点.lower)
        self.编写(':')
        if 节点.upper is not None:
            self.visit(节点.upper)

    def visit_Import(self, node):
        self.另起一行(node)
        self.编写('using ')
        for 索引, 包 in enumerate(node.names):
            if 索引:
                self.编写(', ')
            self.编写(包.name)

        # TODO: 下两行何用？
        # for 包 in node.names:
        #    self.visit(包)

    def visit_ImportFrom(self, node):
        self.另起一行(node)
        self.编写('using ')
        for 索引, 包 in enumerate(node.names):
            if 索引:
                self.编写(', ')
            self.编写(包.name)

        if node.module:
            self.编写(' in %s%s' % ('.' * node.level, node.module))
        else:
            self.编写(' in %s' % ('.' * node.level))

        # TODO: 下两行何用？
        # for item in node.names:
        #    self.visit(item)

    def visit_IfExp(self, 节点):
        self.visit(节点.test)
        self.编写(' ? ')
        self.visit(节点.body)
        self.编写(' : ')
        self.visit(节点.orelse)

    def visit_Expr(self, 节点):
        self.记录("Expr: " + str(节点))
        self.另起一行()
        节点值 = 节点.value
        if 语法树.节点为字符串(节点值):
            self.编写('/* %s */' % literal_eval(节点值))
        else:
            self.visit(节点值)

    def visit_FormattedValue(self, 节点):
        self.编写('str(')
        self.visit(节点.value)
        self.编写(')')

    def visit_NameConstant(self, 节点):
        if 节点.value is None:
            self.编写('nil')
        elif 节点.value:
            self.编写('true')
        else:
            self.编写('false')

    def visit_ExceptHandler(self, 节点):
        self.另起一行(节点)
        self.编写('catch ')
        if 节点.name is not None:
            # 此处原为 self.visit(节点.name)，会报错 AttributeError: 'str' object has no attribute '_fields'
            self.编写(节点.name)
        else:
            self.编写('__')
        if 节点.type is not None:
            self.编写(' : ')
            self.visit(节点.type)
        self.主体(节点.body)

    def visit_arguments(self, 节点):
        self.形参(节点)

    def visit_arg(self, 节点):
        self.编写(节点.arg)


def 转换(节点):
    return 转源码(节点)
