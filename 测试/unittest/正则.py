import re
import unittest
from 木兰.功用.规律 import *

class test正则(unittest.TestCase):

    def test_双引号字符串(self):
        双引号字符串 = r'(")((?<!\\)\\\1|.)*?\1'
        正确字符串 = ['""',
            r'"\""',  # 等价 '"\\""'
            r'"\"a"',
            r'"\c"',  # r'(\")((?<!\\)\\\1|(?<!\\).)*?\1' 不匹配, 因此 ?<! 仅作用于 \\\1 部分
            #r'"\\""'  匹配为 '"\\"'
            r'"\"a\"b"',
            '"abc"',
            r'"\n"',
            ]
        for 字符串 in 正确字符串:
            self.比较(双引号字符串, 字符串, 字符串)
        #TODO： 测试错误字符串

    def test_字符串插值(self):
        插值 = r'\\\(([^\\\)]*)\\\)|`([^`]*)`'
        期望 = {
            r'`ab`': r'`ab`',
            r'\(\)': r'\(\)',  # 不能与正则表达混淆, 反斜杠不需\\
            # r'\(\\)': r'\(\\)', # 不匹配
            # r'\()\)': r'\()\)', # 不匹配
            }
        for 字符串 in 期望:
            self.比较(插值, 字符串, 期望[字符串])

    def 比较(self, 表达式, 全文本, 目标匹配内容):
        m = re.search(表达式, 全文本)
        self.assertEqual(m.group(0), 目标匹配内容, "比较有误")

    def test_规律(self):
        self.assertEqual(序列("a").表达(), r"a")
        self.assertEqual(序列("$").可无().某字("_", 大小写英文, 中文).某字("_", 大小写英文, 数字, 中文).若干().表达(),
            r'\$?[_a-zA-Z\u4e00-\u9fa5][_a-zA-Z0-9\u4e00-\u9fa5]*')

        self.assertEqual(不是(反斜杠, 右小括号).表达(), r'[^\\\)]')

        self.assertEqual(
            任一(
                序列(反斜杠, 左小括号).分段(不是(反斜杠, 右小括号).若干()).序列(反斜杠, 右小括号),
                序列(反引号).分段(不是(反引号).若干()).序列(反引号)
            ).表达(),
            r'\\\(([^\\\)]*)\\\)|`([^`]*)`')

        self.assertEqual(分段(双引号).表达(), r'(\")')

        # TODO：检查引用的分段是否存在
        self.assertEqual(序列(反斜杠, 引用分段(1)).前面不是(反斜杠).表达(), r'(?<!\\)\\\1')
        self.assertEqual(分段(双引号)
            .分段(
                任一(
                    序列(反斜杠, 引用分段(1)).前面不是(反斜杠),
                    序列(非换行字符)
                )
            ).若干().不贪().引用分段(1).表达(),
            r'(\")((?<!\\)\\\1|.)*?\1')

    def test_精通(self):
        self.assertEqual(任一("From", "Subject").表达(), r"From|Subject")
        self.assertEqual(序列(开头, "cat").表达(), r"^cat")
        self.assertEqual(序列(开头, 结尾).表达(), r"^$")
        self.assertEqual(开头, r"^")
        self.assertEqual(序列(开头, 分段(任一("From", "Subject")), 冒号).表达(), r"^(From|Subject):")
        多个数字 = 某字(数字).若干(1)
        self.assertEqual(多个数字.表达(), r"[0-9]+")
        self.assertEqual(序列("<emphasis>", 分段(序列(多个数字, 分段(序列(点号, 多个数字)).若干(3))), "</emphasis>").表达(), r"<emphasis>([0-9]+(\.[0-9]+){3})</emphasis>")
        self.assertEqual(序列("sep", 某字("ea"), "r", 某字("ea"), "te").表达(), r"sep[ea]r[ea]te")
        # 范围: r"<H[1-6]>"

    def test_规律常量(self):
        美元 = r'\$'
        self.assertEqual(
            f'{美元}?[_{大小写英文}{中文}][_{大小写英文}{数字}{中文}]*',
            r'\$?[_a-zA-Z\u4e00-\u9fa5][_a-zA-Z0-9\u4e00-\u9fa5]*')
