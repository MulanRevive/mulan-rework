from enum import Enum, unique
from rply import ParserGenerator
from rply.errors import LexingError
from 木兰.分析器.rply_parser import LRParser
from 木兰.分析器.语法树 import *
from 木兰.分析器.错误 import 语法错误, 词法错误

from 木兰.分析器.词法分析器 import *
from 木兰.分析器.语法树处理 import *
from 木兰.分析器.语法成分 import *

from 木兰.功用.常用 import *

"""
LR(1) 将木兰源码分析后生成 Python 语法树
"""
class 语法分析器:

    # TODO: 改进可视化 parse 过程(各个语法规则的顺序), 方便调试
    调试 = False

    分析器母机 = ParserGenerator(
        规则,
        precedence=[
            ('nonassoc', [名词_超类]),
            ('right', [箭头]),
            ('right', [问号, 冒号]),
            ('left', [连词_或]),
            ('left', [连词_且]),
            # nonassoc 参考: http://www.dabeaz.com/ply/ply.html
            # non-associativity in the precedence table. This would be used when you don't want operations to chain together
            ('nonassoc', [大于, 小于, 大于等于, 小于等于, 严格不等于, 严格等于]),
            ('left', [不等于, 等于]),
            ('nonassoc', [连词_每隔]),
            ('nonassoc', [点点, 点点小于]),
            ('left', [加, 减]),
            ('left', [星号, 除, 求余]),
            ('left', [非]),
            ('right', [乘方]),

            # 原来在 点点 和 加减之间，不知为何。既然测试能过，先放在最高，以观后效。
            ('nonassoc', [前小括号]),
        ]
    )

    # ast 参考: https://docs.python.org/3.7/library/ast.html#abstract-grammar

    @分析器母机.production(语法.模块.成分(语法.注水声明列表))
    def 模块(self, 片段):
        return 语法树.新节点(语法.模块, 主体=片段[0], 忽略类型=[])

    @分析器母机.production(语法.块.成分(分号))
    @分析器母机.production(语法.块.成分(前大括号, 语法.注水声明列表, 后大括号))
    def 块(self, 片段):
        if 语法分析器.调试:
            print('块')
        if len(片段) == 3:
            if 片段[1]:
                return 片段[1]
        return [语法树.空转(片段)]

    @分析器母机.production(语法.注水声明列表.成分())
    @分析器母机.production(语法.注水声明列表.成分(语法.声明列表))
    @分析器母机.production(语法.注水声明列表.成分(语法.声明列表, 换行))
    @分析器母机.production(语法.注水声明列表.成分(语法.声明列表, 分号))
    def 注水声明列表(self, 片段):
        if 语法分析器.调试:
            print('注水声明列表')
        if len(片段) > 0:
            return 片段[0]
        return []

    @分析器母机.production(语法.声明列表.成分(语法.声明))
    @分析器母机.production(语法.声明列表.成分(语法.声明列表, 换行, 语法.声明))
    @分析器母机.production(语法.声明列表.成分(语法.声明列表, 分号, 语法.声明))
    def 声明列表(self, 片段):
        if 语法分析器.调试:
            print('声明列表')
        if len(片段) == 1:
            return [片段[0]]
        片段[0].append(片段[(-1)])
        return 片段[0]

    @分析器母机.production(语法.声明.成分(语法.类型定义))
    @分析器母机.production(语法.声明.成分(语法.函数))
    @分析器母机.production(语法.声明.成分(语法.条件声明))
    @分析器母机.production(语法.声明.成分(语法.每当声明))
    @分析器母机.production(语法.声明.成分(语法.对于声明))
    @分析器母机.production(语法.声明.成分(语法.外部声明))
    def 混合声明(self, 片段):
        if 语法分析器.调试:
            print('混合声明')
        return 片段[0]

    @分析器母机.production(语法.类型定义.成分(名词_类型, 语法.名称, 语法.各基准类, 语法.类型主体))
    def 类型定义(self, 片段):
        return 语法树.新节点(语法.类型定义,
            名称=片段[1].id,
            各基准类=片段[2],
            主体=片段[-1],
            片段=片段)

    @分析器母机.production(语法.各基准类.成分())
    @分析器母机.production(语法.各基准类.成分(冒号, 语法.表达式前缀))
    @分析器母机.production(语法.各基准类.成分(冒号, 语法.各表达式前缀))
    def 各基准类(self, 片段):
        if 语法分析器.调试:
            print('各基准类')
        if len(片段) == 0:
            return []
        if isinstance(片段[1], list):
            return 片段[1]
        return [片段[1]]

    @分析器母机.production(语法.类型主体.成分(前大括号, 语法.各类型内声明, 后大括号))
    def 类型主体(self, 片段):
        if 语法分析器.调试:
            print('类型主体')
        return 片段[1]

    @分析器母机.production(语法.各类型内声明.成分())
    @分析器母机.production(语法.各类型内声明.成分(语法.各类型内声明, 语法.类型内声明))
    def 各类型内声明(self, 片段):
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

    @分析器母机.production(语法.类型内声明.成分(语法.块))
    @分析器母机.production(语法.类型内声明.成分(语法.操作符))
    @分析器母机.production(语法.类型内声明.成分(语法.函数))
    @分析器母机.production(语法.类型内声明.成分(语法.应变属性))
    def 类型内声明(self, 片段):
        if 语法分析器.调试:
            print('类型内声明')
        return 片段[0]

    @分析器母机.production(语法.应变属性.成分(名词_应变属性, 标识符, 语法.块))
    @分析器母机.production(语法.应变属性.成分(名词_应变属性, 标识符, 前小括号, 后小括号, 语法.块))
    @分析器母机.production(语法.应变属性.成分(名词_应变属性, 标识符, 符号_赋值, 前小括号, 语法.形参, 后小括号, 语法.块))
    def 应变属性(self, 片段):
        名称 = 片段[1].getstr()
        函数 = 语法树.新节点(语法.函数, 名称=名称,
                        参数=self.形参列表(),
                        主体=片段[-1],
                        片段=片段)
        if len(片段) == 7:
            函数.args.args.append(片段[4])
            函数.decorator_list.append(
                语法树.属性(
                    值=语法树.新节点(语法.名称,
                        标识=名称.replace('$', ''),
                        上下文=ast.Load(),
                        片段=片段),
                    属性='setter',
                    片段=片段))
        else:
            函数.decorator_list.append(
                语法树.新节点(语法.名称,
                    标识='property',
                    上下文=ast.Load(),
                    片段=片段))
        return 函数

    @分析器母机.production(语法.操作符.成分(名词_操作符, 语法.二元操作符, 语法.操作数, 语法.块))
    def 操作符(self, 片段):
        return 语法树.新节点(语法.函数, 名称=片段[1],
                        参数=片段[2],
                        主体=片段[-1],
                        片段=片段)

    @分析器母机.production(语法.操作数.成分(前小括号, 语法.形参, 后小括号))
    def 操作数(self, 片段):
        各形参 = self.形参列表()
        各形参.args.append(语法树.新节点(语法.操作数, 参数='self',
                               片段=片段))
        [各形参.args.append(形参) for 形参 in 片段 if isinstance(形参, ast.arg)]
        return 各形参

    @分析器母机.production(语法.二元操作符.成分(加))
    @分析器母机.production(语法.二元操作符.成分(减))
    @分析器母机.production(语法.二元操作符.成分(等于))
    def 二元操作符(self, 片段):
        对照表 = {
            加: '__add__',
            减: '__sub__',
            等于: '__eq__',
        }
        return 对照表[片段[0].getstr()]

    @分析器母机.production(语法.声明.成分(语法.引用声明))
    @分析器母机.production(语法.声明.成分(语法.表达式声明))
    @分析器母机.production(语法.声明.成分(语法.赋值))
    @分析器母机.production(语法.声明.成分(语法.增量赋值))
    @分析器母机.production(语法.声明.成分(语法.终止声明))
    @分析器母机.production(语法.声明.成分(语法.跳过声明))
    @分析器母机.production(语法.声明.成分(语法.试试声明))
    @分析器母机.production(语法.声明.成分(语法.抛出声明))
    @分析器母机.production(语法.声明.成分(语法.返回声明))
    def 声明(self, 片段):
        return 片段[0]

    # TODO: 补完 try-catch-throw

    @分析器母机.production(语法.抛出声明.成分(动词_抛出, 语法.表达式))
    def 抛出声明(self, 片段):
        return 语法树.引发(片段[1], 片段)

    @分析器母机.production(语法.顺便处理.成分(语法.表达式前缀, 符号_赋值, 语法.表达式))
    @分析器母机.production(语法.顺便处理.成分(语法.表达式))
    def 顺便处理(self, 片段):
        处理项 = 语法树.顺便处理项(上下文表达式=片段[(-1)], 可选变量=None, 片段=片段)
        if len(片段) == 3:
            片段[0].ctx = ast.Store()
            处理项.optional_vars = 片段[0]
        return 处理项

    @分析器母机.production(语法.试试声明.成分(动词_试试, 语法.顺便处理, 语法.块))
    def 试试声明_顺便处理(self, 片段):
        return 语法树.顺便(各项=[片段[1]], 主体=片段[2], 片段=片段)

    @分析器母机.production(语法.试试声明.成分(动词_试试, 语法.块, 语法.各接手声明))
    def 试试声明(self, 片段):
        return 语法树.试试(主体=(片段[1]),
                      处理=片段[-1],
                      片段=片段)

    @分析器母机.production(语法.各接手声明.成分(语法.各接手声明, 语法.接手声明))
    @分析器母机.production(语法.各接手声明.成分(语法.接手声明))
    def 各接手声明(self, 片段):
        if len(片段) == 1:
            return [片段[0]]
        片段[0].append(片段[1])
        return 片段[0]

    @分析器母机.production(语法.接手声明.成分(动词_接手, 语法.名称, 冒号, 语法.表达式, 语法.块))
    @分析器母机.production(语法.接手声明.成分(动词_接手, 语法.名称, 语法.块))
    def 接手声明(self, 片段):
        名称, 类型 = (None, None)
        if len(片段) == 3:
            名称 = 片段[1].id
        elif len(片段) == 5:
            名称 = 片段[1].id
            类型 = 片段[3]
        return 语法树.例外处理(类型=类型,
                        名称=名称,
                        主体=片段[-1],
                        片段=片段)

    # TODO: 更多引用方式

    @分析器母机.production(语法.模块位置.成分(语法.模块名))
    @分析器母机.production(语法.模块位置.成分(点))
    def 模块位置(self, 片段):
        return 片段[0]

    @分析器母机.production(语法.引用声明.成分(动词_引用, 语法.各模块名, 连词_于, 语法.模块位置))
    @分析器母机.production(语法.引用声明.成分(动词_引用, 星号, 连词_于, 语法.模块位置))
    def 引用于(self, 片段):
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
                语法树.别名(名称=星号,
                        别名=None,
                        片段=片段[1]))
        return 节点

    @分析器母机.production(语法.引用声明.成分(动词_引用, 语法.各模块名))
    def 引用声明(self, 片段):
        return 语法树.新节点(语法.引用声明,
            名称=片段[1],
            片段=片段)

    @分析器母机.production(语法.各模块名.成分(语法.模块名))
    @分析器母机.production(语法.各模块名.成分(语法.各模块名, 逗号, 语法.模块名))
    def 各模块名(self, 片段):
        别名 = 语法树.别名(
            名称=片段[-1],
            别名=None,
            片段=片段[-1]
        )
        if len(片段) == 1:
            return [别名]
        片段[0].append(别名)
        return 片段[0]

    @分析器母机.production(语法.模块名.成分(语法.模块名, 点, 语法.名称))
    @分析器母机.production(语法.模块名.成分(语法.名称))
    def 模块名(self, 片段):
        if len(片段) == 1:
            return 片段[0].id
        return '%s.%s' % (片段[0], 片段[2].id)

    @分析器母机.production(语法.表达式声明.成分(语法.表达式前缀))
    def 表达式声明(self, 片段):
        if 语法分析器.调试:
            print("表达式声明")
        if not isinstance(片段[0], ast.Call):
            # TODO：下面两个似乎不需要
            # if not isinstance(片段[0], ast.Yield):
                #if not isinstance(片段[0], ast.Str):
                    片段[0] = 语法树.新节点(语法.调用, 函数=片段[0],
                      参数=[],
                      关键词=[],
                      片段=片段)
        return 语法树.新节点(语法.表达式, 值 = 片段[0], 片段 = 片段)

    @分析器母机.production(语法.返回声明.成分(动词_返回))
    @分析器母机.production(语法.返回声明.成分(动词_返回, 语法.各表达式))
    def 返回(self, 片段):
        值 = None
        if len(片段) == 2:
            if len(片段[1]) == 1:
                值 = 片段[1][0]
            else:
                值 = 语法树.多项(元素=片段[1],
                           上下文=ast.Load(),
                           片段=片段[1])
        return 语法树.新节点(语法.返回声明,
            值=值,
            片段=片段)

    @分析器母机.production(语法.增量赋值.成分(语法.表达式前缀, 增量赋值, 语法.表达式))
    @分析器母机.production(语法.增量赋值.成分(语法.表达式前缀, 减量赋值, 语法.表达式))
    def 增量赋值(self, 片段):
        运算符 = 片段[1].getstr()
        对照表 = {
            增量赋值: ast.Add(),
            减量赋值: ast.Sub(),
        }
        if 运算符 in 对照表:
            python运算 = 对照表[运算符]

        # 否则报错：
        # ValueError: expression must have Store context but has Load instead
        片段[0].ctx = ast.Store()

        return 语法树.新节点(语法.增量赋值, 变量=片段[0], 运算符=python运算, 值=片段[2], 片段=片段)

    @分析器母机.production(语法.赋值.成分(语法.表达式前缀, 符号_赋值, 语法.表达式))
    def 赋值(self, 片段):
        if 语法分析器.调试:
            print("赋值")
        片段[0].ctx = ast.Store()
        return 语法树.新节点(语法.赋值,
            变量 = 片段[0],
            值 = 片段[2],
            片段 = 片段)

    @分析器母机.production(语法.外部声明.成分(形容词_外部, 语法.各名称))
    def 外部声明(self, 片段):
        return 语法树.新节点(语法.外部声明, 名称=[名称.id for 名称 in 片段[1]], 片段=片段)

    @分析器母机.production(语法.各表达式前缀.成分(语法.各表达式前缀, 逗号, 语法.表达式前缀))
    @分析器母机.production(语法.各表达式前缀.成分(语法.表达式前缀, 逗号, 语法.表达式前缀))
    def 各表达式前缀(self, 片段):
        if isinstance(片段[0], list):
            片段[0].append(片段[2])
            return 片段[0]
        return [片段[0], 片段[2]]

    @分析器母机.production(语法.赋值.成分(语法.各表达式前缀, 符号_赋值, 语法.各表达式))
    def 多项赋值(self, 片段):
        for 表达式前缀 in 片段[0]:
            表达式前缀.ctx = ast.Store()

        左边 = 语法树.多项(
            元素=片段[0],
            上下文=ast.Store(),
            片段=片段)
        if len(片段[2]) > 1:
            右边 = 语法树.多项(
                元素=片段[2],
                上下文=ast.Load(),
                片段=片段[2])
        else:
            右边 = 片段[2][0]
        return 语法树.新节点(语法.赋值,
            变量=左边,
            值=右边,
            片段=片段)

    @分析器母机.production(语法.终止声明.成分(动词_终止))
    def 终止声明(self, 片段):
        return 语法树.新节点(语法.终止声明, 片段 = 片段)

    @分析器母机.production(语法.跳过声明.成分(动词_跳过))
    def 跳过声明(self, 片段):
        return 语法树.新节点(语法.跳过声明, 片段 = 片段)

    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 加, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 减, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 星号, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 乘方, 语法.表达式))
    def 二元表达式(self, 片段):
        左 = 片段[0]
        右 = 片段[2]
        运算符 = 片段[1].getstr()
        对照表 = {
            加: ast.Add(),
            减: ast.Sub(),
            星号: ast.Mult(),
            乘方: ast.Pow()
        }
        if 运算符 in 对照表:
            python运算 = 对照表[运算符]
        else:
            breakpoint()
        return 语法树.新节点(语法.二元表达式, 左=左, 运算符=python运算, 右=右, 片段=片段)

    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 除, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 求余, 语法.表达式))
    def 除法(self, 片段):
        操作符 = '__div__' if 片段[1].getstr() == '/' else '__rem__'
        return 语法树.新节点(语法.调用,
            函数=语法树.新节点(语法.名称,
                标识=操作符,
                上下文=(ast.Load()),
                片段=片段),
            参数=[片段[0], 片段[2]],
            关键词=[],
            片段=片段)

    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 大于, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 大于等于, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 小于, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 小于等于, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 等于, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 不等于, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 严格等于, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 严格不等于, 语法.表达式))
    def 比较(self, 片段):
        对照表 = {
            大于: ast.Gt(),
            大于等于: ast.GtE(),
            小于: ast.Lt(),
            小于等于: ast.LtE(),
            等于: ast.Eq(),
            不等于: ast.NotEq(),
            严格等于: ast.Is(),
            严格不等于: ast.IsNot()
            }
        return 语法树.新节点(语法.二元表达式,
            前项 = 片段[0],
            运算符 = 对照表[片段[1].getstr()],
            后项 = 片段[2],
            片段=片段)

    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 连词_且, 语法.表达式))
    @分析器母机.production(语法.二元表达式.成分(语法.表达式, 连词_或, 语法.表达式))
    def 布尔表达式(self, 片段):
        return 语法树.新节点(语法.二元表达式,
            运算符=(ast.And() if 片段[1].getstr() == 连词_且 else ast.Or()),
            前项 = 片段[0],
            后项 = 片段[2],
            片段=片段)

    @分析器母机.production(语法.范围表达式.成分(语法.表达式, 点点, 语法.表达式))
    @分析器母机.production(语法.范围表达式.成分(语法.表达式, 点点小于, 语法.表达式))
    @分析器母机.production(语法.范围表达式.成分(语法.范围表达式, 连词_每隔, 语法.表达式))
    def 范围表达式(self, 片段):
        连词 = 片段[1].getstr()
        if 连词 != 连词_每隔:
            起 = 片段[0]
            止 = 片段[2]
            if 连词 == 点点:
                止 = 语法树.新节点(语法.二元表达式, 左=止,
                            运算符=ast.Add(),
                            右=语法树.新节点(语法.数, 值=1, 片段=止),
                            片段=止)
                止.fixed = True
            return 语法树.新节点(语法.调用,
                函数=语法树.新节点(语法.名称, 标识='range',
                          上下文=ast.Load(),
                          片段=片段),
                参数=[起, 止],
                关键词=[],
                片段=片段)
        assert isinstance(片段[0], ast.Call)    # 第三个格式
        参数 = 片段[0].args

        # 不允许多个 by 串联
        if len(参数) == 3:
            raise 语法错误(
                信息=('没认出这个词 "%s"' % 片段[1].getstr()),
                文件名=self.文件名,
                行号=语法树.取行号(片段[1]),
                列号=语法树.取列号(片段[1]),
                源码=self.源码)
        参数.append(片段[2])
        止 = 参数[1]
        if hasattr(止, 'fixed'):
            if isinstance(片段[2], ast.Num):
                if 片段[2].n < 0:
                    止.op = ast.Sub()
            else:
                为正 = 语法树.新节点(语法.二元表达式,
                        前项=片段[2],
                        运算符=ast.Gt(),
                        后项=语法树.新节点(语法.数, 值=0, 片段=片段[2]),
                        片段=片段[2])
                增量 = 语法树.如果表达式(
                    条件=为正,
                    主体=止.right,
                    否则=语法树.新节点(语法.数, 值=-1, 片段=片段[2]),
                    片段=片段)
                止.right = 增量
            delattr(止, 'fixed')
        return 片段[0]

    # TODO: #
    @分析器母机.production(语法.一元表达式.成分(减, 语法.表达式))
    @分析器母机.production(语法.一元表达式.成分(非, 语法.表达式))
    @分析器母机.production(语法.一元表达式.成分(取反, 语法.表达式), precedence=非)
    def 一元表达式(self, 片段):
        操作符 = 片段[0].getstr()
        对照表 = {
            减: ast.USub(),
            非: ast.Not(),
            取反: ast.Invert(),
        }
        return 语法树.新节点(语法.一元表达式, 运算符=对照表[操作符], 值=片段[1], 片段=片段)

    @分析器母机.production(语法.三元表达式.成分(语法.表达式, 问号, 语法.表达式, 冒号, 语法.表达式))
    def 三元表达式(self, 片段):
        return 语法树.如果表达式(
            条件=片段[0],
            主体=片段[2],
            否则=片段[-1],
            片段=片段)

    @分析器母机.production(语法.首要表达式.成分(前小括号, 语法.表达式, 后小括号))
    def 首要表达式(self, 片段):
        return 片段[1]

    @分析器母机.production(语法.表达式前缀.成分(语法.调用))
    @分析器母机.production(语法.表达式前缀.成分(语法.变量))
    @分析器母机.production(语法.表达式前缀.成分(语法.匿名函数))
    @分析器母机.production(语法.表达式前缀.成分(语法.字符串))
    @分析器母机.production(语法.表达式前缀.成分(语法.列表表达式))
    @分析器母机.production(语法.表达式前缀.成分(语法.字典表达式))
    def 表达式前缀(self, 片段):
        if 语法分析器.调试:
            print("表达式前缀")
        return 片段[0]

    @分析器母机.production(语法.片.成分(语法.表达式))
    def 索引(self, 片段):
        return 语法树.索引(值=片段[0], 片段=片段)

    @分析器母机.production(语法.片.成分(语法.表达式, 冒号, 语法.表达式))
    @分析器母机.production(语法.片.成分(语法.表达式, 冒号))
    @分析器母机.production(语法.片.成分(冒号, 语法.表达式))
    @分析器母机.production(语法.片.成分(冒号))
    def 片表示(self, 片段):
        下限, 上限 = 片段[0], 片段[-1]
        if isinstance(下限, Token):
            下限 = None
        if isinstance(上限, Token):
            上限 = None
        return 语法树.片(下限, 上限, 片段)

    @分析器母机.production(语法.变量.成分(语法.表达式前缀, 前中括号, 语法.片, 后中括号))
    def 片表达式(self, 片段):
        return 语法树.下标(片段[0], 片段[2], 片段)

    @分析器母机.production(语法.变量.成分(语法.表达式前缀, 点, 语法.名称))
    def 属性表达式(self, 片段):
        return 语法树.属性(
            值=片段[0],
            属性=片段[2].id,
            片段=片段)

    @分析器母机.production(语法.变量.成分(语法.名称))
    def 变量(self, 片段):
        return 片段[0]

    @分析器母机.production(语法.实参部分.成分(前小括号, 语法.各实参, 后小括号))
    @分析器母机.production(语法.实参部分.成分(前小括号, 后小括号))
    def 实参部分(self, 片段):
        if 语法分析器.调试:
            print("实参部分")
        if len(片段) != 3:
            return []
        return 片段[1]

    # 变量->表达式前缀, 以支持高阶函数调用, 如 f(1)(2)
    @分析器母机.production(语法.调用.成分(语法.表达式前缀, 语法.实参部分))
    def 调用(self, 片段):
        if 语法分析器.调试:
            print("调用")
        各参数 = []
        关键词 = []
        for 值, 键 in 片段[1]:
            if 键 is None:
                各参数.append(值)
            else:
                关键词.append(ast.keyword(arg=键,value=值))

        return 语法树.新节点(语法.调用,
                函数=片段[0],
                参数=各参数,
                关键词=关键词,
                片段=片段)

    # TODO: 补全 SUPER
    @分析器母机.production(语法.调用.成分(语法.超类))
    def 调用超类(self, 片段):
        return 片段[0]

    @分析器母机.production(语法.超类.成分(名词_超类, 语法.实参部分))
    @分析器母机.production(语法.超类.成分(名词_超类))
    def 超类(self, 片段):
        超类节点 = [语法树.新节点(语法.名称, 标识='super',
            上下文=ast.Load(),
            片段=片段)]
        if len(片段) == 2:
            超类节点.append(片段[1] if len(片段[1]) > 0 else [(None, None)])
        else:
            超类节点.append([])
        return self.调用(超类节点)

    @分析器母机.production(语法.lambda形参.成分(语法.名称))
    def lambda形参(self, 片段):
        if isinstance(片段[0], ast.Name):
            args = 语法树.新节点(语法.形参列表, 参数=[],
                片段=片段)
            arg = 语法树.新节点(语法.lambda形参, 参数=片段[0].id,
                标注=None,
                片段=片段)
            args.args = [arg]
            return args

        # TODO：添加测试
        raise SyntaxError(message='expect an identifier here',
            filename=(self.文件名),
            lineno=(self.getlineno(片段)),
            colno=(self.getcolno(片段)),
            source=(self.源码))

    @分析器母机.production(语法.lambda主体.成分(箭头, 语法.表达式))
    @分析器母机.production(语法.lambda主体.成分(箭头, 语法.块))
    def lambda主体(self, 片段):
        return 片段[1]

    @分析器母机.production(语法.lambda表达式.成分(语法.lambda形参, 语法.lambda主体))
    def lambda表达式(self, 片段):
        #if len(p) == 1:
        #    return p[0]
        if isinstance(片段[-1], ast.expr):
            return 语法树.新节点(语法.lambda表达式, 参数=片段[0],
              主体=片段[-1],
              片段=片段)
        return self.创建匿名函数(片段, 片段[0], 片段[-1])

    @分析器母机.production(语法.匿名函数.成分(名词_函数, 前小括号, 语法.形参列表, 后小括号, 语法.块))
    @分析器母机.production(语法.匿名函数.成分(名词_函数, 语法.块))
    def lambda_func(self, 片段):
        形参 = 片段[2] if len(片段) == 5 else [] # lambda_无参.ul 测试错误。如果改为`self.形参列表()`则输出 4
        return self.创建匿名函数(片段, 形参, 片段[-1])

    @分析器母机.production(语法.匿名函数.成分(名词_函数, 前小括号, 语法.形参列表, 后小括号, 冒号, 语法.类型名称, 语法.块))
    def 指定类型匿名函数(self, 片段):
        形参, 主体, 返回 = 片段[2], 片段[-1], 片段[-2]
        return self.创建匿名函数(片段, 形参, 主体, 返回)

    @分析器母机.production(语法.类型名称.成分(语法.名称))
    def 类型名称(self, 片段):
        return 片段[0]

    def 创建匿名函数(self, 片段, 形参, 主体, 返回=None):
        函数名 = 语法树.新节点(语法.名称, 标识=随机文本(),
            上下文=ast.Load(),
            片段=片段)
        函数 = 语法树.新节点(语法.函数, 名称=函数名.id,
                        参数=形参,
                        主体=主体,
                        返回=返回,
                        片段=片段)
        self.匿名函数[函数名] = 函数
        return 函数名

    @分析器母机.production(语法.数.成分(整数))
    @分析器母机.production(语法.数.成分(小数))
    def 数(self, 片段):
        try:
            return 语法树.新节点(语法.数, 值=int(片段[0].getstr(), 0), 片段=片段)
        except ValueError:
            return 语法树.新节点(语法.数, 值=float(片段[0].getstr()), 片段=片段)

    @分析器母机.production(语法.字符串.成分(双引号字符串))
    @分析器母机.production(语法.字符串.成分(单引号字符串))
    def 字符串(self, 片段):
        值 = 片段[0].getstr()

        # TODO: 其他转义字符，如 () 等等
        值 = 值.replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\\', '\\')
        if 值.startswith('"'):
            值 = 值.replace(r'\"', '"')
        else:
            值 = 值.replace(r"\'", "'")
        值 = 值[1:-1]
        插值后 = self.执行插值(值, 片段)
        if 插值后 is not None:
            return 插值后
        return 语法树.新节点(语法.字符串, 值=值, 片段=片段)

    def 执行插值(self, 原始字符串, 片段):
        import re
        模式 = re.compile(r'\\\(([^\\\)]*)\\\)|`([^`]*)`')
        占位替代 = 原始字符串
        所有插值 = []
        位置 = 0
        while True:
            匹配 = 模式.search(string=原始字符串, pos=位置)
            if 匹配 is None:
                break
            位置 = 匹配.span()[1]
            表达式 = 匹配.group(1)
            if 表达式 is None:
                表达式 = 匹配.group(2)
            替代文本 = 语法分析器().分析('str(%s)' % 表达式)
            所有插值.append(替代文本.body[0].value)
            占位替代 = 占位替代.replace(匹配.group(0), '%s')

        if len(所有插值) == 0:
            return
        return 语法树.新节点(语法.二元表达式,
            左=语法树.新节点(语法.字符串, 值=占位替代, 片段=片段),
            运算符=ast.Mod(),
            右=语法树.多项(元素=所有插值, 上下文=ast.Load(), 片段=片段),
            片段=片段)

    @分析器母机.production(语法.常量.成分(名词_真))
    def 常量_真(self, 片段):
        return 语法树.常量(True, 片段=片段)

    @分析器母机.production(语法.常量.成分(名词_假))
    def 常量_假(self, 片段):
        return 语法树.常量(False, 片段=片段)

    @分析器母机.production(语法.常量.成分(名词_空))
    def 常量_空(self, 片段):
        return 语法树.常量(None, 片段=片段)

    @分析器母机.production(语法.常量.成分(名词_自身))
    def 常量_自身(self, 片段):
        return 语法树.新节点(语法.名称, 标识='self',
            上下文=ast.Load(),
            片段=片段)

    @分析器母机.production(语法.表达式.成分(语法.多项式乘法))
    @分析器母机.production(语法.表达式.成分(语法.二元表达式))
    @分析器母机.production(语法.表达式.成分(语法.一元表达式))
    @分析器母机.production(语法.表达式.成分(语法.表达式前缀))
    @分析器母机.production(语法.表达式.成分(语法.首要表达式))
    @分析器母机.production(语法.表达式.成分(语法.lambda表达式))
    @分析器母机.production(语法.表达式.成分(语法.三元表达式))
    @分析器母机.production(语法.表达式.成分(语法.数), precedence=等于)
    @分析器母机.production(语法.表达式.成分(语法.常量))

    # TODO 待参透：等于 的优先级在 连词_每隔 下一位
    @分析器母机.production(语法.表达式.成分(语法.范围表达式), precedence=等于)
    def 表达式(self, 片段):
        if 语法分析器.调试:
            print("表达式")
        return 片段[0]

    @分析器母机.production(语法.多项式乘法.成分(语法.数, 语法.表达式前缀))
    @分析器母机.production(语法.多项式乘法.成分(语法.数, 语法.首要表达式))
    def 多项式乘法(self, 片段):
        片段[1] = self.转换为多项(片段[1])
        return 语法树.新节点(语法.二元表达式,
            左=片段[0],
            运算符=ast.Mult(),
            右=片段[1],
            片段=片段)

    @分析器母机.production(语法.字典表达式.成分(前大括号, 冒号, 后大括号))
    @分析器母机.production(语法.字典表达式.成分(前大括号, 语法.各键值对, 后大括号))
    def 字典表达式(self, 片段):
        各键 = []
        各值 = []
        if isinstance(片段[1], list):
            各键 = [对[0] for 对 in 片段[1]]
            各值 = [对[1] for 对 in 片段[1]]
        return 语法树.字典(各键=各键,
            各值=各值,
            片段=片段)

    @分析器母机.production(语法.各键值对.成分(语法.键值对))
    @分析器母机.production(语法.各键值对.成分(语法.各键值对, 逗号, 语法.键值对))
    def 各键值对(self, 片段):
        if len(片段) < 3:
            return [片段[0]]
        片段[0].append(片段[-1])
        return 片段[0]

    @分析器母机.production(语法.键值对.成分(语法.表达式, 冒号, 语法.表达式))
    def 键值对(self, 片段):
        return (片段[-3], 片段[-1])

    @分析器母机.production(语法.列表表达式.成分(前中括号, 后中括号))
    @分析器母机.production(语法.列表表达式.成分(前中括号, 语法.各表达式, 后中括号))
    def 列表表达式(self, 片段):
        元素 = 片段[1] if len(片段) == 3 else []
        return 语法树.列表(元素, 片段=片段)

    @分析器母机.production(语法.各名称.成分(语法.名称))
    @分析器母机.production(语法.各名称.成分(语法.各名称, 逗号, 语法.名称))
    @分析器母机.production(语法.各实参.成分(语法.实参))
    @分析器母机.production(语法.各实参.成分(语法.各实参, 逗号, 语法.实参))
    @分析器母机.production(语法.各表达式.成分(语法.表达式))
    @分析器母机.production(语法.各表达式.成分(语法.各表达式, 逗号, 语法.表达式))
    def 各实参(self, 片段):
        if 语法分析器.调试:
            print("各实参")
        if len(片段) == 3:
            片段[0].append(片段[2])
            return 片段[0]
        return [片段[0]]

    @分析器母机.production(语法.实参.成分(语法.表达式))
    @分析器母机.production(语法.实参.成分(标识符, 符号_赋值, 语法.表达式))
    def 实参(self, 片段):
        if 语法分析器.调试:
            print("实参")
        if len(片段) == 1:
            return (片段[0], None)
        return (片段[-1], 片段[0].getstr())

    @分析器母机.production(语法.形参列表.成分())
    @分析器母机.production(语法.形参列表.成分(语法.非空形参列表))
    def 形参列表(self, 片段=[]):
        if not 片段:
            return 语法树.新节点(语法.形参列表, 参数=[])
        return self.形参合法化(片段[0])

    @分析器母机.production(语法.非空形参列表.成分(语法.形参))
    @分析器母机.production(语法.非空形参列表.成分(语法.非空形参列表, 逗号, 语法.形参))
    def 非空形参列表(self, 片段):
        if len(片段) == 1:
            各形参 = self.形参列表()
        else:
            各形参 = 片段[0]
        各形参.args.append(片段[-1])
        return 各形参

    @分析器母机.production(语法.形参.成分(语法.名称, 冒号, 语法.类型名称))
    @分析器母机.production(语法.形参.成分(语法.名称))
    def 形参(self, 片段):
        return 语法树.新节点(语法.形参,
            参数=片段[0].id,
            标注=(None if len(片段) == 1 else 片段[-1]),
            片段=片段)

    @分析器母机.production(语法.形参.成分(语法.名称, 符号_赋值, 语法.表达式))
    def 带默认值形参(self, 片段):
        参数 = self.形参(片段[:1])
        参数.default = 片段[2]
        return 参数

    @分析器母机.production(语法.函数.成分(名词_函数, 标识符, 前小括号, 语法.形参列表, 后小括号, 语法.块))
    @分析器母机.production(语法.函数.成分(名词_函数, 标识符, 语法.块))
    def 函数(self, 片段):
        return 语法树.新节点(语法.函数,
            名称=(片段[1].getstr()),
            参数=(片段[3] if len(片段) == 6 else self.形参列表()),
            主体=片段[-1],
            片段=片段)

    @分析器母机.production(语法.函数.成分(名词_函数, 标识符, 前小括号, 语法.形参列表, 后小括号, 冒号, 语法.类型名称, 语法.块))
    @分析器母机.production(语法.函数.成分(名词_函数, 标识符, 冒号, 语法.类型名称, 语法.块))
    def 函数(self, 片段):
        return 语法树.新节点(语法.函数,
            名称=(片段[1].getstr()),
            参数=(片段[3] if len(片段) == 8 else self.形参列表()),
            主体=片段[-1],
            返回=片段[-2],
            片段=片段)

    @分析器母机.production(语法.条件声明.成分(连词_如果, 语法.表达式, 语法.块, 语法.否则如果声明))
    @分析器母机.production(语法.条件声明.成分(连词_如果, 语法.表达式, 语法.块, 连词_否则, 语法.块))
    @分析器母机.production(语法.否则如果声明.成分())
    @分析器母机.production(语法.否则如果声明.成分(连词_否则如果, 语法.表达式, 语法.块, 语法.否则如果声明))
    @分析器母机.production(语法.否则如果声明.成分(连词_否则如果, 语法.表达式, 语法.块, 连词_否则, 语法.块))
    def 条件声明(self, 片段):
        if len(片段) == 0:
            return []
        否则部分 = 片段[-1]
        return 语法树.新节点(语法.条件声明,
            条件=片段[1],
            主体=片段[2],
            否则=否则部分 if isinstance(否则部分, list) else [否则部分],
            片段=片段)

    @分析器母机.production(语法.条件声明.成分(语法.声明, 连词_如果, 语法.表达式))
    def 条件倒置声明(self, 片段):
        return 语法树.新节点(语法.条件声明,
            条件=片段[-1],
            主体=[片段[0]],
            否则=[],
            片段=片段)

    @分析器母机.production(语法.声明.成分(语法.块))
    def 单块(self, 片段):
        return 语法树.新节点(语法.条件声明,
            条件=语法树.常量(True, 片段),
            主体=片段[0],
            否则=[],
            片段=片段)

    @分析器母机.production(语法.每当声明.成分(连词_每当, 语法.表达式, 语法.块))
    def 每当(self, 片段):
        return 语法树.新节点(语法.每当声明,
            条件=片段[1],
            主体=片段[2],
            片段=片段)

    @分析器母机.production(语法.每当声明.成分(动词_循环, 语法.块))
    def 无条件每当(self, 片段):
        return 语法树.新节点(语法.每当声明,
            条件=语法树.常量(True, 片段),
            主体=片段[1],
            片段=片段)

    @分析器母机.production(语法.迭代器.成分(语法.表达式前缀))
    @分析器母机.production(语法.迭代器.成分(语法.各表达式前缀))
    def 迭代器(self, 片段):
        return 片段[0]

    @分析器母机.production(语法.遍历范围.成分(语法.表达式))
    def 遍历范围(self, 片段):
        # TODO: 处理 ast.Starred
        return 片段[0]

    @分析器母机.production(语法.对于声明.成分(连词_对, 语法.迭代器, 连词_于, 语法.遍历范围, 语法.块))
    @分析器母机.production(语法.对于声明.成分(连词_对, 语法.迭代器, 冒号, 语法.遍历范围, 语法.块))
    def 对于声明(self, 片段):
        目标 = 片段[1]
        if isinstance(目标, list):
            for 项 in 目标:
                if hasattr(项, 'ctx'):
                    项.ctx = ast.Store()

            目标 = 语法树.多项(元素=目标,
               上下文=ast.Store(),
               片段=片段)
        else:
            目标.ctx = ast.Store()
        return 语法树.对于(目标=目标,
                      遍历范围=片段[3],
                      主体=片段[4],
                      片段=片段)

    @分析器母机.production(语法.对于声明.成分(语法.声明, 连词_对, 语法.迭代器, 连词_于, 语法.遍历范围))
    @分析器母机.production(语法.对于声明.成分(语法.声明, 连词_对, 语法.迭代器, 冒号, 语法.遍历范围))
    def 单个对于声明(self, 片段):
        倒装 = 片段[1:]
        倒装.append([片段[0]])
        return self.对于声明(倒装)

    @分析器母机.production(语法.名称.成分(标识符))
    def 标识符(self, 片段):
        标识 = 片段[0].getstr()
        名称 = 语法树.新节点(语法.名称,
            标识=标识,
            上下文=(ast.Load()),
            片段=片段)
        if not 标识.startswith('$'):
            return 名称
        名称.id = 'self'
        return 语法树.属性(
            值=名称,
            属性=标识.replace('$', ''),
            片段=片段)

    @分析器母机.error
    def error_handler(self, 词):
        if 词.getstr() == '\n':
            return
        # TODO: 最好取到语法信息(上下文)
        raise 语法错误(
            信息=('没认出这个词 "%s"' % 词.gettokentype()),
            文件名=self.文件名,
            行号=语法树.取行号(词),
            列号=语法树.取列号(词),
            源码=self.源码)

    def 形参合法化(self, 形参):
        带默认值 = False
        for 参数 in 形参.args:
            if hasattr(参数, 'default') and 参数.default:
                带默认值 = True
                形参.defaults.append(参数.default)
            elif 带默认值:
                raise 语法错误(信息='需要一个表达式指定默认值',
                  文件名=self.文件名,
                  行号=arg.lineno,
                  列号=arg.col_offset,
                  源码=self.源码)

        return 形参

    def 转换为多项(self, 各实参):
        if not isinstance(各实参, ast.arguments):
            return 各实参
        return 语法树.多项(上下文=ast.Load(),
            元素=[ast.Name((arg.arg), (ast.Load()), lineno=(arg.lineno), col_offset=(arg.col_offset)) for arg in 各实参.args],
            片段=各实参)

    分析器 = LRParser(分析器母机.build())

    def __init__(self, 分词器=分词器):
        self.分词器 = 分词器
        self.文件名 = ''
        self.匿名函数 = {}
        self.源码 = None

    def 分析(self, 源码, 源码文件=''):
        self.源码 = 源码.split("\n")
        语法树.源码 = self.源码
        self.文件名 = 源码文件
        try:
            各词 = self.分词器.lex(源码)
            # self.查看(各词)
            节点 = self.分析器.parse(各词, state=self)
        except LexingError as e:
            raise 词法错误(异常=e,
                    文件名=源码文件,
                    源码=源码)

        节点 = AnnoFuncInsertPass(self.匿名函数).visit(节点)
        节点 = NameFixPass(源码文件).visit(节点)
        return 节点

    def 查看(self, 各词):
        for 词 in 各词:
            print(f"{词}={词.getsourcepos()}")
