import unittest
import ast
from 分析器 import 语法分析器
from 词法分析器 import 分词器
from 功用 import 语法树相关

class test语法树(unittest.TestCase):

    def test_行列号(self):
        节点 = self.生成语法树("print(1/0)")
        expr节点 = self.取子节点(节点, "body", 0)
        call节点 = self.取子节点(expr节点, "value")
        self.assertEqual(call节点.lineno, 1)
        self.assertEqual(call节点.col_offset, 1)

        除法节点 = self.取子节点(call节点, "func")
        self.assertEqual(除法节点.lineno, 1)
        self.assertEqual(除法节点.col_offset, 1)

    # 必须在 Python 3.7 下运行.
    def test_整树比较(self):
        木兰 = "Module(body=[Expr(value=Call(func=Name(id='print', ctx=Load(), lineno=1, col_offset=1), args=[Num(n=2, lineno=1, col_offset=7)], keywords=[], lineno=1, col_offset=1), lineno=1, col_offset=1)])"
        节点 = self.生成语法树("print(2)")
        self.assertEqual(ast.dump(节点, True, True), 木兰)

        木兰 = "Module(body=[Expr(value=Call(func=Name(id='print', ctx=Load(), lineno=1, col_offset=1), args=[Num(n=0, lineno=1, col_offset=7)], keywords=[], lineno=1, col_offset=1), lineno=1, col_offset=1), Expr(value=Call(func=Name(id='print', ctx=Load(), lineno=2, col_offset=1), args=[BinOp(left=BinOp(left=Num(n=1, lineno=2, col_offset=7), op=Add(), right=BinOp(left=Num(n=2, lineno=2, col_offset=9), op=Mult(), right=Num(n=3, lineno=2, col_offset=11), lineno=2, col_offset=9), lineno=2, col_offset=7), op=Sub(), right=Call(func=Name(id='__div__', ctx=Load(), lineno=2, col_offset=13), args=[Num(n=4, lineno=2, col_offset=13), Num(n=5, lineno=2, col_offset=15)], keywords=[], lineno=2, col_offset=13), lineno=2, col_offset=7)], keywords=[], lineno=2, col_offset=1), lineno=2, col_offset=1)])"
        节点 = self.生成语法树("print(0)\nprint(1+2*3-4/5)")
        self.assertEqual(ast.dump(节点, True, True), 木兰)

        木兰 = "Module(body=[Assign(targets=[Name(id='a', ctx=Store(), lineno=1, col_offset=1)], value=Num(n=2, lineno=1, col_offset=3), lineno=1, col_offset=1), Expr(value=Call(func=Name(id='print', ctx=Load(), lineno=2, col_offset=1), args=[Name(id='a', ctx=Load(), lineno=2, col_offset=7)], keywords=[], lineno=2, col_offset=1), lineno=2, col_offset=1)])"
        节点 = self.生成语法树("a=2\nprint(a)")
        self.assertEqual(ast.dump(节点, True, True), 木兰)

    def 生成语法树(self, 源码):
        各词 = 分词器.lex(源码)
        分析器 = 语法分析器().创建()
        return 分析器.parse(各词)

    def 取子节点(self, 节点, 子节点名, 索引 = -1):
        for 子节点 in ast.iter_fields(节点):
            if 子节点[0] == 子节点名:
                if isinstance(子节点[1], list):
                    return 子节点[1][索引]
                else:
                    return 子节点[1]

if __name__ == '__main__':
    unittest.main()