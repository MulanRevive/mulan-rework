import ast
import unittest
from xml.etree import ElementTree

from 木兰.分析器.词法分析器 import 分词器
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.生成.blockly import 代码生成器


class Blockly测试(unittest.TestCase):
    def 生成(self, 源码):
        节点 = 语法分析器(分词器).分析(源码, "<测试>")
        xml = 代码生成器().生成(节点)
        return ElementTree.fromstring(xml)

    def test_赋值循环和输出(self):
        根 = self.生成(
            """
total = 0
for current in 1..10 {
  total += current
}
print(total)
"""
        )

        self.assertTrue(根.tag.endswith("xml"))
        命名空间 = {"x": "http://www.w3.org/1999/xhtml"}
        self.assertEqual(根.find("x:variables/x:variable", 命名空间).text, "total")
        块类型 = [块.attrib["type"] for 块 in 根.iter("{http://www.w3.org/1999/xhtml}block")]
        self.assertIn("variables_set", 块类型)
        self.assertIn("controls_for", 块类型)
        self.assertIn("math_arithmetic", 块类型)
        self.assertIn("text_print", 块类型)

    def test_不支持的语句给出明确错误(self):
        节点 = ast.Module(body=[ast.Pass()], type_ignores=[])
        with self.assertRaises(NotImplementedError):
            代码生成器().生成(节点)


if __name__ == "__main__":
    unittest.main()
