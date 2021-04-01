from 木兰.生成 import 木兰

import ast
import unittest

class test所有(unittest.TestCase):

    def test(self):

        语法树节点 = ast.parse("1", "")
        生成器 = 木兰.木兰生成器()
        生成器.visit(语法树节点)
        self.assertEqual("".join(生成器.结果), "1")
