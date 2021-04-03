#!/usr/bin/env python3

import os, sys, getopt
import ast
from 木兰.分析器.词法分析器 import 分词器
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.生成 import 木兰
from 木兰.环境 import 创建全局变量
from 木兰.交互 import 开始交互
from 木兰.功用.反馈信息 import 反馈信息
from 木兰.功用.调试辅助 import 语法树相关

def 用途(程序):
    介绍 = '''使用方法: %s 源码文件
选项:
 --版本,         -版   显示版本
 --python变木兰, -兰   将 Python 源码转换为木兰源码
'''
    sys.stderr.write(介绍 % os.path.basename(程序))
    sys.exit(-1)

def 中(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        选项, 参数 = getopt.getopt(
            argv[1:],
            '兰版',
            [
                "python变木兰",
                '版本'])
    except getopt.GetoptError as e:
        try:
            sys.stderr.write(str(e) + '\n')
            用途(argv[0])
        finally:
            e = None
            del e

    版本 = False
    python变木兰 = False
    for 某项, 值 in 选项:
        if 某项 in ('-版', '--版本'):
            版本 = True
        elif 某项 in ("-兰", "--python变木兰"):
            python变木兰 = True

    if 版本:
        from 木兰 import __版本__
        sys.stderr.write('%s\n' % __版本__)
        sys.exit()

    if len(sys.argv) == 1:
        sys.exit(开始交互())

    if len(参数) > 0:
        源码文件 = 参数[0]
    with open(源码文件, 'r', encoding='utf-8') as f:
        源码 = f.read()

    if python变木兰:
        语法树节点 = ast.parse(源码, 源码文件)
        print(木兰.转换(语法树节点))
        return

    分析器 = 语法分析器(分词器)
    节点 = 分析器.分析(源码, 源码文件)

    #print(ast.dump(节点, True, True))
    #print(语法树相关.格式化节点(节点, 1))

    # 参考：https://docs.python.org/3.7/library/functions.html?highlight=compile#compile
    try:
        可执行码 = compile(节点, 源码文件, 'exec')

        环境变量 = 创建全局变量(文件名=源码文件)

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
