import ast
import unittest
import warnings

from 木兰.生成.codegen import to_source


class CodegenTest(unittest.TestCase):

    def test_constant_nodes_do_not_use_deprecated_visitors(self):
        module = ast.parse("x = 1\ny = 'hi'\nz = None\nb = b'hi'\n")

        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            source = to_source(module)

        self.assertEqual(source, "x = 1\ny = 'hi'\nz = None\nb = b'hi'")


if __name__ == "__main__":
    unittest.main()
