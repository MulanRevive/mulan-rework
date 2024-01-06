from 木兰.生成 import 木兰

import ast
import unittest

from 测试.unittest.生成源码表 import 木兰源码表, python源码表

头部信息 = "/* 本文件由命令 `木兰 -兰 ` 自动生成. */\n"

# 注意：所有测试用源码切勿在末尾加空行，否则比较有误

# TODO: 确保生成的木兰代码运行效果与 Python 相同
# 如果用例与木兰功能测试用例有相当重合，考虑复用


class test所有(unittest.TestCase):

    def test(self):
        for python路径 in 木兰源码表:
            python源码 = python源码表[python路径]
            木兰源码 = 木兰源码表[python路径]

            语法树节点 = ast.parse(python源码, python路径)
            生成器 = 木兰.木兰生成器("  ", 头部信息)
            生成器.visit(语法树节点)
            生成源码 = "".join(生成器.结果)
            self.assertEqual(生成源码, 头部信息 + "\n" + 木兰源码, python路径 + " 转换错误")
