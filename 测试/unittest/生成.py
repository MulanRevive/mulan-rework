from 木兰.生成 import 木兰

import ast
import os
import unittest

# TODO: 确保生成的木兰代码运行效果与 Python 相同
# 如果用例与木兰功能测试用例有相当重合，考虑复用

源码目录 = "测试/unittest/源码生成/"

原始木兰未过 = {
    "变长指名参数.py": "TypeError: can only concatenate str (not \"arg\") to str",
}


class test所有(unittest.TestCase):

    def test(self):

        for 路径, 目录名, 所有文件 in os.walk(源码目录):
            for 文件 in 所有文件:
                文件名 = os.path.splitext(os.path.join(路径, 文件))
                if 文件名[1] == '.py' and 文件 not in 原始木兰未过:
                    self.比较(文件名[0])

    def 比较(self, python文件名):
        python路径 = python文件名 + '.py'
        with open(python路径, 'r', encoding='utf-8') as f:
            python源码 = f.read()

        木兰路径 = python文件名 + ".ul"
        if os.path.isfile(木兰路径):
            with open(木兰路径, 'r', encoding='utf-8') as f:
                木兰源码 = f.read()
        else:
            木兰源码 = python源码

        语法树节点 = ast.parse(python源码, python路径)
        生成器 = 木兰.木兰生成器("  ")
        生成器.visit(语法树节点)
        self.assertEqual("".join(生成器.结果), 木兰源码, python路径 + " 转换错误")
