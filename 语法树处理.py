import ast


class NameFixPass(ast.NodeTransformer):
    # 只看到如下区别, class 定义中此属性非空: decorator_list=[Name(id='staticmethod', ctx=Load(), lineno=2, col_offset=5)],
    """
    A python NodeVisitor which traverses the generated ast
    to fix the signature of class methods by adding the
    implicit argument 'self' and also convert the function
    name of the class constructors..
    """

    def __init__(self, filename):
        self.filename = filename
        self.类 = ['']

    def visit_FunctionDef(self, 函数):
        if 函数.name.startswith('$'):
            函数.name = 函数.name.replace('$', '')
            函数.args.args.insert(0, ast.arg(arg='self',
                                             annotation=None,
                                             lineno=(函数.lineno),
                                             col_offset=(函数.col_offset)))
        elif self.类[(-1)]:
            if not 函数.args.args or 函数.args.args[0].arg != 'self':
                decorator = ast.Name(id='staticmethod',
                                     ctx=(ast.Load()),
                                     lineno=(函数.lineno),
                                     col_offset=(函数.col_offset))
                函数.decorator_list.append(decorator)
        self.类.append(None)
        函数 = self.generic_visit(函数)
        self.类.pop(-1)
        return 函数

    def visit_ClassDef(self, 类):
        self.类.append(类.name)
        类 = self.generic_visit(类)
        self.类.pop(-1)
        return 类
