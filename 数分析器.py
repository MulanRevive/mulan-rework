import ast
from rply import ParserGenerator

### 分词器部分
from rply import LexerGenerator

分词器母机 = LexerGenerator()

分词器母机.add('数', r'\d+')

分词器 = 分词器母机.build()

### 语法树部分

from rply.token import BaseBox

### 语法分析器部分

分析器母机 = ParserGenerator(
    # 所有词名
    ['数']
)

# ast 参考: https://docs.python.org/3.7/library/ast.html#abstract-grammar

@分析器母机.production('表达式 : 数')
def 数表达式(片段):
    数值 = int(片段[0].getstr(), 0)
    数 = 语法树.数(数值, 行号=0, 列号=0)
    表达式 = 语法树.表达式(值 = 数, 行号=0, 列号=0)
    return 语法树.模块(主体=[表达式], 忽略类型=[])

分析器 = 分析器母机.build()

class 语法树:
    @staticmethod
    def 模块(主体, 忽略类型):
        return ast.Module(body = 主体, type_ignores = 忽略类型)

    @staticmethod
    def 表达式(值, 行号, 列号):
        return ast.Expr(value = 值, lineno = 行号, col_offset = 列号)

    @staticmethod
    def 数(值, 行号, 列号):
        return ast.Num(value = 值, lineno = 行号, col_offset = 列号)