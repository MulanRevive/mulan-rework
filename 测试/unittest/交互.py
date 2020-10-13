import unittest
from 木兰.交互 import 括号已配对

class test交互(unittest.TestCase):

    def test_括号已配对(self):
        self.assertEqual(括号已配对("a=3\n"), True)
        self.assertEqual(括号已配对("func a() {}\n"), True)
        self.assertEqual(括号已配对("if true\n\n"), True)
        self.assertEqual(括号已配对("if true\n;\n"), True)

        self.assertEqual(括号已配对("1+\\n"), False)
        self.assertEqual(括号已配对("if\n"), False)
        self.assertEqual(括号已配对("elif\n"), False)
        self.assertEqual(括号已配对("else\n"), False)
        self.assertEqual(括号已配对("for\n"), False)
        self.assertEqual(括号已配对("func\n"), False)
        self.assertEqual(括号已配对("func a\n"), False)
        self.assertEqual(括号已配对("func a(\n"), False)
        self.assertEqual(括号已配对("func a()\n"), False)
        self.assertEqual(括号已配对("func a() {\n"), False)
        self.assertEqual(括号已配对("loop\n"), False)
        self.assertEqual(括号已配对("operator\n"), False)
        self.assertEqual(括号已配对("type\n"), False)
        self.assertEqual(括号已配对("while\n"), False)

if __name__ == '__main__':
    unittest.main()