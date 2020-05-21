from rply import LexerGenerator
import rply, re

规则 = [
'整数',
'加',
'減',
'乘',
'除',
'标识符',
'(',
')',
'===',
'!==',
'==',
'!=',
'>',
'<',
'>=',
'<=',
'换行',
'=',
',',
'前括号',
'后括号',
'连词_如果',
'连词_否则如果',
'连词_否则',
'连词_或',
'连词_且',
'连词_每当',
'终止',
'跳过',
'名词_函数',
'动词_返回',
]

分词器母机 = LexerGenerator()

分词器母机.add('整数', '\\d+')
分词器母机.add('前括号', '{\\r*\\n*') # TODO: 何用？ , flags=(re.DOTALL)
分词器母机.add('后括号', '\\r*\\n*}') # , flags=(re.DOTALL)
分词器母机.add('连词_且', '\\band\\b')
分词器母机.add('连词_或', '\\bor\\b')
分词器母机.add('连词_如果', '\\bif\\b')
分词器母机.add('连词_否则如果', '\\r*\\n*\\s*elif\\s*\\r*\\n*') # TODO: 何用？ , flags=(re.DOTALL)
分词器母机.add('连词_否则', '\\r*\\n*\\s*else\\s*\\r*\\n*') # , flags=(re.DOTALL)
分词器母机.add('连词_每当', '\\bwhile\\b')
分词器母机.add('动词_返回', '\\breturn\\b')
分词器母机.add('终止', '\\bbreak\\b')
分词器母机.add('跳过', '\\bcontinue\\b')
分词器母机.add('名词_函数', '\\bfunc\\b')
分词器母机.add('标识符', '\\$?[_a-zA-Z][_a-zA-Z0-9]*')
分词器母机.add('(', '\\(')
分词器母机.add(')', '\\)')
分词器母机.add('===', '===')
分词器母机.add('!==', '!==')
分词器母机.add('==', '==')
分词器母机.add('!=', '!=')
分词器母机.add('>=', '>=')
分词器母机.add('<=', '<=')
分词器母机.add('>', '>')
分词器母机.add('<', '<')
分词器母机.add('=', '=')
分词器母机.add(',', ',')
分词器母机.add('加', '\\+')
分词器母机.add('減', '-')
分词器母机.add('乘', '\\*')
分词器母机.add('除', '/')
分词器母机.add('换行', '\n')
分词器母机.ignore('[ \t]+') # TODO: \r 何用?

分词器 = 分词器母机.build()
