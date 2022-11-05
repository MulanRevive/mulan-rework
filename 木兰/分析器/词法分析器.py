from rply import 分词器母机
import re

# 顺序与词法规则添加顺序一致. 值不为中文的是关键词.

小数 = '小数'
整数 = '整数'
十六进制数 = '十六进制数'
双引号字符串 = '双引号字符串'
单引号字符串 = '单引号字符串'
前大括号 = '前大括号'
后大括号 = '后大括号'
名词_空 = 'nil'
名词_真 = 'true'
名词_假 = 'false'
连词_且 = 'and'
连词_或 = 'or'
连词_如果 = 'if'
连词_否则如果 = 'elif'
连词_否则 = 'else'
连词_每当 = 'while'
动词_循环 = 'loop'
连词_对 = 'for'
动词_返回 = 'return'
动词_终止 = 'break'
动词_跳过 = 'continue'
名词_函数 = 'func'
名词_类型 = 'type'
动词_引用 = 'using'
连词_于 = 'in'
动词_试试 = 'try'
动词_接手 = 'catch'
动词_抛出 = 'throw'
动词_生成 = 'yield'
名词_操作符 = 'operator'
连词_每隔 = 'by'
形容词_外部 = 'extern'
名词_超类 = 'super'
名词_应变属性 = 'attr'
标识符 = '标识符'
点点点 = '...'
点点小于 = '..<'
点点 = '..'
点 = '.'
名词_自身 = '$'
前中括号 = '['
后中括号 = ']'
前小括号 = '('
后小括号 = ')'
严格等于 = '==='
严格不等于 = '!=='
等于 = '=='
不等于 = '!='
大于等于 = '>='
小于等于 = '<='
箭头 = '->'
位_左移 = '<<'
位_右移 = '>>'
位_与 = '&'
位_或 = '竖线'
大于 = '>'
小于 = '<'
符号_赋值 = '='
逗号 = ','
增量赋值 = '+='
减量赋值 = '-='
乘法赋值 = '*='
除法赋值 = '/='
左移赋值 = '<<='
右移赋值 = '>>='
求余赋值 = '%='
与赋值 = '&='
或赋值 = '竖线='
乘方赋值 = '^='
加 = '+'
减 = '-'
星号 = '*'
除 = '/'
求余 = '%'
乘方 = '^'
分号 = ';'
井号 = '#'
非 = '!'
问号 = '?'
冒号 = ':'
取反 = '~'
换行 = '换行'

规则 = [
    小数,
    整数,
    十六进制数,
    加,
    减,
    星号,
    除,
    标识符,
    前小括号,
    后小括号,
    严格等于,
    严格不等于,
    等于,
    不等于,
    位_左移,
    位_右移,
    位_与,
    位_或,
    大于,
    小于,
    大于等于,
    小于等于,
    换行,
    符号_赋值,
    逗号,
    前大括号,
    后大括号,
    连词_如果,
    连词_否则如果,
    连词_否则,
    连词_或,
    连词_且,
    连词_每当,
    动词_终止,
    动词_跳过,
    名词_函数,
    动词_返回,
    问号,
    冒号,
    动词_引用,
    点,
    连词_于,
    名词_空,
    非,
    名词_类型,
    名词_操作符,
    形容词_外部,
    名词_真,
    名词_假,
    双引号字符串,
    单引号字符串,
    连词_对,
    动词_生成,
    点点点,
    点点,
    点点小于,
    分号,
    增量赋值,
    减量赋值,
    乘法赋值,
    除法赋值,
    左移赋值,
    右移赋值,
    求余赋值,
    与赋值,
    或赋值,
    乘方赋值,
    动词_循环,
    前中括号,
    后中括号,
    连词_每隔,
    箭头,
    乘方,
    名词_自身,
    名词_应变属性,
    动词_试试,
    求余,
    名词_超类,
    取反,
    动词_抛出,
    动词_接手,
    井号,
]

分词器母机 = 分词器母机()

分词器母机.添了(十六进制数, '0[xX][0-9A-Fa-f]+')
分词器母机.添了(小数, r'\d+\.\d+')
分词器母机.添了(整数, r'\d+')
分词器母机.添了(双引号字符串, r'(")((?<!\\)\\\1|.)*?\1')
分词器母机.添了(单引号字符串, r"(')((?<!\\)\\\1|.)*?\1")  # \' 之前不能有 \

