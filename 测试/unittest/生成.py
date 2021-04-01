from 木兰.生成 import 木兰

import ast
import unittest

期望值 = {
    "1.py": "1",
    "标识符.py": "某量",
    "函数/调用无实参.py": "操作()",
    "函数/调用单个实参.py": "操作(1)",
    "函数/调用多个实参.py": "操作(1, 2)",
    "函数/调用指名参数.py": "操作(x=1)",
}

class test所有(unittest.TestCase):

    def test(self):
        for 文件 in 期望值:
            路径 = "测试/unittest/python源码/" + 文件
            with open(路径, 'r', encoding='utf-8') as f:
                源码 = f.read()

            语法树节点 = ast.parse(源码, 路径)
            生成器 = 木兰.木兰生成器()
            生成器.visit(语法树节点)
            self.assertEqual("".join(生成器.结果), 期望值[文件], 文件 + " 转换错误")
