import ast

from rply.token import SourcePosition
from rply import Token

class 语法树:
    @staticmethod
    def 模块(主体, 忽略类型):
        return ast.Module(body = 主体, type_ignores = 忽略类型)

    @staticmethod
    def 表达式(值, 片段):
        return ast.Expr(value = 值, lineno = 语法树.取行号(片段), col_offset = 语法树.取列号(片段))

    @staticmethod
    def 数(值, 片段):
        return ast.Num(值, lineno = 语法树.取行号(片段), col_offset = 语法树.取列号(片段))

    @staticmethod
    def 二元运算(左, 运算符, 右, 片段):
        return ast.BinOp(左, 运算符, 右, lineno = 语法树.取行号(片段), col_offset = 语法树.取列号(片段))

    @staticmethod
    def 名称(标识, 上下文, 片段):
        return ast.Name(id=标识, ctx=上下文, lineno = 语法树.取行号(片段), col_offset = 语法树.取列号(片段))

    @staticmethod
    def 调用(函数, 参数, 片段):
        return ast.Call(func=函数, args=参数, keywords=[], starargs=None, kwargs=None,
            lineno = 语法树.取行号(片段), col_offset = 语法树.取列号(片段))

    @staticmethod
    def 赋值(变量, 值, 片段):
        return ast.Assign([变量], 值, lineno = 语法树.取行号(片段), col_offset = 语法树.取列号(片段))

    @staticmethod
    def 常数(值, 片段):
        return ast.NameConstant(value=值, lineno = 语法树.取行号(片段), col_offset = 语法树.取列号(片段))

    @staticmethod
    def 如果(条件, 主体, 否则, 片段):
        return ast.If(test=条件, body=主体, orelse=否则, lineno = 语法树.取行号(片段), col_offset = 语法树.取列号(片段))

    '''
    不同于 python3 的语法树中, col_offset 是从 0 开始:
    >>> ast.dump(ast.parse("2+3"), True, True)
    'Module(body=[Expr(value=BinOp(left=Num(n=2, lineno=1, col_offset=0), op=Add(), right=Num(n=3, lineno=1, col_offset=2), lineno=1, col_offset=0), lineno=1, col_offset=0)])'
    '''
    def 取源码位置(片段):
        if isinstance(片段, list):
            if len(片段) > 0:
                片段 = 片段[0]
        if isinstance(片段, Token):
            return 片段.getsourcepos()
        # Constant 也是 ast.expr
        if isinstance(片段, ast.stmt) or isinstance(片段, ast.expr):
            # TODO: 之前没 import SourcePosition 时, 编译/运行未报错! 需解决
            return SourcePosition(0, 片段.lineno, 片段.col_offset)
        return SourcePosition(0, 0, 0)

    def 取行号(片段):
        try:
            return 语法树.取源码位置(片段).lineno
        except:
            return 0

    def 取列号(片段):
        try:
            return 语法树.取源码位置(片段).colno
        except:
            return 0
