import ast
from rply import Token
from rply import ParserGenerator

### 分词器部分
from rply import LexerGenerator

分词器母机 = LexerGenerator()

分词器母机.add('整数', r'\d+')
分词器母机.add('加', '\\+')
分词器母机.add('減', '-')
分词器母机.add('乘', '\\*')
分词器母机.add('除', '/')
分词器母机.add('标识符', '\\$?[_a-zA-Z][_a-zA-Z0-9]*')
分词器母机.add('(', '\\(')
分词器母机.add(')', '\\)')
分词器母机.add('换行', '\n')

分词器 = 分词器母机.build()

### 语法分析器部分
class 语法分析器:

    def 取源码位置(片段):
        if isinstance(片段, Token):
            return 片段.getsourcepos()

    def 取行号(片段):
        try:
            return 语法分析器.取源码位置(片段).lineno
        except:
            return 0

    分析器母机 = ParserGenerator(
        # 所有词名
        [
            '整数',
            '加',
            '減',
            '乘',
            '除',
            '标识符',
            '(',
            ')',
            '换行',
        ],
        precedence=[
            ('left', ['加', '減']),
            ('left', ['乘', '除']),
        ]
    )

    # ast 参考: https://docs.python.org/3.7/library/ast.html#abstract-grammar

    @分析器母机.production('模块 : 声明列表')
    def 模块(片段):
        return 语法树.模块(主体=片段[0], 忽略类型=[])

    @分析器母机.production('声明列表 : 表达式声明')
    @分析器母机.production('声明列表 : 声明列表 换行 表达式声明')
    def 声明列表(片段):
        #print('声明列表')
        if len(片段) == 1:
            return [片段[0]]
        片段[0].append(片段[(-1)])
        return 片段[0]

    @分析器母机.production('表达式声明 : 表达式')
    def 表达式声明(片段):
        return 语法树.表达式(值 = 片段[0], 行号=0, 列号=0)

    @分析器母机.production('表达式 : 二元表达式')
    @分析器母机.production('表达式 : 数')
    @分析器母机.production('表达式 : 调用')
    def 表达式(片段):
        return 片段[0]

    @分析器母机.production('数 : 整数')
    def 数(片段):
        数值 = int(片段[0].getstr(), 0)
        return 语法树.数(数值, 行号=语法分析器.取行号(片段[0]), 列号=0)

    @分析器母机.production('二元表达式 : 表达式 加 表达式')
    @分析器母机.production('二元表达式 : 表达式 減 表达式')
    @分析器母机.production('二元表达式 : 表达式 乘 表达式')
    def 二元表达式(片段):
        左 = 片段[0]
        右 = 片段[2]
        运算符 = 片段[1].getstr()
        python运算 = 运算符
        if 运算符 == '+':
            python运算 = ast.Add()
        elif 运算符 == '-':
            python运算 = ast.Sub()
        elif 运算符 == '*':
            python运算 = ast.Mult()
        else:
            breakpoint()
        return 语法树.二元运算(左, python运算, 右, 行号=0, 列号=0)

    @分析器母机.production('二元表达式 : 表达式 除 表达式')
    def 除法(片段):
        return 语法树.调用(
            函数=语法树.名称(
                标识='__除__',
                上下文=(ast.Load()),
                行号=0,
                列号=0),
            参数=[片段[0], 片段[2]],
            行号=0,
            列号=0)

    @分析器母机.production('调用 : 变量 参数部分')
    def 调用(片段):
        各参数 = []
        for 值, 键 in 片段[1]:
            if 键 is None:
                各参数.append(值)

        return 语法树.调用(
                片段[0],
                参数=各参数,
                行号=0,
                列号=0)

    @分析器母机.production('参数部分 : ( 各参数 )')
    def 参数部分(片段):
        if len(片段) != 3:
            return []
        return 片段[1]

    @分析器母机.production('各参数 : 参数')
    def 各参数(片段):
        return [片段[0]]

    @分析器母机.production('变量 : 名称')
    def 变量(片段):
        return 片段[0]

    @分析器母机.production('名称 : 标识符')
    def 标识符(片段):
        标识 = 片段[0].getstr()
        return 语法树.名称(
            标识=标识,
            上下文=(ast.Load()),
            行号=0,
            列号=0)

    @分析器母机.production('参数 : 表达式')
    def 参数(片段):
        return (片段[0], None)

    分析器 = 分析器母机.build()

    def 创建(self):
        return self.分析器

class 语法树:
    @staticmethod
    def 模块(主体, 忽略类型):
        return ast.Module(body = 主体, type_ignores = 忽略类型)

    @staticmethod
    def 表达式(值, 行号, 列号):
        return ast.Expr(value = 值, lineno = 行号, col_offset = 列号)

    @staticmethod
    def 数(值, 行号, 列号):
        return ast.Num(值, lineno = 行号, col_offset = 列号)

    @staticmethod
    def 二元运算(左, 运算符, 右, 行号, 列号):
        return ast.BinOp(左, 运算符, 右, lineno = 行号, col_offset = 列号)

    @staticmethod
    def 名称(标识, 上下文, 行号, 列号):
        return ast.Name(id=标识, ctx=上下文, lineno=行号, col_offset=列号)

    @staticmethod
    def 调用(函数, 参数, 行号, 列号):
        return ast.Call(func=函数, args=参数, keywords=[], starargs=None, kwargs=None, lineno=行号, col_offset=列号)
