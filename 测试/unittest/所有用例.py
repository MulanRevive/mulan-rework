from 测试.期望值表 import *
from 编辑器.运行木兰 import 运行木兰代码

import unittest

class test所有(unittest.TestCase):

    def test(self):
        路径 = '测试/'
        for 文件 in 期望值:
            源码路径 = 路径 + 文件
            self.assertEqual(运行木兰代码(源码路径), 期望值[文件].decode("utf-8"), 文件 + " 失败")