# 逆向中，只要正则表达式包含 \r*\n*，就使用了 flags=(re.DOTALL)，即便表达式中并无`.`。
# 由于此 flag 仅对 `.` 的行为起作用，对这些不带 `.` 的表达式应无效果，因此省去。
分词器母机.添了(前大括号, r'{\r*\n*')
分词器母机.添了(后大括号, r'\r*\n*}')
分词器母机.添了(名词_空, r'\bnil\b')
分词器母机.添了(名词_真, r'\btrue\b')
分词器母机.添了(名词_假, r'\bfalse\b')
分词器母机.添了(连词_且, r'\band\b')
分词器母机.添了(连词_或, r'\bor\b')
分词器母机.添了(连词_如果, r'\bif\b')
分词器母机.添了(连词_否则如果, r'\r*\n*\s*elif\s*\r*\n*')
分词器母机.添了(连词_否则, r'\r*\n*\s*else\s*\r*\n*')
分词器母机.添了(连词_每当, r'\bwhile\b')
分词器母机.添了(动词_循环, r'\bloop\b')
分词器母机.添了(连词_对, r'\bfor\b')
分词器母机.添了(动词_返回, r'\breturn\b')
分词器母机.添了(动词_终止, r'\bbreak\b')
分词器母机.添了(动词_跳过, r'\bcontinue\b')
分词器母机.添了(名词_函数, r'\bfunc\b')
分词器母机.添了(名词_类型, r'\btype\b')
分词器母机.添了(动词_引用, r'\busing\b')
分词器母机.添了(连词_于, r'\bin\b')
分词器母机.添了(动词_试试, r'\btry\b')
分词器母机.添了(动词_接手, r'\r*\n*\s*catch\s*\r*\n*')
# TODO: finally
分词器母机.添了(动词_抛出, r'\bthrow\b')
分词器母机.添了(名词_操作符, r'\boperator\b')
分词器母机.添了(动词_生成, r'\byield\b')
分词器母机.添了(连词_每隔, r'\bby\b')
分词器母机.添了(形容词_外部, r'\bextern\b')
分词器母机.添了(名词_超类, r'\bsuper\b')
分词器母机.添了(名词_应变属性, r'\battr\b')
分词器母机.添了(标识符, r'\$?[_a-zA-Z\u4e00-\u9fa5][_a-zA-Z0-9\u4e00-\u9fa5]*')
分词器母机.添了(点点点, r'\.\.\.')
分词器母机.添了(点点小于, r'\.\.<')
分词器母机.添了(点点, r'\.\.')
分词器母机.添了(点, r'\.')
分词器母机.添了(名词_自身, r'\$')
分词器母机.添了(前中括号, r'\[')
分词器母机.添了(后中括号, r'\]')
分词器母机.添了(前小括号, r'\(')
分词器母机.添了(后小括号, r'\)')
分词器母机.添了(严格等于, '===')
分词器母机.添了(严格不等于, '!==')
分词器母机.添了(等于, '==')
分词器母机.添了(不等于, '!=')
分词器母机.添了(大于等于, '>=')
分词器母机.添了(小于等于, '<=')
分词器母机.添了(箭头, '->')
分词器母机.添了(乘法赋值, '\*=')
分词器母机.添了(除法赋值, '/=')
分词器母机.添了(左移赋值, '<<=')
分词器母机.添了(右移赋值, '>>=')
分词器母机.添了(求余赋值, '%=')
分词器母机.添了(与赋值, r'&=')
分词器母机.添了(或赋值, r'\|=')
分词器母机.添了(乘方赋值, r'\^=')
分词器母机.添了(位_左移, '<<')
分词器母机.添了(位_右移, '>>')
分词器母机.添了(位_与, r'&')
分词器母机.添了(位_或, r'\|')
分词器母机.添了(大于, '>')
分词器母机.添了(小于, '<')
分词器母机.添了(符号_赋值, '=')
分词器母机.添了(逗号, ',')
分词器母机.添了(增量赋值, r'\+=')
分词器母机.添了(减量赋值, '-=')
分词器母机.添了(加, '\+')
分词器母机.添了(减, '-')
分词器母机.添了(星号, '\*')
分词器母机.添了(除, '/')
分词器母机.添了(求余, '%')
分词器母机.添了(乘方, r'\^')
分词器母机.添了(分号, ';')
分词器母机.添了(井号, '#')
分词器母机.添了(非, '!')
分词器母机.添了(问号, r'\?')
分词器母机.添了(冒号, ':')
分词器母机.添了(取反, '~')
分词器母机.添了(换行, r'\n')
分词器母机.略过('[ \t]+')  # TODO: \r 何用? 也许和 windows 换行有关
分词器母机.略过('//[^\n]*')
分词器母机.略过('/\\*.*?\\*/', 匹配参数=(re.DOTALL))

分词器 = 分词器母机.产出()
