import ast
from rply import ParserGenerator
from 语法树 import *
from 错误 import 语法错误

from 词法分析器 import 规则

class 语法分析器:

    # TODO: 改进可视化 parse 过程(各个语法规则的顺序), 方便调试
    调试 = False

    分析器母机 = ParserGenerator(
        规则,
        precedence=[
            ('right', ['?', ':']),
            ('left', ['连词_或']),
            ('left', ['连词_且']),
            # nonassoc 参考: http://www.dabeaz.com/ply/ply.html
            # non-associativity in the precedence table. This would be used when you don't want operations to chain together
            ('nonassoc', ['>', '<', '>=', '<=', '!==', '===']),
            ('left', ['!=', '==']),
            ('left', ['加', '減']),
            ('left', ['星号', '除']),
            ('left', ['非']),
        ]
    )

    # ast 参考: https://docs.python.org/3.7/library/ast.html#abstract-grammar

    @分析器母机.production('模块 : 注水声明列表')
    def 模块(片段):
        return 语法树.模块(主体=片段[0], 忽略类型=[])

    @分析器母机.production('块 : 前括号 注水声明列表 后括号')
    def 块(片段):
        if 语法分析器.调试:
            print('块')
        if len(片段) == 3:
            if 片段[1]:
                return 片段[1]
        return [语法树.空转(片段)]

    # TODO: 分号
    @分析器母机.production('注水声明列表 : ')
    @分析器母机.production('注水声明列表 : 声明列表')
    @分析器母机.production('注水声明列表 : 声明列表 换行')
    def 注水声明列表(片段):
        if 语法分析器.调试:
            print('注水声明列表')
        if len(片段) > 0:
            return 片段[0]
        return []

    # TODO： 分号
    @分析器母机.production('声明列表 : 声明')
    @分析器母机.production('声明列表 : 声明列表 换行 声明')
    def 声明列表(片段):
        if 语法分析器.调试:
            print('声明列表')
        if len(片段) == 1:
            return [片段[0]]
        片段[0].append(片段[(-1)])
        return 片段[0]

    @分析器母机.production('声明 : 类型定义')
    @分析器母机.production('声明 : 函数')
    @分析器母机.production('声明 : 条件声明')
    @分析器母机.production('声明 : 每当声明')
    @分析器母机.production('声明 : 外部声明')
    def 混合声明(片段):
        if 语法分析器.调试:
            print('混合声明')
        return 片段[0]

    @分析器母机.production('类型定义 : 名词_类型 名称 各基准类 类型主体')
    def 类型定义(片段):
        return 语法树.类定义(
            名称=片段[1].id,
            各基准类=片段[2],
            主体=片段[-1],
            片段=片段)

    @分析器母机.production('各基准类 :')
    @分析器母机.production('各基准类 : : 表达式前缀')
    def 各基准类(片段):
        if 语法分析器.调试:
            print('各基准类')
        if len(片段) == 0:
            return []
        return [片段[1]]

    @分析器母机.production('类型主体 : 前括号 各类型内声明 后括号')
    def 类型主体(片段):
        if 语法分析器.调试:
            print('类型主体')
        return 片段[1]

    @分析器母机.production('各类型内声明 : ')
    @分析器母机.production('各类型内声明 : 各类型内声明 类型内声明')
    def 各类型内声明(片段):
        if 语法分析器.调试:
            print('各类型内声明')
        if len(片段) == 0:
            # TODO: 应该报语法错误?
            return []
        if isinstance(片段[1], list): # TODO: 有这种情况吗?
            片段[0] += 片段[1]
        else:
            片段[0].append(片段[1])
        return 片段[0]

    @分析器母机.production('类型内声明 : 块')
    @分析器母机.production('类型内声明 : 操作符')
    @分析器母机.production('类型内声明 : 函数')
    def 类型内声明(片段):
        if 语法分析器.调试:
            print('类型内声明')
        return 片段[0]

    @分析器母机.production('操作符 : 名词_操作符 二元操作符 操作数 块')
    def 操作符(片段):
        return 语法树.函数定义(名称=片段[1],
                        形参列表=片段[2],
                        主体=片段[-1],
                        片段=片段)

    @分析器母机.production('操作数 : ( 形参 )')
    def 操作数(片段):
        各形参 = 语法分析器.形参列表()
        各形参.args.append(语法树.形参(名称='self',
                               标注=None,
                               片段=片段))
        [各形参.args.append(形参) for 形参 in 片段 if isinstance(形参, ast.arg)]
        return 各形参

    @分析器母机.production('二元操作符 : 加')
    @分析器母机.production('二元操作符 : 減')
    def 二元操作符(片段):
        对照表 = {
            '+': '__add__',
            '-': '__sub__',
        }
        return 对照表[片段[0].getstr()]

    @分析器母机.production('声明 : 引用声明')
    @分析器母机.production('声明 : 表达式声明')
    @分析器母机.production('声明 : 赋值')
    @分析器母机.production('声明 : 终止声明')
    @分析器母机.production('声明 : 跳过声明')
    @分析器母机.production('声明 : 返回声明')
    def 声明(片段):
        return 片段[0]

    # TODO: try-catch-throw

    # TODO: 更多引用方式

    @分析器母机.production('模块位置 : 模块名')
    @分析器母机.production('模块位置 : 点')
    def 模块位置(片段):
        return 片段[0]

    @分析器母机.production('引用声明 : 动词_引用 各模块名 连词_于 模块位置')
    @分析器母机.production('引用声明 : 动词_引用 星号 连词_于 模块位置')
    def 引用于(片段):
        模块, 层 = 片段[-1], 0
        if isinstance(片段[-1], Token):
            模块 = None
            层 = 1 if 片段[-1].getstr() == '.' else 2
        节点 = 语法树.从模块导入(
            模块=模块,
            各名称=[],
            位置=层,
            片段=片段)
        if isinstance(片段[1], list):
            节点.names += 片段[1]
        else:
            节点.names.append(
                语法树.别名(名称='*',
                        别名=None,
                        片段=片段[1]))
        return 节点

    @分析器母机.production('引用声明 : 动词_引用 各模块名')
    def 引用声明(片段):
        return 语法树.导入(
            名称=片段[1],
            片段=片段)

    @分析器母机.production('各模块名 : 模块名')
    @分析器母机.production('各模块名 : 各模块名 , 模块名')
    def 各模块名(片段):
        别名 = 语法树.别名(
            名称=片段[-1],
            别名=None,
            片段=片段[-1]
        )
        if len(片段) == 1:
            return [别名]
        片段[0].append(别名)
        return 片段[0]

    @分析器母机.production('模块名 : 模块名 点 名称')
    @分析器母机.production('模块名 : 名称')
    def 模块名(片段):
        if len(片段) == 1:
            return 片段[0].id
        return '%s.%s' % (片段[0], 片段[2].id)

    @分析器母机.production('表达式声明 : 表达式前缀')
    def 表达式声明(片段):
        if 语法分析器.调试:
            print("表达式声明")
        return 语法树.表达式(值 = 片段[0], 片段 = 片段)

    # TODO: 返回(多个)值
    @分析器母机.production('返回声明 : 动词_返回')
    @分析器母机.production('返回声明 : 动词_返回 表达式')
    def 返回(片段):
        值 = None
        if len(片段) == 2:
            值 = 片段[1]
        return 语法树.返回(
            值=值,
            片段=片段)

    # TODO: 支持多元赋值, 如: a, b, c = 1, 2, 3
    @分析器母机.production('赋值 : 表达式前缀 = 表达式')
    def 赋值(片段):
        if 语法分析器.调试:
            print("赋值")
        片段[0].ctx = ast.Store()
        return 语法树.赋值(
            变量 = 片段[0],
            值 = 片段[2],
            片段 = 片段)

    @分析器母机.production('外部声明 : 形容词_外部 各名称')
    def 外部声明(片段):
        return 语法树.全局([名称.id for 名称 in 片段[1]], 片段=片段)

    @分析器母机.production('终止声明 : 动词_终止')
    def 终止声明(片段):
        return 语法树.终止(片段 = 片段)

    @分析器母机.production('跳过声明 : 动词_跳过')
    def 跳过声明(片段):
        return 语法树.跳过(片段 = 片段)

    @分析器母机.production('二元表达式 : 表达式 加 表达式')
    @分析器母机.production('二元表达式 : 表达式 減 表达式')
    @分析器母机.production('二元表达式 : 表达式 星号 表达式')
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

    # TODO: ~ -
    @分析器母机.production('一元表达式 : 非 表达式')
    def 一元表达式(片段):
        操作符 = 片段[0].getstr()
        if 操作符 == '!':
            操作符 = ast.Not()
        return 语法树.一元操作(操作符, 片段[1], 片段=片段)

    @分析器母机.production('三元表达式 : 表达式 ? 表达式 : 表达式')
    def 三元表达式(片段):
        return 语法树.如果表达式(
            条件=片段[0],
            主体=片段[2],
            否则=片段[-1],
            片段=片段)

    @分析器母机.production('表达式前缀 : 变量')
    @分析器母机.production('表达式前缀 : 调用')
    def 表达式前缀(片段):
        if 语法分析器.调试:
            print("表达式前缀")
        return 片段[0]

    # TODO: 添加测试: 调用().名称
    @分析器母机.production('变量 : 表达式前缀 点 名称')
    def 属性表达式(片段):
        return 语法树.属性(
            值=片段[0],
            属性=片段[2].id,
            片段=片段)

    @分析器母机.production('变量 : 名称')
    def 变量(片段):
        return 片段[0]

    @分析器母机.production('实参部分 : ( 各实参 )')
    @分析器母机.production('实参部分 : ( )')
    def 实参部分(片段):
        if 语法分析器.调试:
            print("实参部分")
        if len(片段) != 3:
            return []
        return 片段[1]

    # 变量->表达式前缀, 以支持高阶函数调用, 如 f(1)(2)
    @分析器母机.production('调用 : 表达式前缀 实参部分')
    def 调用(片段):
        if 语法分析器.调试:
            print("调用")
        各参数 = []
        for 值, 键 in 片段[1]:
            if 键 is None:
                #print(值)
                各参数.append(值)

        return 语法树.调用(
                片段[0],
                参数=各参数,
                片段=片段)

    # TODO: SUPER

    @分析器母机.production('数 : 整数')
    @分析器母机.production('数 : 小数')
    def 数(片段):
        try:
            return 语法树.数(int(片段[0].getstr(), 0), 片段)
        except ValueError:
            return 语法树.数(float(片段[0].getstr()), 片段)

    @分析器母机.production('常量 : 名词_真')
    def 常量_真(片段):
        return 语法树.常量(True, 片段=片段)

    @分析器母机.production('常量 : 名词_假')
    def 常量_假(片段):
        return 语法树.常量(False, 片段=片段)

    @分析器母机.production('常量 : 名词_空')
    def 常量_空(片段):
        return 语法树.常量(None, 片段=片段)

    @分析器母机.production('表达式 : 二元表达式')
    @分析器母机.production('表达式 : 一元表达式')
    @分析器母机.production('表达式 : 表达式前缀')
    @分析器母机.production('表达式 : 三元表达式')
    @分析器母机.production('表达式 : 数') # TODO: 为何要, precedence='==' ?
    @分析器母机.production('表达式 : 常量')
    def 表达式(片段):
        if 语法分析器.调试:
            print("表达式")
        return 片段[0]

    @分析器母机.production('各名称 : 名称')
    @分析器母机.production('各名称 : 各名称 , 名称')
    @分析器母机.production('各实参 : 实参')
    @分析器母机.production('各实参 : 各实参 , 实参')
    def 各实参(片段):
        if 语法分析器.调试:
            print("各实参")
        if len(片段) == 3:
            片段[0].append(片段[2])
            return 片段[0]
        return [片段[0]]

    @分析器母机.production('实参 : 表达式')
    def 实参(片段):
        if 语法分析器.调试:
            print("实参")
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
    def 形参(片段):
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

    @分析器母机.error
    def error_handler(词):
        # TODO: 最好取到语法信息(上下文)
        raise 语法错误(
            信息=('没认出这个词 "%s"' % 词.gettokentype()),
            文件名=语法分析器.文件名,
            行号=语法树.取行号(词),
            列号=语法树.取列号(词),
            源码=语法分析器.源码)

    分析器 = 分析器母机.build()

    def 创建(self, 源码, 源码文件):
        语法分析器.源码 = 源码.split("\n")
        语法分析器.文件名 = 源码文件
        return self.分析器
