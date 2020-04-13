import ast
import python
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
    数 = int(片段[0].getstr(), 0)
    # 匹配规则右部的片段列表
    return ast.Module(
                body=[
                    ast.Expr(
                        value=ast.Num(数,
                            lineno=0,
                            col_offset=0),
                        lineno=0,
                        col_offset=0)
                    ],
                type_ignores=[])

分析器 = 分析器母机.build()

源码文件 = '数.mulan'
with open(源码文件, 'r') as f:
    源码 = f.read()

各词 = 分词器.lex(源码)

节点 = 分析器.parse(各词)

print(python.dump(节点))

code = compile(节点, 源码文件, 'exec')

exec(code, {}) # 'print': print