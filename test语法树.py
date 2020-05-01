import unittest
import ast
from 数分析器 import 语法分析器, 分词器

class test语法树(unittest.TestCase):

    def test_行列号(self):
        节点 = self.生成语法树("2")
        expr节点 = self.取子节点(节点, "body", 0)  # module 节点下可有多个节点
        self.assertEqual(expr节点.lineno, 1)
        self.assertEqual(expr节点.col_offset, 1)

        constant子节点 = self.取子节点(expr节点, "value")
        self.assertEqual(constant子节点.lineno, 1)
        self.assertEqual(constant子节点.col_offset, 1)

        节点 = self.生成语法树("1/0")
        #print(ast.dump(节点, True, True))
        expr节点 = self.取子节点(节点, "body", 0)
        call节点 = self.取子节点(expr节点, "value")
        除法节点 = self.取子节点(call节点, "func")
        self.assertEqual(除法节点.lineno, 1)
        self.assertEqual(除法节点.col_offset, 1)

        # 运算位置
        节点 = self.生成语法树("1+0")
        expr节点 = self.取子节点(节点, "body", 0)
        binop节点 = self.取子节点(expr节点, "value")
        self.assertEqual(binop节点.lineno, 1)
        self.assertEqual(binop节点.col_offset, 1)

        # 第二行
        节点 = self.生成语法树("1+2\n3/4")
        print(ast.dump(节点, True, True))
        print(self.格式化节点(节点, 1))
        第二行expr节点 = self.取子节点(节点, "body", 1)
        call节点 = self.取子节点(第二行expr节点, "value")
        除法节点 = self.取子节点(call节点, "func")
        self.assertEqual(除法节点.lineno, 2)
        self.assertEqual(除法节点.col_offset, 1)

        # 调用
        节点 = self.生成语法树("print(2)")
        expr节点 = self.取子节点(节点, "body", 0)
        call节点 = self.取子节点(expr节点, "value")
        self.assertEqual(call节点.lineno, 1)
        self.assertEqual(call节点.col_offset, 1)

        #节点 = self.生成语法树("print(2/4)")
        #print(ast.dump(节点, True, True))

    def 生成语法树(self, 源码):
        各词 = 分词器.lex(源码)
        分析器 = 语法分析器().创建()
        return 分析器.parse(各词)

    def 取子节点(self, 节点, 子节点名, 索引 = -1):
        for 子节点 in ast.iter_fields(节点):
            if 子节点[0] == 子节点名:
                if isinstance(子节点[1], list):
                    return 子节点[1][索引]
                else:
                    return 子节点[1]

    def 格式化节点(self, 节点, 层次):
        缩进 = "  "
        输出 = ""
        if isinstance(节点, list):
            输出 += "["
            for 子节点 in 节点:
                输出 += self.格式化节点(子节点, 层次 + 1)
            输出 += "]"
        elif isinstance(节点, int):
            输出 += str(节点)
        elif isinstance(节点, str):
            输出 += 节点
        else:
            输出 += type(节点).__name__ + "("
            属性个数 = 0
            for 属性 in ast.iter_fields(节点):
                属性个数 += 1
                输出 += "\n" + 缩进 * 层次 + 属性[0] + "="
                输出 += self.格式化节点(属性[1], 层次 + 1)
            if isinstance(节点, ast.stmt) or isinstance(节点, ast.expr):
                输出 += "\n" + 缩进 * 层次 + "lineno=" + str(节点.lineno)
                输出 += "\n" + 缩进 * 层次 + "col_offset=" + str(节点.col_offset)
            if 属性个数 == 0:
                return 输出 + ")"
            return 输出 + "\n" + 缩进 * (层次 - 1) + ")"
        return 输出

if __name__ == '__main__':
    unittest.main()