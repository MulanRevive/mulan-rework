import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
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
