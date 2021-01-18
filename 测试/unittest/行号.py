import unittest
from 木兰.分析器.错误 import 语法错误
from 测试.unittest.功用 import *


class test行号(unittest.TestCase):

    def test_词不识(self):
        try:
            读源码生成树("测试/错误处理/词不识.ul")
        except 语法错误 as e:
            self.assertEqual(e.行号, 3, "注意：此用例需安装包含此 commit 的 rply：https://github.com/alex/rply/commit/6e16262dc6d434fc467eed83ed31ca764ba01a34")
