import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from 木兰.中 import 中


class test命令行(unittest.TestCase):

    def test_ARGV接收源码文件后的命令行参数(self):
        with TemporaryDirectory() as 临时目录:
            源码文件 = Path(临时目录) / "打印命令行参数.ul"
            源码文件.write_text("println(ARGV)\n", encoding="utf-8")

            输出 = StringIO()
            with redirect_stdout(输出):
                中(["木兰", str(源码文件), "a", "b", "c", "1", "2", "3"])

        self.assertEqual(输出.getvalue(), "[a, b, c, 1, 2, 3]\n")

    def test_ARGV接收执行代码后的命令行参数(self):
        输出 = StringIO()
        with redirect_stdout(输出):
            中(["木兰", "--执行代码=println(ARGV)", "a", "b"])

        self.assertEqual(输出.getvalue(), "[a, b]\n")

    def test_执行代码模式可读取ARGV类型(self):
        输出 = StringIO()
        with redirect_stdout(输出):
            中(["木兰", "--执行代码=println(typeof(ARGV))", "a", "b"])

        self.assertEqual(输出.getvalue(), "list\n")

    def test_执行代码模式可调用辅助输出函数(self):
        输出 = StringIO()
        with redirect_stdout(输出):
            中(["木兰", "--执行代码=__print__('ok')"])

        self.assertEqual(输出.getvalue(), "ok\n")

    def test_源码文件模式设置__file__(self):
        with TemporaryDirectory() as 临时目录:
            源码文件 = Path(临时目录) / "打印文件名.ul"
            源码文件.write_text("println(__file__)\n", encoding="utf-8")

            输出 = StringIO()
            with redirect_stdout(输出):
                中(["木兰", str(源码文件)])

        self.assertEqual(输出.getvalue(), f"{源码文件}\n")

    def test_执行代码模式设置__file__(self):
        输出 = StringIO()
        with redirect_stdout(输出):
            中(["木兰", "--执行代码=println(__file__)"])

        self.assertEqual(输出.getvalue(), "<命令行>\n")

    def test_标准输入流模式设置全局变量(self):
        输出 = StringIO()
        原标准输入 = sys.stdin
        try:
            sys.stdin = StringIO("println(__file__)\nprintln(ARGV)\n")
            with redirect_stdout(输出):
                中(["木兰", "-", "a", "b"])
        finally:
            sys.stdin = 原标准输入

        self.assertEqual(输出.getvalue(), "<标准输入流>\n[a, b]\n")
