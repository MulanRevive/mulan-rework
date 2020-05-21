import ast
from rply import ParserGenerator
from 语法树 import *

from 词法分析器 import 规则

class 语法分析器:

    分析器母机 = ParserGenerator(
        规则,
        precedence=[
            ('left', ['连词_或']),
            ('left', ['连词_且']),
            # nonassoc 参考: http://www.dabeaz.com/ply/ply.html
            # non-associativity in the precedence table. This would be used when you don't want operations to chain together
            ('nonassoc', ['>', '<', '>=', '<=', '!==', '===']),
            ('left', ['!=', '==']),
            ('left', ['加', '減']),
            ('left', ['乘', '除']),
        ]
    )

    # ast 参考: https://docs.python.org/3.7/library/ast.html#abstract-grammar

    @分析器母机.production('模块 : 声明列表')
    def 模块(片段):
        return 语法树.模块(主体=片段[0], 忽略类型=[])

    @分析器母机.production('块 : 前括号 声明列表 后括号')
    def 块(片段):
        #print('块')
        return 片段[1]

    @分析器母机.production('声明列表 : 声明')
    @分析器母机.production('声明列表 : 声明列表 换行 声明')
    def 声明列表(片段):
        #print('声明列表')
        if len(片段) == 1:
            return [片段[0]]
        片段[0].append(片段[(-1)])
        return 片段[0]

    @分析器母机.production('声明 : 函数')
    @分析器母机.production('声明 : 条件声明')
    @分析器母机.production('声明 : 每当声明')
    def 混合声明(片段):
        return 片段[0]

    @分析器母机.production('声明 : 表达式声明')
    @分析器母机.production('声明 : 赋值')
    @分析器母机.production('声明 : 终止声明')
    @分析器母机.production('声明 : 跳过声明')
    @分析器母机.production('声明 : 返回声明')
    def 声明(片段):
        return 片段[0]

    @分析器母机.production('表达式声明 : 表达式前缀')
    def 表达式声明(片段):
        #print("表达式声明")
        return 语法树.表达式(值 = 片段[0], 片段 = 片段)

    # TODO: 支持多元赋值, 如: a, b, c = 1, 2, 3
    @分析器母机.production('赋值 : 表达式前缀 = 表达式')
    def 赋值(片段):
        #print("赋值")
        片段[0].ctx = ast.Store()
        return 语法树.赋值(
            变量 = 片段[0],
            值 = 片段[2],
            片段 = 片段)

    # TODO: 返回(多个)值
    @分析器母机.production('返回声明 : 动词_返回')
    def ret_stmt(片段):
        值 = None
        return 语法树.返回(
            值=值,
            片段=片段)

    @分析器母机.production('终止声明 : 终止')
    def 终止声明(片段):
        return 语法树.终止(片段 = 片段)

    @分析器母机.production('跳过声明 : 跳过')
    def 跳过声明(片段):
        return 语法树.跳过(片段 = 片段)

    @分析器母机.production('二元表达式 : 表达式 加 表达式')
    @分析器母机.production('二元表达式 : 表达式 減 表达式')
    @分析器母机.production('二元表达式 : 表达式 乘 表达式')
    def 二元表达式(片段):
        左 = 片段[0]
        右 = 片段[2]
        运算符 = 片段[1].getstr()
        对照表 = {
            '+': ast.Add(),
            '-': ast.Sub(),
            '*': ast.Mult()
        }
        if 运算符 in 对照表:
            python运算 = 对照表[运算符]
        else:
            breakpoint()
        return 语法树.二元运算(左, python运算, 右, 片段)

    @分析器母机.production('二元表达式 : 表达式 除 表达式')
    def 除法(片段):
        return 语法树.调用(
            函数=语法树.名称(
                标识='__div__',
                上下文=(ast.Load()),
                片段=片段),
            参数=[片段[0], 片段[2]],
            片段=片段)

    @分析器母机.production('二元表达式 : 表达式 > 表达式')
    @分析器母机.production('二元表达式 : 表达式 >= 表达式')
    @分析器母机.production('二元表达式 : 表达式 < 表达式')
    @分析器母机.production('二元表达式 : 表达式 <= 表达式')
    @分析器母机.production('二元表达式 : 表达式 == 表达式')
    @分析器母机.production('二元表达式 : 表达式 != 表达式')
    @分析器母机.production('二元表达式 : 表达式 === 表达式')
    @分析器母机.production('二元表达式 : 表达式 !== 表达式')
    def 比较(片段):
        对照表 = {
            '>': ast.Gt(),
            '>=': ast.GtE(),
            '<': ast.Lt(),
            '<=': ast.LtE(),
            '==': ast.Eq(),
            '!=': ast.NotEq(),
            '===': ast.Is(),
            '!==': ast.IsNot()
            }
        return 语法树.比较(
            前项 = 片段[0],
            操作符 = 对照表[片段[1].getstr()],
            后项 = 片段[2],
            片段=片段)

    @分析器母机.production('二元表达式 : 表达式 连词_且 表达式')
    @分析器母机.production('二元表达式 : 表达式 连词_或 表达式')
    def 布尔表达式(片段):
        return 语法树.布尔操作(
            操作符=(ast.And() if 片段[1].getstr() == 'and' else ast.Or()),
            前项 = 片段[0],
            后项 = 片段[2],
            片段=片段)

    @分析器母机.production('表达式前缀 : 变量')
    @分析器母机.production('表达式前缀 : 调用')
    def 表达式前缀(片段):
        #print("表达式前缀")
        return 片段[0]

    @分析器母机.production('变量 : 名称')
    def 变量(片段):
        return 片段[0]

    @分析器母机.production('实参部分 : ( 各实参 )')
    @分析器母机.production('实参部分 : ( )')
    def 实参部分(片段):
        if len(片段) != 3:
            return []
        return 片段[1]

    @分析器母机.production('调用 : 变量 实参部分')
    def 调用(片段):
        各参数 = []
        for 值, 键 in 片段[1]:
            if 键 is None:
                各参数.append(值)

        return 语法树.调用(
                片段[0],
                参数=各参数,
                片段=片段)

    @分析器母机.production('数 : 整数')
    @分析器母机.production('数 : 小数')
    def 数(片段):
        try:
            return 语法树.数(int(片段[0].getstr(), 0), 片段)
        except ValueError:
            return 语法树.数(float(片段[0].getstr()), 片段)

    @分析器母机.production('表达式 : 二元表达式')
    @分析器母机.production('表达式 : 表达式前缀')
    @分析器母机.production('表达式 : 数') # TODO: 为何要, precedence='==' ?
    def 表达式(片段):
        return 片段[0]

    @分析器母机.production('各实参 : 实参')
    @分析器母机.production('各实参 : 各实参 , 实参')
    def 各实参(片段):
        if len(片段) == 3:
            片段[0].append(片段[2])
            return 片段[0]
        return [片段[0]]

    @分析器母机.production('实参 : 表达式')
    def 实参(片段):
        return (片段[0], None)

    @分析器母机.production('形参列表 : ')
    @分析器母机.production('形参列表 : 非空形参列表')
    def 形参列表(片段=[]):
        if not 片段:
            return 语法树.各形参([])
        # TODO: 如支持形参默认值, 需要 legalize_arguments
        return 片段[0]

    @分析器母机.production('非空形参列表 : 形参')
    @分析器母机.production('非空形参列表 : 非空形参列表 , 形参')
    def 非空形参列表(片段):
        if len(片段) == 1:
            各形参 = 语法分析器.形参列表()
        else:
            各形参 = 片段[0]
        各形参.args.append(片段[-1])
        return 各形参

    @分析器母机.production('形参 : 名称')
    def param(片段):
        return 语法树.形参(
            名称=片段[0].id,
            标注=(None if len(片段) == 1 else 片段[-1]),
            片段=片段)

    @分析器母机.production('函数 : 名词_函数 标识符 ( 形参列表 ) 块')
    @分析器母机.production('函数 : 名词_函数 标识符 块')
    def 函数(片段):
        return 语法树.函数定义(
            名称=(片段[1].getstr()),
            形参列表=(片段[3] if len(片段) == 6 else 语法分析器.形参列表()),
            主体=片段[-1],
            片段=片段)

    @分析器母机.production('条件声明 : 连词_如果 表达式 块 否则如果声明')
    @分析器母机.production('条件声明 : 连词_如果 表达式 块 连词_否则 块')
    @分析器母机.production('否则如果声明 : ')
    @分析器母机.production('否则如果声明 : 连词_否则如果 表达式 块 否则如果声明')
    @分析器母机.production('否则如果声明 : 连词_否则如果 表达式 块 连词_否则 块')
    def 条件声明(片段):
        if len(片段) == 0:
            return []
        否则部分 = 片段[-1]
        return 语法树.如果(
            条件=片段[1],
            主体=片段[2],
            否则=否则部分 if isinstance(否则部分, list) else [否则部分],
            片段=片段)

    @分析器母机.production('条件声明 : 声明 连词_如果 表达式')
    def 条件倒置声明(片段):
        return 语法树.如果(
            条件=片段[-1],
            主体=[片段[0]],
            否则=[],
            片段=片段)

    @分析器母机.production('声明 : 块')
    def 单块(片段):
        return 语法树.如果(
            条件=语法树.常数(True, 片段),
            主体=片段[0],
            否则=[],
            片段=片段)

    @分析器母机.production('每当声明 : 连词_每当 表达式 块')
    def 每当(片段):
        return 语法树.每当(
            条件=片段[1],
            主体=片段[2],
            片段=片段)

    @分析器母机.production('名称 : 标识符')
    def 标识符(片段):
        标识 = 片段[0].getstr()
        return 语法树.名称(
            标识=标识,
            上下文=(ast.Load()),
            片段=片段)

    分析器 = 分析器母机.build()

    def 创建(self):
        return self.分析器
