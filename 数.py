#!/usr/bin/env python3

import sys
import ast, python
from 数分析器 import 分析器, 分词器
from 环境 import 创建全局变量

源码文件 = sys.argv[1]
with open(源码文件, 'r') as f:
    源码 = f.read()

各词 = 分词器.lex(源码)

节点 = 分析器.parse(各词)

#print(python.dump(节点))
#print(ast.dump(节点, True, True))

# 参考：https://docs.python.org/3.7/library/functions.html?highlight=compile#compile
可执行码 = compile(节点, 源码文件, 'exec')

环境变量 = 创建全局变量()

exec(可执行码, 环境变量)