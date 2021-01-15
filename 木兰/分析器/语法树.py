import ast

from rply.token import SourcePosition
from rply import Token

from 木兰.分析器.语法成分 import *

class 语法树:

    源码 = []

    @staticmethod
    def 新节点(类型, 主体=None, 忽略类型=None, 值=None, 左=None, 运算符=None, 右=None, 标识=None,
            上下文=None, 函数=None, 参数=None, 关键词=None, 变量=None, 条件=None, 否则=None,
            前项=None, 后项=None, 标注=None, 名称=None, 返回=None, 各基准类=None, 片段=None):
        if 类型 == 语法.模块:
            节点 = ast.Module(body=主体, type_ignores=忽略类型)
        elif 类型 == 语法.表达式:
            节点 = ast.Expr(value=值)
        elif 类型 == 语法.数:
            节点 = ast.Num(n=值)
        elif 类型 == 语法.二元表达式:
            if isinstance(运算符, ast.And) or isinstance(运算符, ast.Or):
                节点 = ast.BoolOp(op=运算符, values=[前项, 后项])
            elif isinstance(运算符, ast.Add) or isinstance(运算符, ast.Sub) or isinstance(运算符, ast.Mult) or isinstance(运算符, ast.Pow) or isinstance(运算符, ast.Mod):
                节点 = ast.BinOp(left=左, op=运算符, right=右)
            else:
                # TODO: 为何比较符和后项在数组中?
                节点 = ast.Compare(前项, [运算符], [后项])
        elif 类型 == 语法.名称:
            节点 = ast.Name(id=标识, ctx=上下文)
        elif 类型 == 语法.调用:
            节点 = ast.Call(func=函数, args=参数, keywords=关键词)
        elif 类型 == 语法.赋值:
            节点 = ast.Assign([变量], 值)
        elif 类型 == 语法.增量赋值:
            节点 = ast.AugAssign(变量, 运算符, 值)
        elif 类型 == 语法.条件声明:
            节点 = ast.If(test=条件, body=主体, orelse=否则)
        elif 类型 == 语法.每当声明:
            节点 = ast.While(test=条件, body=主体, orelse=[])
        elif 类型 == 语法.终止声明:
            节点 = ast.Break()
        elif 类型 == 语法.跳过声明:
            节点 = ast.Continue()
        elif 类型 == 语法.操作数:
            节点 = ast.arg(arg=参数)
        elif 类型 == 语法.lambda形参 or 类型 == 语法.形参:
            节点 = ast.arg(arg=参数, annotation=标注)
        elif 类型 == 语法.形参列表:
            节点 = ast.arguments(args=参数, kwonlyargs=[], kw_defaults=[], defaults=[], vararg=None, kwarg=None)
        elif 类型 == 语法.函数:
            节点 = ast.FunctionDef(
                    name=名称,
                    args=参数,
                    body=主体,
                    decorator_list=[])
            if 返回:
                节点.returns = 返回
        elif 类型 == 语法.返回声明:
            节点 = ast.Return(value=值)
        elif 类型 == 语法.引用声明:
            节点 = ast.Import(names=名称)
        elif 类型 == 语法.lambda表达式:
            节点 = ast.Lambda(args=参数, body=主体)
        elif 类型 == 语法.类型定义:
            节点 = ast.ClassDef(name=名称,
                            bases=各基准类,
                            keywords=[],
                            body=主体,
                            decorator_list=[])
        elif 类型 == 语法.字符串:
            节点 = ast.Str(值)
        elif 类型 == 语法.外部声明:
            节点 = ast.Global(names=名称)
        elif 类型 == 语法.一元表达式:
            节点 = ast.UnaryOp(op=运算符, operand=值)

        if 片段:
            节点.lineno = 语法树.取行号(片段)
            节点.col_offset = 语法树.取列号(片段)
        return 节点

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
    def 常量(值, 片段):
        return ast.NameConstant(value=值, lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

    @staticmethod
    def 空转(片段):
        return ast.Pass(lineno=语法树.取行号(片段), col_offset=语法树.取列号(片段))

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
    def 片(下限, 上限, 片段):
        return ast.Slice(lower=下限,
                        upper=上限,
                        step=None,
                        lineno=语法树.取行号(片段),
                        col_offset=语法树.取列号(片段))
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
    def 顺便处理项(上下文表达式, 可选变量, 片段):
        return ast.withitem(context_expr=上下文表达式,
            optional_vars=可选变量,
            lineno=语法树.取行号(片段),
            col_offset=语法树.取列号(片段))

    @staticmethod
    def 顺便(各项, 主体, 片段):
        return ast.With(items=各项,
            body=主体,
            lineno=语法树.取行号(片段),
            col_offset=语法树.取列号(片段))

    @staticmethod
    def 试试(主体, 处理, 片段):
        return ast.Try(body=主体,
                       handlers=处理,
                       orelse=[],
                       finalbody=[],
                       lineno=语法树.取行号(片段),
                       col_offset=语法树.取列号(片段))

    @staticmethod
    def 例外处理(类型, 名称, 主体, 片段):
        return ast.ExceptHandler(type=类型,
                                 name=名称,
                                 body=主体,
                                 lineno=语法树.取行号(片段),
                                 col_offset=语法树.取列号(片段))
    @staticmethod
    def 引发(例外, 片段):
        return ast.Raise(exc=例外,
            cause=None,
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
            if 片段.gettokentype() == '$end':
                return 语法树.取末位()
            return 片段.getsourcepos()
        # Constant 也是 ast.expr
        if isinstance(片段, ast.stmt) or isinstance(片段, ast.expr):
            # TODO: 之前没 import SourcePosition 时, 编译/运行未报错! 需解决
            return SourcePosition(0, 片段.lineno, 片段.col_offset)
        return SourcePosition(0, 0, 0)

    def 取末位():
        idx = -1
        行号 = len(语法树.源码)
        列号 = len(语法树.源码[(-1)])
        return SourcePosition(idx, 行号, 列号)

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
