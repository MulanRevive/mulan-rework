import unittest

from 编辑器.运行木兰 import 运行木兰代码
from 木兰.分析器.错误 import 语法错误
from 木兰.功用.反馈信息 import *
from 测试.unittest.功用 import *

class test所有(unittest.TestCase):

    def test_运行前报错(self):
        try:
            读源码生成树("测试/错误处理/2.ul")
        except 语法错误 as e:
            self.assertEqual(e.信息, "没认出这个词 \"整数\"")

    def test_运行时报错(self):
        报错 = 运行木兰代码("测试/错误处理/下标越界.ul")
        self.assertEqual(报错[0], 报错_列表索引)
        报错 = 运行木兰代码("测试/错误处理/try随意.ul")
        self.assertEqual(报错[0], "需要添加此属性：__enter__" + 参考_enter)

    def test_列号(self):
        try:
            节点 = 生成语法树("using func")
            self.fail("不该到这")
        except 语法错误 as e:
            self.assertEqual(e.列号, 7)

    def test_行列号(self):
        try:
            读源码生成树("测试/错误处理/词不识.ul")
        except 语法错误 as e:
            self.assertEqual(e.信息, "分词时没认出这个词 \"#\"")
            self.assertEqual(e.行号, 3)
            self.assertEqual(e.列号, 6) # 应该为 1, 在rply 提问: https://github.com/alex/rply/pull/95#issuecomment-729513800
