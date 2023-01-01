#!/usr/bin/env python3

import ast
import getopt
import os
import sys

from sys import argv

from 木兰.交互 import 开始交互
from 木兰.分析器.词法分析器 import 分词器
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.功用.反馈信息 import 反馈信息
from 木兰.环境 import 创建全局变量
from 木兰.生成 import 木兰, python


def 用途(程序):
    介绍 = '''使用方法: %s [-树p码兰调交反执溯版助] 源码文件
    
选项：
 --语法树　　　　　 -树　　将木兰源码转换为 Python 语法树
 --木兰变python　　 -p 　　将木兰源码转换为 Python 源码
 --生成字节码　　　 -码　　将木兰源码转换为 donsok 字节码 (实验性)
 --python变木兰　　 -兰　　将 Python 源码转换为木兰源码
 --调试　　　　　　 -调　　使用 Pdb 环境调试代码
 --交互　　　　　　 -交　　以交互式审查脚本
 --反汇编　　　　　 -反　　将生成的 Python 字节码反汇编
 --执行代码=<代码>　-执　　执行来自命令行参数的代码
 --显示回溯　　　　 -溯　　显示异常的栈回溯信息
 --版本　　　　　　 -版　　显示版本
 --帮助　　　　　　 -助　　显示帮助信息
'''
    sys.stderr.write(介绍 % os.path.basename(程序))
    sys.exit(-1)


def 中(命令行各分段=None):
    if 命令行各分段 is None:
        命令行各分段 = argv

    try:
        所有选项, 参数 = getopt.getopt(
            命令行各分段[1:],
            '版助反交兰p码调溯树执词',
            [
                "语法树",
                "python变木兰",
                '版本',
                '木兰变python',
                '生成字节码',
                '调试',
                '反汇编',
                '执行代码=',
                '显示回溯',
                '帮助',
                '交互',
                '显示分词',
            ]
        )
    except getopt.GetoptError as e:
        try:
            sys.stderr.write(str(e) + '\n')
            用途(命令行各分段[0])
        finally:
            e = None
            del e

    源码文件 = None
    版本 = False
    python变木兰 = False
    语法树 = False
    生成python代码 = False
    生成字节码 = False
    调试 = False
    反汇编 = False
    命令行执行码 = None
    显示回溯 = False
    交互 = False
    显示分词 = False
    for 选项, 值 in 所有选项:
        if 选项 in ('-版', '--版本'):
            版本 = True
        elif 选项 in ("-兰", "--python变木兰"):
            python变木兰 = True
        elif 选项 in ("-树", "--语法树"):
            语法树 = True
        elif 选项 in ('--木兰变python', '-p'):
            生成python代码 = True
        elif 选项 in ('--生成字节码', '-码'):
            生成字节码 = True
        elif 选项 in ('--调试', '-调'):
            调试 = True
        elif 选项 in ('--反汇编', '-反'):
            反汇编 = True
        elif 选项 in ('--显示回溯', '-溯'):
            显示回溯 = True
        elif 选项 in ('--帮助', '-助'):
            用途(命令行各分段[0])
        elif 选项 in ('--交互', '-交'):
            交互 = True
        elif 选项 in ('--执行代码', '-执'):
            命令行执行码 = 值
        elif 选项 in ('--显示分词', '-词'):
            显示分词 = True

    if 版本:
        from 木兰 import __版本__
        sys.stderr.write('%s\n' % __版本__)
        sys.exit()

    if len(命令行各分段) == 1:
        sys.exit(开始交互())

    if 源码文件 is None:
        if len(参数) > 0:
            源码文件 = 参数[0]
        else:
            if not 命令行执行码:
                用途(命令行各分段[0])
    try:
        源码 = None

        if 命令行执行码:
            源码 = 命令行执行码
            源码文件 = '<命令行>'
        elif 源码文件 == '-':
            源码 = sys.stdin.read()
            源码文件 = '<标准输入流>'
        else:
            with open(源码文件, encoding='UTF-8') as 源码文件对象:
                源码 = 源码文件对象.read()

        if not 源码:
            sys.stderr.write('文件 %s 为空！' % 源码文件)
            sys.exit(-1)

        if 显示分词:
            各词 = 分词器.分词(源码)
            for 词 in 各词:
                print(词.gettokentype(), end=' ')
            return

        if python变木兰:
            语法树节点 = ast.parse(源码, 源码文件)
            print(木兰.转换(语法树节点))
            return

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
            except ModuleNotFoundError as _:
                sys.stderr.write(f"依赖库 pygen 未找到")
            return

        # 参考：https://docs.python.org/3.7/library/functions.html?highlight=compile#compile
        可执行码 = compile(节点, 源码文件, 'exec')

        if 反汇编:
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

        if 交互:
            sys.exit(开始交互(全局变量=环境变量))

    except Exception as e:
        if 显示回溯:
            raise

        if isinstance(e, SyntaxError):
            sys.stderr.write(f"语法错误: {e}\n")
        elif isinstance(e, TypeError):
            sys.stderr.write(f"类型错误: {e}\n")
        elif isinstance(e, ValueError):
            sys.stderr.write(f"语法错误: {e}\n")
        else:
            sys.stderr.write('%s\n' % 反馈信息(e, 源码文件))
