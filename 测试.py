#!/usr/bin/env python3

import subprocess

from sys import platform

路径 = '测试/'
# 不确定为何输出是bytes：https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
期望值 = {
    "运算/加.ul": b'5',
    "运算/减.ul": b"1",
    "运算/乘.ul": b"6",
    "运算/除整.ul": b"2",
    "运算/除留整.ul": b"1", # TODO: 多行代码
    "运算/四则运算.ul": b"4",
    "运算/加小数.ul": b"5.0",
    "运算/除小数.ul": b"2.0",
    "运算/比较.ul": b"2222222222222",
    "运算/赋值.ul": b"2",
    "运算/赋值两次.ul": b"6",
    "流程控制/条件.ul": b"3",
    "流程控制/条件否则如果.ul": b"2",
    "流程控制/条件否则.ul": b"4",
    "流程控制/条件三段.ul": b"5",
    "流程控制/条件倒置.ul": b"6",
    "流程控制/条件否则多行.ul": b"34",
    "流程控制/每当.ul": b"6",
    "流程控制/循环控制.ul": b"23",
    "流程控制/三元表达式.ul": b"213",
    "函数/函数_无参数.ul": b"2",
    "函数/函数_单参数.ul": b"2",
    "函数/函数_多参数.ul": b"123",
    "函数/函数_多层调用.ul": b"3",
    "函数/二阶函数.ul": b"11",
    "函数/返回空.ul": b"2",
    "函数/返回单值.ul": b"2",
    "特殊字符/多行.ul": b"23", # TODO: 如果末尾加空行, 报错 rply.errors.ParsingError: (None, None)
    "特殊字符/块.ul": b"2",
    "特殊字符/块多行.ul": b"3",
    "特殊字符/空格.ul": b"2",
    "特殊字符/制表符.ul": b"2",
    "特殊字符/缩进.ul": b"2",
    "特殊字符/注释块.ul": b"2",
    "引用/引用本地py.ul": b"2",
    "引用/引用本地包内py.ul": b"2",
    "引用/引用本地多py.ul": b"23",
    "引用/引用本地py全部内容.ul": b"32",

    # TODO： 深究 python 中 'from . import *'的含义。参考：
    # https://stackoverflow.com/questions/57774193/what-does-from-dot-import-asterisk-do-in-python-3
    # "引用/引用本地py点.ul": b"2",

    # TODO: 引用 python 标准库, 第三方库

    "引用/引用本地py某内容.ul": b"2",
    # "引用/引用木兰.ul": b"2", TODO: 需要对.ul 文件特别处理, 见逆向 env
    "综合.ul": b"10",
    #"错误处理/死递归.ul": b"test",
    # "空行.ul": b"1", TODO: 暂报语法错误
}

# 多进程参考：https://shuzhanfan.github.io/2017/12/parallel-processing-python-subprocess/
进程表 = {}

# 参考：https://stackoverflow.com/questions/748028/how-to-get-output-of-exe-in-python-script
for 文件 in 期望值:
    进程表[文件] = subprocess.Popen(["./中.py", 路径 + 文件], stdout=subprocess.PIPE)

失败表 = {}

for 文件 in 进程表:
    反馈 = 进程表[文件].communicate()
    输出 = 反馈[0]
    # TODO: 确认报错信息
    报错 = 反馈[1]

    if 输出 == 期望值[文件]:
        print("通过： " + 文件)
    # elif 报错 == 期望值[文件]:
    #    print("错误一致: " + 文件)
    else:
        失败表[文件] = 输出 or 报错

print("===================")
if len(失败表) > 0:
    for 文件 in 失败表:
        print("失败： " + 文件 + " 期望：" + str(期望值[文件]) + " 实际：" + str(失败表[文件]))
else:
    print("！全部通过！")

