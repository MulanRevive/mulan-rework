#!/usr/bin/env python3

import sys
import ast
from 木兰.分析器.词法分析器 import 分词器
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.环境 import 创建全局变量
from 木兰.交互 import 开始交互
from 木兰.功用.反馈信息 import 反馈信息
from 木兰.功用.调试辅助 import 语法树相关


def 中(argv=None):
    if argv is None:
        argv = sys.argv

    if len(sys.argv) == 1:
        sys.exit(开始交互())

    源码文件 = sys.argv[1]
    with open(源码文件, 'r', encoding='utf-8') as f:
        源码 = f.read()

    分析器 = 语法分析器(分词器)
    节点 = 分析器.分析(源码, 源码文件)

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
        sys.stderr.write(f"语法错误: {语法错误}\n")
