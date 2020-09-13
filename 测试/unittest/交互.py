import unittest
from 交互 import 括号已配对

class test交互(unittest.TestCase):

    def test_括号已配对(self):
        self.assertEqual(括号已配对("a=3\n"), True)
        self.assertEqual(括号已配对("func a() {}\n"), True)
        self.assertEqual(括号已配对("func a()\n"), False)
        self.assertEqual(括号已配对("func a\n"), False)
        self.assertEqual(括号已配对("func a(\n"), False)
        self.assertEqual(括号已配对("func a() {\n"), False)

if __name__ == '__main__':
    unittest.main()