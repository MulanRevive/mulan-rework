from rply import ParserGenerator
from rply.errors import LexingError
from rply_parser import LRParser
from 分析器.语法树 import *
from 分析器.错误 import 语法错误

from 分析器.词法分析器 import 分词器
from 分析器.词法分析器 import *
from 分析器.语法树处理 import NameFixPass

class 语法分析器:

    # TODO: 改进可视化 parse 过程(各个语法规则的顺序), 方便调试
    调试 = False

    # TODO: 提取语法名称, 按定义的先后顺序. 现有问题: 如何解决与处理函数的重名问题, 比如"数"
    模块 = '模块'
    块 = '块'
    注水声明列表 = '注水声明列表'
    #数 = '数'
    字符串 = '字符串'

    分析器母机 = ParserGenerator(
        规则,
        precedence=[
            #('nonassoc', ['标识符']),
            ('right', ['?', ':']),
            ('left', [连词_或]),
            ('left', [连词_且]),
            # nonassoc 参考: http://www.dabeaz.com/ply/ply.html
            # non-associativity in the precedence table. This would be used when you don't want operations to chain together
            ('nonassoc', ['>', '<', '>=', '<=', '!==', '===']),
            ('left', ['!=', '==']),
            ('nonassoc', [连词_每隔]),
            ('nonassoc', [点点, 点点小于]),
            #('nonassoc', ['(']),
            ('left', [加, 減]),
            ('left', [星号, 除]),
            ('left', [非]),
        ]
    )

    # ast 参考: https://docs.python.org/3.7/library/ast.html#abstract-grammar

    class 语法:
        def __init__(self, 名称):
            self.名称 = 名称

        def 构成(self, *成分):
            return self.名称 + " : " + " ".join(成分)

    @分析器母机.production(语法(模块).构成('注水声明列表'))
    def 模块(self, 片段):
        return 语法树.模块(主体=片段[0], 忽略类型=[])

    @分析器母机.production(语法(块).构成(分号))
    @分析器母机.production(语法(块).构成(前大括号, 注水声明列表, 后大括号))
    def 块(self, 片段):
        if 语法分析器.调试:
            print('块')
        if len(片段) == 3:
            if 片段[1]:
                return 片段[1]
        return [语法树.空转(片段)]

    # TODO: 分号
    @分析器母机.production(语法(注水声明列表).构成())
    @分析器母机.production(语法(注水声明列表).构成('声明列表'))
    @分析器母机.production(语法(注水声明列表).构成('声明列表', '换行'))
    def 注水声明列表(self, 片段):
        if 语法分析器.调试:
            print('注水声明列表')
        if len(片段) > 0:
            return 片段[0]
        return []

    # TODO： 分号
    @分析器母机.production(语法('声明列表').构成('声明'))
    @分析器母机.production(语法('声明列表').构成('声明列表', 换行, '声明'))
    def 声明列表(self, 片段):
        if 语法分析器.调试:
            print('声明列表')
        if len(片段) == 1:
            return [片段[0]]
        片段[0].append(片段[(-1)])
        return 片段[0]

    @分析器母机.production(语法('声明').构成('类型定义'))
    @分析器母机.production(语法('声明').构成('函数'))
    @分析器母机.production(语法('声明').构成('条件声明'))
    @分析器母机.production(语法('声明').构成('每当声明'))
    @分析器母机.production(语法('声明').构成('对于声明'))
    @分析器母机.production(语法('声明').构成('外部声明'))
    def 混合声明(self, 片段):
        if 语法分析器.调试:
            print('混合声明')
        return 片段[0]

    @分析器母机.production(语法('类型定义').构成(名词_类型, '名称 各基准类 类型主体'))
    def 类型定义(self, 片段):
        return 语法树.类定义(
            名称=片段[1].id,
            各基准类=片段[2],
            主体=片段[-1],
            片段=片段)

    @分析器母机.production(语法('各基准类').构成())
    @分析器母机.production(语法('各基准类').构成(冒号, '表达式前缀'))
    def 各基准类(self, 片段):
        if 语法分析器.调试:
            print('各基准类')
        if len(片段) == 0:
            return []
        return [片段[1]]

    @分析器母机.production(语法('类型主体').构成(前大括号, '各类型内声明', 后大括号))
    def 类型主体(self, 片段):
        if 语法分析器.调试:
            print('类型主体')
        return 片段[1]

    @分析器母机.production(语法('各类型内声明').构成())
    @分析器母机.production(语法('各类型内声明').构成('各类型内声明 类型内声明'))
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

    @分析器母机.production(语法('类型内声明').构成('块'))
    @分析器母机.production(语法('类型内声明').构成('操作符'))
    @分析器母机.production(语法('类型内声明').构成('函数'))
    def 类型内声明(self, 片段):
        if 语法分析器.调试:
            print('类型内声明')
        return 片段[0]

    @分析器母机.production(语法('操作符').构成(名词_操作符, '二元操作符 操作数 块'))
    def 操作符(self, 片段):
        return 语法树.函数定义(名称=片段[1],
                        形参列表=片段[2],
                        主体=片段[-1],
                        片段=片段)

    @分析器母机.production(语法('操作数').构成(前小括号, '形参', 后小括号))
    def 操作数(self, 片段):
        各形参 = self.形参列表()
        各形参.args.append(语法树.形参(名称='self',
                               标注=None,
                               片段=片段))
        [各形参.args.append(形参) for 形参 in 片段 if isinstance(形参, ast.arg)]
        return 各形参

    @分析器母机.production(语法('二元操作符').构成(加))
    @分析器母机.production(语法('二元操作符').构成(減))
    def 二元操作符(self, 片段):
        对照表 = {
            '+': '__add__',
            '-': '__sub__',
        }
        return 对照表[片段[0].getstr()]

    @分析器母机.production(语法('声明').构成('引用声明'))
    @分析器母机.production(语法('声明').构成('表达式声明'))
    @分析器母机.production(语法('声明').构成('赋值'))
    @分析器母机.production(语法('声明').构成('增量赋值'))
    @分析器母机.production(语法('声明').构成('终止声明'))
    @分析器母机.production(语法('声明').构成('跳过声明'))
    @分析器母机.production(语法('声明').构成('返回声明'))
    def 声明(self, 片段):
        return 片段[0]

    # TODO: try-catch-throw

    # TODO: 更多引用方式

    @分析器母机.production(语法('模块位置').构成('模块名'))
    @分析器母机.production(语法('模块位置').构成(点))
    def 模块位置(self, 片段):
        return 片段[0]

    @分析器母机.production(语法('引用声明').构成(动词_引用, '各模块名', 连词_于, '模块位置'))
    @分析器母机.production(语法('引用声明').构成(动词_引用, 星号, 连词_于, '模块位置'))
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
                语法树.别名(名称='*',
                        别名=None,
                        片段=片段[1]))
        return 节点

    @分析器母机.production(语法('引用声明').构成(动词_引用, '各模块名'))
    def 引用声明(self, 片段):
        return 语法树.导入(
            名称=片段[1],
            片段=片段)

    @分析器母机.production(语法('各模块名').构成('模块名'))
    @分析器母机.production(语法('各模块名').构成('各模块名', 逗号, '模块名'))
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

    @分析器母机.production(语法('模块名').构成('模块名', 点, '名称'))
    @分析器母机.production(语法('模块名').构成('名称'))
    def 模块名(self, 片段):
        if len(片段) == 1:
            return 片段[0].id
        return '%s.%s' % (片段[0], 片段[2].id)

    @分析器母机.production(语法('表达式声明').构成('表达式前缀'))
    def 表达式声明(self, 片段):
        if 语法分析器.调试:
            print("表达式声明")
        return 语法树.表达式(值 = 片段[0], 片段 = 片段)

    @分析器母机.production(语法('返回声明').构成(动词_返回))
    @分析器母机.production(语法('返回声明').构成(动词_返回, '各表达式'))
    def 返回(self, 片段):
        值 = None
        if len(片段) == 2:
            if len(片段[1]) == 1:
                值 = 片段[1][0]
            else:
                值 = 语法树.多项(元素=片段[1],
                           上下文=ast.Load(),
                           片段=片段[1])
        return 语法树.返回(
            值=值,
            片段=片段)

    @分析器母机.production(语法('增量赋值').构成('表达式前缀 += 表达式'))
    @分析器母机.production(语法('增量赋值').构成('表达式前缀 -= 表达式'))
    def 增量赋值(self, 片段):
        运算符 = 片段[1].getstr()
        对照表 = {
            '+=': ast.Add(),
            '-=': ast.Sub(),
        }
        if 运算符 in 对照表:
            python运算 = 对照表[运算符]

        # 否则报错：
        # ValueError: expression must have Store context but has Load instead
        片段[0].ctx = ast.Store()

        return 语法树.增量赋值(片段[0], python运算, 片段[2], 片段=片段)

    @分析器母机.production(语法('赋值').构成('表达式前缀 = 表达式'))
    def 赋值(self, 片段):
        if 语法分析器.调试:
            print("赋值")
        片段[0].ctx = ast.Store()
        return 语法树.赋值(
            变量 = 片段[0],
            值 = 片段[2],
            片段 = 片段)

    @分析器母机.production(语法('外部声明').构成(形容词_外部, '各名称'))
    def 外部声明(self, 片段):
        return 语法树.全局([名称.id for 名称 in 片段[1]], 片段=片段)

    @分析器母机.production(语法('各表达式前缀').构成('表达式前缀 , 表达式前缀'))
    def 各表达式前缀(self, 片段):
        return [片段[0], 片段[2]]

    @分析器母机.production(语法('赋值').构成('各表达式前缀 = 各表达式'))
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
        # TODO: 研究何用. a, b = 2 会报错: cannot unpack non-iterable int object
        else:
            右边 = 片段[2][0]
        return 语法树.赋值(
            变量=左边,
            值=右边,
            片段=片段)

    @分析器母机.production(语法('终止声明').构成(动词_终止))
    def 终止声明(self, 片段):
        return 语法树.终止(片段 = 片段)

    @分析器母机.production(语法('跳过声明').构成(动词_跳过))
    def 跳过声明(self, 片段):
        return 语法树.跳过(片段 = 片段)

    @分析器母机.production(语法('二元表达式').构成('表达式', 加, '表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式', 減, '表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式', 星号, '表达式'))
    def 二元表达式(self, 片段):
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

    @分析器母机.production(语法('二元表达式').构成('表达式', 除, '表达式'))
    def 除法(self, 片段):
        return 语法树.调用(
            函数=语法树.名称(
                标识='__div__',
                上下文=(ast.Load()),
                片段=片段),
            参数=[片段[0], 片段[2]],
            片段=片段)

    @分析器母机.production(语法('二元表达式').构成('表达式 > 表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式 >= 表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式 < 表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式 <= 表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式 == 表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式 != 表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式 === 表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式 !== 表达式'))
    def 比较(self, 片段):
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

    @分析器母机.production(语法('二元表达式').构成('表达式', 连词_且, '表达式'))
    @分析器母机.production(语法('二元表达式').构成('表达式', 连词_或, '表达式'))
    def 布尔表达式(self, 片段):
        return 语法树.布尔操作(
            操作符=(ast.And() if 片段[1].getstr() == 'and' else ast.Or()),
            前项 = 片段[0],
            后项 = 片段[2],
            片段=片段)

    @分析器母机.production(语法('范围表达式').构成('表达式', 点点, '表达式'))
    @分析器母机.production(语法('范围表达式').构成('表达式', 点点小于, '表达式'))
    @分析器母机.production(语法('范围表达式').构成('范围表达式', 连词_每隔, '表达式'))
    def 范围表达式(self, 片段):
        连词 = 片段[1].getstr()
        if 连词 != 'by':
            起 = 片段[0]
            止 = 片段[2]
            if 连词 == '..':
                止 = 语法树.二元运算(止,
                             ast.Add(),
                             语法树.数(1, 片段=止),
                             片段=止)
                止.fixed = True
            return 语法树.调用(
                函数=语法树.名称(标识='range',
                          上下文=ast.Load(),
                          片段=片段),
                参数=[起, 止],
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
                为正 = 语法树.比较(
                        前项=片段[2],
                        操作符=ast.Gt(),
                        后项=语法树.数(0, 片段[2]),
                        片段=片段[2])
                增量 = 语法树.如果表达式(
                    条件=为正,
                    主体=止.right,
                    否则=语法树.数(-1, 片段[2]),
                    片段=片段)
                止.right = 增量
                delattr(止, 'fixed')
            return 片段[0]

    # TODO: ~
    @分析器母机.production(语法('一元表达式').构成(減, '表达式'))
    @分析器母机.production(语法('一元表达式').构成(非, '表达式'))
    def 一元表达式(self, 片段):
        操作符 = 片段[0].getstr()
        对照表 = {
            '-': ast.USub(),
            '!': ast.Not(),
        }
        return 语法树.一元操作(对照表[操作符], 片段[1], 片段=片段)

    @分析器母机.production(语法('三元表达式').构成('表达式 ? 表达式 : 表达式'))
    def 三元表达式(self, 片段):
        return 语法树.如果表达式(
            条件=片段[0],
            主体=片段[2],
            否则=片段[-1],
            片段=片段)

    @分析器母机.production(语法('首要表达式').构成('( 表达式 )'))
    def 首要表达式(self, 片段):
        return 片段[1]

    @分析器母机.production(语法('表达式前缀').构成('变量'))
    @分析器母机.production(语法('表达式前缀').构成('调用'))
    @分析器母机.production(语法('表达式前缀').构成('字符串'))
    @分析器母机.production(语法('表达式前缀').构成('列表表达式'))
    def 表达式前缀(self, 片段):
        if 语法分析器.调试:
            print("表达式前缀")
        return 片段[0]

    @分析器母机.production(语法('片').构成('表达式'))
    def 索引(self, 片段):
        return 语法树.索引(值=片段[0], 片段=片段)

    @分析器母机.production(语法('变量').构成('表达式前缀 [ 片 ]'))
    def 片表达式(self, 片段):
        return 语法树.下标(片段[0], 片段[2], 片段)

    # TODO: 添加测试: 调用().名称
    @分析器母机.production(语法('变量').构成('表达式前缀', 点, '名称'))
    def 属性表达式(self, 片段):
        return 语法树.属性(
            值=片段[0],
            属性=片段[2].id,
            片段=片段)

    @分析器母机.production(语法('变量').构成('名称'))
    def 变量(self, 片段):
        return 片段[0]

    @分析器母机.production(语法('实参部分').构成('( 各实参 )'))
    @分析器母机.production(语法('实参部分').构成('( )'))
    def 实参部分(self, 片段):
        if 语法分析器.调试:
            print("实参部分")
        if len(片段) != 3:
            return []
        return 片段[1]

    # 变量->表达式前缀, 以支持高阶函数调用, 如 f(1)(2)
    @分析器母机.production(语法('调用').构成('表达式前缀 实参部分'))
    def 调用(self, 片段):
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

    @分析器母机.production(语法('数').构成(整数))
    @分析器母机.production(语法('数').构成(小数))
    def 数(self, 片段):
        try:
            return 语法树.数(int(片段[0].getstr(), 0), 片段)
        except ValueError:
            return 语法树.数(float(片段[0].getstr()), 片段)

    @分析器母机.production(语法(字符串).构成(双引号字符串))
    @分析器母机.production(语法(字符串).构成(单引号字符串))
    def 字符串(self, 片段):
        值 = 片段[0].getstr()
        值 = 值[1:-1]
        return 语法树.字符串(值, 片段)

    @分析器母机.production(语法('常量').构成(名词_真))
    def 常量_真(self, 片段):
        return 语法树.常量(True, 片段=片段)

    @分析器母机.production(语法('常量').构成(名词_假))
    def 常量_假(self, 片段):
        return 语法树.常量(False, 片段=片段)

    @分析器母机.production(语法('常量').构成(名词_空))
    def 常量_空(self, 片段):
        return 语法树.常量(None, 片段=片段)

    @分析器母机.production(语法('表达式').构成('二元表达式'))
    @分析器母机.production(语法('表达式').构成('一元表达式'))
    @分析器母机.production(语法('表达式').构成('表达式前缀'))
    @分析器母机.production(语法('表达式').构成('首要表达式'))
    @分析器母机.production(语法('表达式').构成('三元表达式'))
    @分析器母机.production(语法('表达式').构成('数')) # TODO: 为何要, precedence='==' ?
    @分析器母机.production(语法('表达式').构成('常量'))

    # ? 如果没有 precedence 就 1 shift/reduce conflict
    @分析器母机.production(语法('表达式').构成('范围表达式'), precedence='==')
    def 表达式(self, 片段):
        if 语法分析器.调试:
            print("表达式")
        return 片段[0]

    @分析器母机.production(语法('列表表达式').构成('[ ]'))
    @分析器母机.production(语法('列表表达式').构成('[ 各表达式 ]'))
    def 列表表达式(self, 片段):
        元素 = 片段[1] if len(片段) == 3 else []
        return 语法树.列表(元素, 片段=片段)

    @分析器母机.production(语法('各名称').构成('名称'))
    @分析器母机.production(语法('各名称').构成('各名称 , 名称'))
    @分析器母机.production(语法('各实参').构成('实参'))
    @分析器母机.production(语法('各实参').构成('各实参 , 实参'))
    @分析器母机.production(语法('各表达式').构成('表达式'))
    @分析器母机.production(语法('各表达式').构成('各表达式 , 表达式'))
    def 各实参(self, 片段):
        if 语法分析器.调试:
            print("各实参")
        if len(片段) == 3:
            片段[0].append(片段[2])
            return 片段[0]
        return [片段[0]]

    @分析器母机.production(语法('实参').构成('表达式'))
    def 实参(self, 片段):
        if 语法分析器.调试:
            print("实参")
        return (片段[0], None)

    @分析器母机.production(语法('形参列表').构成())
    @分析器母机.production(语法('形参列表').构成('非空形参列表'))
    def 形参列表(self, 片段=[]):
        if not 片段:
            return 语法树.各形参([])
        # TODO: 如支持形参默认值, 需要 legalize_arguments
        return 片段[0]

    @分析器母机.production(语法('非空形参列表').构成('形参'))
    @分析器母机.production(语法('非空形参列表').构成('非空形参列表 , 形参'))
    def 非空形参列表(self, 片段):
        if len(片段) == 1:
            各形参 = self.形参列表()
        else:
            各形参 = 片段[0]
        各形参.args.append(片段[-1])
        return 各形参

    @分析器母机.production(语法('形参').构成('名称'))
    def 形参(self, 片段):
        return 语法树.形参(
            名称=片段[0].id,
            标注=(None if len(片段) == 1 else 片段[-1]),
            片段=片段)

    @分析器母机.production(语法('函数').构成(名词_函数, '标识符 ( 形参列表 ) 块'))
    @分析器母机.production(语法('函数').构成(名词_函数, '标识符 块'))
    def 函数(self, 片段):
        return 语法树.函数定义(
            名称=(片段[1].getstr()),
            形参列表=(片段[3] if len(片段) == 6 else self.形参列表()),
            主体=片段[-1],
            片段=片段)

    @分析器母机.production(语法('条件声明').构成(连词_如果, '表达式 块 否则如果声明'))
    @分析器母机.production(语法('条件声明').构成(连词_如果, '表达式 块', 连词_否则, '块'))
    @分析器母机.production(语法('否则如果声明').构成())
    @分析器母机.production(语法('否则如果声明').构成(连词_否则如果, '表达式 块 否则如果声明'))
    @分析器母机.production(语法('否则如果声明').构成(连词_否则如果, '表达式 块', 连词_否则, '块'))
    def 条件声明(self, 片段):
        if len(片段) == 0:
            return []
        否则部分 = 片段[-1]
        return 语法树.如果(
            条件=片段[1],
            主体=片段[2],
            否则=否则部分 if isinstance(否则部分, list) else [否则部分],
            片段=片段)

    @分析器母机.production(语法('条件声明').构成('声明', 连词_如果, '表达式'))
    def 条件倒置声明(self, 片段):
        return 语法树.如果(
            条件=片段[-1],
            主体=[片段[0]],
            否则=[],
            片段=片段)

    @分析器母机.production(语法('声明').构成('块'))
    def 单块(self, 片段):
        return 语法树.如果(
            条件=语法树.常量(True, 片段),
            主体=片段[0],
            否则=[],
            片段=片段)

    @分析器母机.production(语法('每当声明').构成(连词_每当, '表达式 块'))
    def 每当(self, 片段):
        return 语法树.每当(
            条件=片段[1],
            主体=片段[2],
            片段=片段)

    @分析器母机.production(语法('每当声明').构成(动词_循环, '块'))
    def 无条件每当(self, 片段):
        return 语法树.每当(
            条件=语法树.常量(True, 片段),
            主体=片段[1],
            片段=片段)

    @分析器母机.production(语法('迭代器').构成('表达式前缀'))
    def 迭代器(self, 片段):
        return 片段[0]

    @分析器母机.production(语法('遍历范围').构成('表达式'))
    def 遍历范围(self, 片段):
        # TODO: 处理 ast.Starred
        return 片段[0]

    @分析器母机.production(语法('对于声明').构成(连词_对, '迭代器', 连词_于, '遍历范围 块'))
    @分析器母机.production(语法('对于声明').构成(连词_对, '迭代器', ': 遍历范围 块'))
    def 对于声明(self, 片段):
        目标 = 片段[1]
        # TODO: 遍历 list
        目标.ctx = ast.Store()
        return 语法树.对于(目标=目标,
                      遍历范围=片段[3],
                      主体=片段[4],
                      片段=片段)

    @分析器母机.production(语法('对于声明').构成('声明', 连词_对, '迭代器', 连词_于, '遍历范围'))
    @分析器母机.production(语法('对于声明').构成('声明', 连词_对, '迭代器 : 遍历范围'))
    def 单个对于声明(self, 片段):
        倒装 = 片段[1:]
        倒装.append([片段[0]])
        return self.对于声明(倒装)

    @分析器母机.production(语法('名称').构成('标识符'))
    def 标识符(self, 片段):
        标识 = 片段[0].getstr()
        return 语法树.名称(
            标识=标识,
            上下文=(ast.Load()),
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

    分析器 = LRParser(分析器母机.build())

    def __init__(self, 分词器=分词器):
        self.分词器 = 分词器
        self.文件名 = ''
        self.源码 = None

    def 分析(self, 源码, 源码文件):
        self.源码 = 源码.split("\n")
        self.文件名 = 源码文件
        try:
            各词 = self.分词器.lex(源码)
            节点 = self.分析器.parse(各词, state=self)
        except LexingError as e:
            raise 语法错误(
                信息=('分词时没认出这个词 "%s"' % 源码[e.getsourcepos().idx]),
                文件名=源码文件,
                行号=e.getsourcepos().lineno,
                列号=e.getsourcepos().colno,
                源码=源码.split("\n"))

        节点 = NameFixPass(源码文件).visit(节点)
        return 节点

    def 查看(各词):
        for 词 in 各词:
            print(词)
