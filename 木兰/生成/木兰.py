from ast import NodeVisitor

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
        self.结果 = []
        self.缩进量 = 缩进量
        self.缩进 = 0
        self.行数 = 0
        if 头部 is not None:
            self.结果.append(头部)

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

    def class_body(self, 所有声明):
        self.编写(' {')
        self.缩进 += 1
        self.另起一行()
        self.主体([])
        self.缩进 -= 1
        self.另起一行()
        self.编写('}')

    # 待补全
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

        if 节点.kwarg is not None:
            写逗号()
            # 实际上木兰的变长形参并非如此声明，不知此何用
            self.编写("**" + 节点.kwarg)

    # 待补全：类方法等
    def visit_FunctionDef(self, 节点):
        self.另起一行(额外=1)
        self.另起一行(节点)
        self.编写('func ')
        self.编写('%s(' % 节点.name)
        self.visit(节点.args)
        self.编写(')')
        self.主体(节点.body)

    def visit_ClassDef(self, 节点):
        self.另起一行(额外=2)
        self.另起一行(节点)
        self.编写('type %s' % 节点.name)

        self.class_body(节点.body)

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
        if 节点.id == 'print':
            self.编写('println')
        elif 节点.id == 'chr':
            self.编写('char')
        else:
            self.编写(节点.id)

    def visit_Num(self, 节点):
        self.编写(repr(节点.n))

    def visit_Expr(self, 节点):
        self.另起一行()
        self.visit(节点.value)

    def visit_arguments(self, 节点):
        self.形参(节点)

    def visit_arg(self, 节点):
        self.编写(节点.arg)

def 转换(节点):
    return 转源码(节点)
