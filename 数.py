import python
from 数分析器 import 分析器, 分词器

源码文件 = '数.mulan'
with open(源码文件, 'r') as f:
    源码 = f.read()

各词 = 分词器.lex(源码)

节点 = 分析器.parse(各词)

print(python.dump(节点))

code = compile(节点, 源码文件, 'exec')

exec(code, {})