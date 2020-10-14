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
            if 函数.name == self.类[(-1)]:
                函数.name = '__init__'
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

class AnnoFuncInsertPass(ast.NodeTransformer):
    """
    Visit all ast to insert each anonymous function
    just before where it has been referenced.
    """

    def __init__(self, 匿名函数):
        self.匿名函数 = 匿名函数

    def generic_visit(self, 节点):
        for 域, 旧值 in ast.iter_fields(节点):
            if isinstance(旧值, list) and len(旧值) > 0:
                if isinstance(旧值[0], ast.stmt):
                    旧值[:] = self.visit_stmts(旧值)
                    continue
                各新值 = []
                for 值 in 旧值:
                    if isinstance(值, ast.AST):
                        值 = self.visit(值)
                        if 值 is None:
                            continue
                        elif not isinstance(值, ast.AST):
                            各新值.extend(值)
                            continue
                    各新值.append(值)

                旧值[:] = 各新值
            elif isinstance(旧值, ast.AST):
                新值 = self.visit(旧值)
                if 新值 is None:
                    delattr(节点, 域)
                else:
                    setattr(节点, 域, 新值)

        return 节点

    def visit_stmts(self, 声明列表):
        新声明列表 = []
        for 声明 in 声明列表:
            声明 = self.visit(声明)
            for 节点 in ast.walk(声明):
                if isinstance(节点, ast.Name) and 节点 in self.匿名函数:
                    新声明列表.append(self.匿名函数[节点])
                    del self.匿名函数[节点]

            新声明列表.append(声明)

        return 新声明列表