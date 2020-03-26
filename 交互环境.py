import ast, sys, cmd
from rply import ParserGenerator

### 分词器部分
from rply import LexerGenerator

分词器母机 = LexerGenerator()

分词器母机.add('数', r'\d+')
分词器母机.add('加', r'\+')
分词器母机.add('减', r'-')
分词器母机.add('乘', r'×')
分词器母机.add('除', r'÷')
分词器母机.add('左括号', r'\(')
分词器母机.add('右括号', r'\)')

分词器母机.ignore(r'\s+')

分词器 = 分词器母机.build()

### 语法树部分

from rply.token import BaseBox

### 语法分析器部分

分析器母机 = ParserGenerator(
    # 所有词名
    ['数', '左括号', '右括号',
     '加', '减', '乘', '除'
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['加', '减']),
        ('left', ['乘', '除'])
    ]
)

@分析器母机.production('表达式 : 数')
def 数表达式(片段):
    # 匹配规则右部的片段列表
    return ast.Num((int(片段[0].getstr(), 0)),
                    lineno=0,#(self.getlineno(p)),
                    col_offset=0)

@分析器母机.production('表达式 : 左括号 表达式 右括号')
def 括号表达式(片段):
    return 片段[1]

@分析器母机.production('表达式 : 表达式 加 表达式')
@分析器母机.production('表达式 : 表达式 减 表达式')
@分析器母机.production('表达式 : 表达式 乘 表达式')
@分析器母机.production('表达式 : 表达式 除 表达式')
def 二元运算表达式(片段):
    左 = 片段[0]
    右 = 片段[2]
    运算符 = 片段[1]
    python运算 = 运算符
    if 运算符.gettokentype() == '加':
        python运算 = ast.Add()
    elif 运算符.gettokentype() == '减':
        python运算 = ast.Sub()
    elif 运算符.gettokentype() == '乘':
        python运算 = ast.Mult()
    elif 运算符.gettokentype() == '除':
        python运算 = ast.Div()
    else:
        raise AssertionError('不应出现')
    return ast.Expression(
        body=ast.BinOp(左,
          python运算, 右,
          lineno=0,
          col_offset=0),
        type_ignores=[])

分析器 = 分析器母机.build()

class 木兰(cmd.Cmd):
    intro = "Welcome to ulang's REPL..\nType 'help' for more informations."
    prompt = '> '

    def default(self, line):
        节点 = 分析器.parse(分词器.lex(line))
        # print(ast.dump(节点))
        代码 = compile(节点, '<STDIN>', 'eval')
        print(eval(代码))

    def do_quit(self, arg):
        sys.exit()

if __name__ == '__main__':
    木兰().cmdloop()
