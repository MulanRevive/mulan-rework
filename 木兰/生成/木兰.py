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

    def visit_Num(self, 节点):
        self.编写(repr(节点.n))

def 转换(节点):
    return 转源码(节点)
