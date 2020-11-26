from 测试.期望值表 import 期望值
from 编辑器.运行木兰 import 运行木兰代码

import unittest

class test所有(unittest.TestCase):

    def test(self):
        测试目录 = '测试/'
        全部通过 = True
        失败表 = {}

        for 文件 in 期望值:
            路径 = 测试目录 + 文件
            实际值 = 运行木兰代码(路径)
            预期值 = 期望值[文件].decode("utf-8")

            if 实际值 != 预期值:
                失败表[文件] = 实际值
                全部通过 = False

        for 文件 in 失败表:
            print(f"失败： {文件} 期望：{repr(期望值[文件].decode('utf-8'))} 实际：{repr(失败表[文件])}")
        self.assertTrue(全部通过, "以上用例未通过！")
