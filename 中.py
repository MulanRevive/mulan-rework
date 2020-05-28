#!/usr/bin/env python3

import re, sys
import ast, python
from 词法分析器 import 分词器
from 分析器 import 语法分析器
from 环境 import 创建全局变量
from 功用 import 语法树相关

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

#print(python.dump(节点))
#print(ast.dump(节点, True, True))
#print(语法树相关.格式化节点(节点, 1))

# 参考：https://docs.python.org/3.7/library/functions.html?highlight=compile#compile
try:
    可执行码 = compile(节点, 源码文件, 'exec')

    环境变量 = 创建全局变量()

    try:
        exec(可执行码, 环境变量)
    except RecursionError as 递归报错:
        sys.stderr.write("递归过深。请确认: 1、的确需要递归 2、递归的收敛正确" + '\n')
    except ZeroDivisionError as 除零报错:
        sys.stderr.write("请勿除零" + '\n')
    except NameError as 未定义:
        # 参考: https://github.com/program-in-chinese/study/blob/6084cbfc39166842b95d25d5c2fe419f1c604475/1-%E5%9F%BA%E7%A1%80/%E6%8E%A7%E5%88%B6%E5%8F%B0/%E8%A7%A3%E9%87%8A%E5%99%A8.py
        sys.stderr.write(re.sub(r"name '(.*)' is not defined", r"'\1'没定义就使用了", str(未定义)) + '\n')
except SyntaxError as 语法错误:
    sys.stderr.write("语法错误: " + str(语法错误) + '\n')

