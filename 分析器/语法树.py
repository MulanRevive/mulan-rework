import ast

from rply.token import SourcePosition
from rply import Token


class 语法树:
    @staticmethod
    def 模块(主体, 忽略类型):
        return ast.Module(body=主体, type_ignores=忽略类型)

    @staticmethod
    def 表达式(值, 片段):
        return ast.Expr(value=值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 数(值, 片段):
        return ast.Num(值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 二元运算(左, 运算符, 右, 片段):
        return ast.BinOp(左, 运算符, 右, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 名称(标识, 上下文, 片段):
        return ast.Name(id=标识, ctx=上下文, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 调用(函数, 参数, 关键字, 片段):
        return ast.Call(func=函数, args=参数, keywords=关键字, starargs=None, kwargs=None,
                        lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 赋值(变量, 值, 片段):
        return ast.Assign([变量], 值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 增量赋值(变量, 运算符, 值, 片段):
        return ast.AugAssign(变量, 运算符, 值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 如果(条件, 主体, 否则, 片段):
        return ast.If(test=条件, body=主体, orelse=否则, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    # TODO: 为何比较符和后项在数组中?
    @staticmethod
    def 比较(前项, 操作符, 后项, 片段):
        return ast.Compare(前项, [操作符], [后项], lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 布尔操作(前项, 操作符, 后项, 片段):
        return ast.BoolOp(op=操作符, values=[前项, 后项], lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 每当(条件, 主体, 片段):
        return ast.While(test=条件, body=主体, orelse=[], lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 终止(片段):
        return ast.Break(lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 跳过(片段):
        return ast.Continue(lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 无标注形参(名称, 片段):
        return ast.arg(arg=名称, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 形参(名称, 标注, 片段):
        return ast.arg(arg=名称, annotation=标注, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 各形参(各参数, 片段=None):
        if not 片段:
            return ast.arguments(args=各参数, kwonlyargs=[], kw_defaults=[], defaults=[], vararg=None, kwarg=None)
        return ast.arguments(args=各参数, kwonlyargs=[], kw_defaults=[], defaults=[], vararg=None, kwarg=None,
            lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 无返回函数定义(名称, 形参列表, 主体, 片段):
        return ast.FunctionDef(
            name=名称,
            args=形参列表,
            body=主体,
            decorator_list=[],
            lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 函数定义(名称, 形参列表, 主体, 返回, 片段):
        return ast.FunctionDef(
            name=名称,
            args=形参列表,
            body=主体,
            decorator_list=[],
            returns=返回,
            lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 返回(值, 片段):
        return ast.Return(value=值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 导入(名称, 片段):
        return ast.Import(names=名称, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 别名(名称, 别名, 片段):
        return ast.alias(name=名称, asname=别名, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 属性(值, 属性, 片段):
        return ast.Attribute(value=值, attr=属性, ctx=(ast.Load()), lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 从模块导入(模块, 各名称, 位置, 片段):
        return ast.ImportFrom(module=模块, names=各名称, level=位置, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 一元操作(操作符, 值, 片段):
        return ast.UnaryOp(操作符, 值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 常量(值, 片段):
        return ast.NameConstant(value=值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 类定义(名称, 各基准类, 主体, 片段):
        return ast.ClassDef(name=名称,
                            bases=各基准类,
                            keywords=[],
                            body=主体,
                            decorator_list=[],
                            starargs=None,
                            kwargs=None,
                            lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 空转(片段):
        return ast.Pass(lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 全局(各名称, 片段):
        return ast.Global(各名称, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 字符串(值, 片段):
        return ast.Str(值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 对于(目标, 遍历范围, 主体, 片段):
        return ast.For(target=目标, iter=遍历范围, body=主体, orelse=[],
                       lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 列表(元素, 片段):
        return ast.List(elts=元素, ctx=ast.Load(), lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 索引(值, 片段):
        return ast.Index(value=值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 下标(全值, 片, 片段):
        return ast.Subscript(value=全值,
                             slice=片,
                             ctx=(ast.Load()),
                             lineno=语法树.取行号(片段),
                             col_offset=语法树.取列号(片段))

    @staticmethod
    def 多项(元素, 上下文, 片段):
        return ast.Tuple(elts=元素,
                         ctx=上下文,
                         lineno=语法树.取行号(片段),
                         col_offset=语法树.取列号(片段))

    @staticmethod
    def 字典(各键, 各值, 片段):
        return ast.Dict(keys=各键,
            values=各值,
            lineno=语法树.取行号(片段),
            col_offset=语法树.取列号(片段))

    @staticmethod
    def Lambda(参数, 主体, 片段):
        return ast.Lambda(args=参数,
            body=主体,
            lineno=语法树.取行号(片段),
            col_offset=语法树.取列号(片段))

    # 表达式部分

    @staticmethod
    def 如果表达式(条件, 主体, 否则, 片段):
        return ast.IfExp(test=条件, body=主体, orelse=否则, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

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
