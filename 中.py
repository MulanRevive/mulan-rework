#!/usr/bin/env python3

import re, sys, traceback
import ast, python
from 词法分析器 import 分词器
from 分析器 import 语法分析器
from 环境 import 创建全局变量
from 功用.语法树相关 import 语法树相关
from 功用.反馈信息 import 反馈信息
from 语法树处理 import NameFixPass

def 查看(各词):
    for 词 in 各词:
        print(词)

源码文件 = sys.argv[1]
with open(源码文件, 'r', encoding='utf-8') as f:
    源码 = f.read()

各词 = 分词器.lex(源码)
#查看(各词)

分析器 = 语法分析器().创建(源码, 源码文件)
节点 = 分析器.parse(各词)

节点 = NameFixPass(源码文件).visit(节点)

#print(python.dump(节点))
#print(ast.dump(节点, True, True))
#print(语法树相关.格式化节点(节点, 1))

# 参考：https://docs.python.org/3.7/library/functions.html?highlight=compile#compile
try:
    可执行码 = compile(节点, 源码文件, 'exec')

    环境变量 = 创建全局变量()

    try:
        exec(可执行码, 环境变量)
    except Exception as e:
        try:
            sys.stderr.write('%s\n' % 反馈信息(e, 源码文件))
        finally:
            e = None
            del e
except SyntaxError as 语法错误:
    sys.stderr.write("语法错误: " + str(语法错误) + '\n')

