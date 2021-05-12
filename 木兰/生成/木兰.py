from ast import *

'''
注释"研究"的待进一步揣摩
'''
比较操作符 = {
    In: 'in'
}

def 转源码(节点, 缩进量="  "):
    """
    本方法由语法树生成木兰源码，可用于实现 Python 到木兰源码的简单转换工具。
    """
    自述 = "/* 本文件由命令 `木兰 -兰 ` 自动生成. */\n"
    生成器 = 木兰生成器(缩进量, 头部=自述)
    生成器.visit(节点)
    return "".join(生成器.结果)

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

    def 形参(self, 节点):
        # TODO: 避免重复
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

    # 待补完
    def visit_Compare(self, 节点):
        self.编写('(')
        左边 = 节点.left
        已开头 = False
        for 操作符, 右边 in zip(节点.ops, 节点.comparators):
            if 已开头:
                self.编写(' and ')
            操作符 = 比较操作符[type(操作符)]
            if 'in' == 操作符:
                self.visit(右边)
                self.编写('.__contains__(')
                self.visit(左边)
                self.编写(')')
            左边 = 右边
            已开头 = True

        self.编写(')')

    def visit_Expr(self, 节点):
        self.记录("Expr: " + str(节点))
        self.另起一行()
        self.visit(节点.value)

    def visit_arguments(self, 节点):
        self.形参(节点)

    def visit_arg(self, 节点):
        self.编写(节点.arg)

def 转换(节点):
    return 转源码(节点)
