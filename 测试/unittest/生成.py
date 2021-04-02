from 木兰.生成 import 木兰

import ast
import unittest

# TODO: 确保生成的木兰代码运行效果与 Python 相同

期望值 = {
    "1.py": "1",
    "标识符.py": "某量",
    "函数/无实参.py": "func a() {\nprintln(1)\n}\na()", # TODO: 文本置于文件中？
    "函数/调用单个实参.py": "a(1)",
    "函数/调用多个实参.py": "a(1, 2)",
    "函数/调用指名参数.py": "a(x=1)",
    "函数/调用print.py": "println(1)",
    "函数/调用chr.py": "char(97)",
    "函数/调用多层.py": "output(add(2))",
    "函数/二阶函数.py": "println(increment(10)(1))",
    "特殊字符/多行.py": "println(2)\nprintln(3)",
}

class test所有(unittest.TestCase):

    def test(self):
        for 文件 in 期望值:
            路径 = "测试/unittest/源码生成/python/" + 文件
            with open(路径, 'r', encoding='utf-8') as f:
                源码 = f.read()

            语法树节点 = ast.parse(源码, 路径)
            生成器 = 木兰.木兰生成器()
            生成器.visit(语法树节点)
            self.assertEqual("".join(生成器.结果), 期望值[文件], 文件 + " 转换错误")
