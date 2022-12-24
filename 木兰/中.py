#!/usr/bin/env python3

import ast
import getopt
import os
import sys

from 木兰.交互 import 开始交互
from 木兰.分析器.词法分析器 import 分词器
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.功用.反馈信息 import 反馈信息
from 木兰.环境 import 创建全局变量
from 木兰.生成 import 木兰, python


def 用途(程序):
    介绍 = '''使用方法: %s 源码文件
选项:
 --版本,         -版   显示版本
 --帮助          -助   显示帮助信息
 --反编译        -反   反编译 Python 代码
 --交互          -交   以交互式审查脚本
 --python变木兰, -兰   将 Python 源码转换为木兰源码
 --木兰变python  -p    将木兰源码转换为 Python 源码
 --生成字节码     -码   将木兰源码转换为 donsok 字节码 (实验性)
 --调试          -调   使用 Pdb 环境调试代码
 --显示回溯       -溯   显示异常的栈回溯信息
 --语法树,       -树   语法树信息
 --执行代码=<代码> -执  执行来自命令行参数的代码
'''
    sys.stderr.write(介绍 % os.path.basename(程序))
    sys.exit(-1)


def 中(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        选项, 参数 = getopt.getopt(
            argv[1:],
            '版助反交兰p码调溯树执',
            [
                "语法树",
                "python变木兰",
                '版本',
                'dump-python',
                '生成字节码',
                '调试',
                '反编译',
                '执行代码='
            ]
        )
    except getopt.GetoptError as e:
        try:
            sys.stderr.write(str(e) + '\n')
            用途(argv[0])
        finally:
            e = None
            del e

    版本 = False
    python变木兰 = False
    语法树 = False
    生成python代码 = False
    生成字节码 = False
    调试 = False
    反编译 = False
    从命令行执行 = False
    for 某项, 值 in 选项:
        if 某项 in ('-版', '--版本'):
            版本 = True
        elif 某项 in ("-兰", "--python变木兰"):
            python变木兰 = True
        elif 某项 in ("-树", "--语法树"):
            语法树 = True
        elif 某项 == '--dump-python':
            生成python代码 = True
        elif 某项 in ('--生成字节码', '-码'):
            生成字节码 = True
        elif 某项 in ('--调试', '-调'):
            调试 = True
        elif 某项 in ('--反编译', '-反'):
            反编译 = True
        elif 某项 in ('--执行代码', '-执'):
            从命令行执行 = True
            源码文件 = '<命令行>'
            源码 = 值

    if 版本:
        from 木兰 import __版本__
        sys.stderr.write('%s\n' % __版本__)
        sys.exit()

    if len(sys.argv) == 1:
        sys.exit(开始交互())

    if not 从命令行执行:
        if len(参数) > 0:
            源码文件 = 参数[0]
        with open(源码文件, 'r', encoding='utf-8') as f:
            源码 = f.read()

    if python变木兰:
        语法树节点 = ast.parse(源码, 源码文件)
        print(木兰.转换(语法树节点))
        return
    try:
        分析器 = 语法分析器(分词器)
        节点 = 分析器.分析(源码, 源码文件)

        if 生成python代码:
            print(python.代码生成器().得到源码(节点))
            return

        if 语法树:
            print(ast.dump(节点, True, True))
            # print(语法树相关.格式化节点(节点, 1))
            return

        if 生成字节码:
            try:
                from pygen.compiler import Compiler
                print(Compiler().compile(节点, 源码文件).dump())
            except ModuleNotFoundError as 模块错误:
                sys.stderr.write(f"依赖库 pygen 未找到")
            return

        # 参考：https://docs.python.org/3.7/library/functions.html?highlight=compile#compile
        可执行码 = compile(节点, 源码文件, 'exec')

        if 反编译:
            from dis import dis
            dis(可执行码)
            return

        环境变量 = 创建全局变量(文件名=源码文件)

        if 调试:
            from pdb import run as Pdb运行, Restart as Pdb重新运行
            while True:
                try:
                    Pdb运行(可执行码, 环境变量, None)
                except Pdb重新运行:
                    pass
                else:
                    break

        else:
            exec(可执行码, 环境变量)

    except SyntaxError as 语法错误:
        sys.stderr.write(f"语法错误: {语法错误}\n")
    except TypeError as 类型错误:
        sys.stderr.write(f"类型错误: {类型错误}\n")
    except ValueError as 语法错误:
        sys.stderr.write(f"语法错误: {语法错误}\n")
    except Exception as e:
        try:
            sys.stderr.write('%s\n' % 反馈信息(e, 源码文件))
        finally:
            e = None
            del e
