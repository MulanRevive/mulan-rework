import unittest
import ast
from 分析器.语法分析器 import 语法分析器
from 分析器.词法分析器 import 分词器

# TODO：需确保无此类 Warning：ParserGeneratorWarning: 28 shift/reduce conflicts
class test语法树(unittest.TestCase):

    def test_词法分析(self):
        # 由于换行也包括在内，"后括号"一词的位置并非 2：1
        各词 = self.分词("{print(2)\n}")
        for 词 in 各词:
            最末 = 词
        self.assertEqual(最末.getstr(), "\n}")
        self.assertEqual(最末.getsourcepos().lineno, 1)
        self.assertEqual(最末.getsourcepos().colno, 10)

    def test_行列号(self):
        节点 = self.生成语法树("print(1/0)")
        expr节点 = self.取子节点(节点, "body", 0)
        call节点 = self.取子节点(expr节点, "value")
        self.assertEqual(call节点.lineno, 1)
        self.assertEqual(call节点.col_offset, 1)

        除法节点 = self.取子节点(call节点, "func")
        self.assertEqual(除法节点.lineno, 1)
        self.assertEqual(除法节点.col_offset, 1)

    # 必须在 Python 3.7 下运行. 注意：木兰源码勿带多余空格，否则行列数不一致。
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

        木兰 = "Module(body=[FunctionDef(name='echo', args=arguments(args=[arg(arg='number', annotation=None, lineno=1, col_offset=11)], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=[Expr(value=Call(func=Name(id='print', ctx=Load(), lineno=2, col_offset=1), args=[Name(id='number', ctx=Load(), lineno=2, col_offset=7)], keywords=[], lineno=2, col_offset=1), lineno=2, col_offset=1)], decorator_list=[], lineno=1, col_offset=1), Expr(value=Call(func=Name(id='echo', ctx=Load(), lineno=4, col_offset=1), args=[Num(n=2, lineno=4, col_offset=6)], keywords=[], lineno=4, col_offset=1), lineno=4, col_offset=1)])"
        节点 = self.生成语法树("func echo(number) {\nprint(number)\n}\necho(2)")
        self.assertEqual(ast.dump(节点, True, True), 木兰)

        木兰 = "Module(body=[ClassDef(name='Person', bases=[], keywords=[], body=[FunctionDef(name='__add__', args=arguments(args=[arg(arg='self', lineno=2, col_offset=12), arg(arg='a', annotation=None, lineno=2, col_offset=13)], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=[Return(value=Call(func=Name(id='Person', ctx=Load(), lineno=2, col_offset=25), args=[BinOp(left=Attribute(value=Name(id='self', ctx=Load(), lineno=2, col_offset=32), attr='name', ctx=Load(), lineno=2, col_offset=32), op=Add(), right=Attribute(value=Name(id='a', ctx=Load(), lineno=2, col_offset=44), attr='name', ctx=Load(), lineno=2, col_offset=44), lineno=2, col_offset=32)], keywords=[], lineno=2, col_offset=25), lineno=2, col_offset=18)], decorator_list=[], lineno=2, col_offset=1), FunctionDef(name='__init__', args=arguments(args=[arg(arg='self', annotation=None, lineno=3, col_offset=1), arg(arg='name', annotation=None, lineno=3, col_offset=14)], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=[Assign(targets=[Attribute(value=Name(id='self', ctx=Load(), lineno=3, col_offset=22), attr='name', ctx=Store(), lineno=3, col_offset=22)], value=Name(id='name', ctx=Load(), lineno=3, col_offset=34), lineno=3, col_offset=22)], decorator_list=[], lineno=3, col_offset=1)], decorator_list=[], lineno=1, col_offset=1)])"
        节点 = self.生成语法树("type Person {\noperator + (a) { return Person(self.name + a.name) }\nfunc $Person(name) { self.name = name }}")
        self.assertEqual(ast.dump(节点, True, True), 木兰)

    def 分词(self, 源码):
        return 分词器.lex(源码)

    def 生成语法树(self, 源码):
        分析器 = 语法分析器()
        return 分析器.分析(源码, '')

    def 取子节点(self, 节点, 子节点名, 索引 = -1):
        for 子节点 in ast.iter_fields(节点):
            if 子节点[0] == 子节点名:
                if isinstance(子节点[1], list):
                    return 子节点[1][索引]
                else:
                    return 子节点[1]

if __name__ == '__main__':
    unittest.main()