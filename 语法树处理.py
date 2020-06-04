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
        self.cls = ['']

    def visit_FunctionDef(self, func):
        if func.name.startswith('$'):
            pass
        elif self.cls[(-1)]:
            if not func.args.args or func.args.args[0].arg != 'self':
                decorator = ast.Name(id='staticmethod',
                  ctx=(ast.Load()),
                  lineno=(func.lineno),
                  col_offset=(func.col_offset))
                func.decorator_list.append(decorator)
        self.cls.append(None)
        func = self.generic_visit(func)
        self.cls.pop(-1)
        return func

    def visit_ClassDef(self, cls):
        self.cls.append(cls.name)
        cls = self.generic_visit(cls)
        self.cls.pop(-1)
        return cls
