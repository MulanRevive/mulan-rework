import ast

# 提取所有标识符后分析使用的术语与短语句式

class 标识符提取器(ast.NodeVisitor):

    def __init__(self):
        self.调试 = True
        self.所有标识符 = []

    def 日志(self, 信息):
        if self.调试:
            print(信息)

    def 记录(self, 文本):
        if not isinstance(文本, str):
            raise AssertionError("未正确处理节点：" + repr(文本))
        self.所有标识符.append(文本)

    def visit_Name(self, 节点):
        self.日志("Name: " + 节点.id)
        self.记录(节点.id)

python路径 = '木兰/分析器/词法分析器.py' # '辅助工具/标识符提取.py'
with open(python路径, 'r', encoding='utf-8') as f:
    python源码 = f.read()
语法树节点 = ast.parse(python源码, python路径)
提取器 = 标识符提取器()
提取器.visit(语法树节点)