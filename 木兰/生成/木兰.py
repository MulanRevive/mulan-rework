from ast import NodeVisitor

def 转源码(节点, 缩进="  "):
    """
    本方法由语法树生成木兰源码，可用于实现 Python 到木兰源码的简单转换工具。
    """
    自述 = "/* 本文件由命令 `木兰 -兰 ` 自动生成. */\n"
    生成器 = 木兰生成器(头部=自述)
    生成器.visit(节点)
    return "".join(生成器.结果)

class 木兰生成器(NodeVisitor):

    def __init__(self, 头部=None):
        self.结果 = []
        if 头部 is not None:
            self.结果.append(头部)

    def 编写(self, 文本):
        self.结果.append(文本)

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
        self.编写(节点.id)

    def visit_Num(self, 节点):
        self.编写(repr(节点.n))

def 转换(节点):
    return 转源码(节点)
