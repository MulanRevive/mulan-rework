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
    "运算/除留整.ul": b"10",
    "运算/四则运算.ul": b"4",
    "运算/加小数.ul": b"5.0",
    "运算/除小数.ul": b"2.0",
    "运算/比较.ul": b"2222222222222",
    "运算/赋值.ul": b"2",
    "运算/赋值两次.ul": b"6",
    "运算/赋值增量.ul": b"21",
    "运算/一元操作.ul": b"2-1",
    "运算/赋值多项.ul": b"21",

    # TODO: 加上 `(2<1)!=nil and`
    "运算/空.ul": b"true",

    "流程控制/条件.ul": b"31",
    "流程控制/条件否则如果.ul": b"2",
    "流程控制/条件否则.ul": b"4",
    "流程控制/条件三段.ul": b"5",
    "流程控制/条件倒置.ul": b"65",
    "流程控制/条件否则多行.ul": b"34",
    "流程控制/每当.ul": b"6",
    "流程控制/循环控制.ul": b"2301201245",
    "流程控制/三元表达式.ul": b"213",
    "流程控制/循环for.ul": b"012012021230125",
    "流程控制/空块.ul": b"123",
    "流程控制/循环loop.ul": b"123",

    "函数/无参数.ul": b"22",
    "函数/单参数.ul": b"2",
    "函数/多参数.ul": b"123",
    "函数/多层调用.ul": b"3",
    "函数/二阶函数.ul": b"11",
    "函数/返回空.ul": b"2",
    "函数/返回单值.ul": b"2",
    "函数/全局.ul": b"42",
    "函数/无返回.ul": b"2nil",
    "函数/过滤.ul": b"[10]",
    "函数/map.ul": b"[1, 4, 9]",
    "函数/返回多值.ul": b"12", # TODO: 原本元组输出为 1, 2， 而非(1，2)
    "函数/匿名函数.ul": b"[1][1][3][3][1, 4]12",
    "函数/API/any.ul": b"true",
    "函数/API/文件.ul": b"hi",
    "函数/形参默认值.ul": b"2",
    "函数/指名参数.ul": b"466",

    "特殊字符/多行.ul": b"23", # TODO: 如果末尾加空行, 报错 rply.errors.ParsingError: (None, None)
    "特殊字符/块.ul": b"2",
    "特殊字符/块多行.ul": b"3",
    "特殊字符/空格.ul": b"2",
    "特殊字符/制表符.ul": b"2",
    "特殊字符/缩进.ul": b"2",
    "特殊字符/注释块.ul": b"23",
    "特殊字符/中文标识符.ul": b"2020",
    "特殊字符/空行.ul": b"1",
    "特殊字符/小括号.ul": b"4",
    "特殊字符/分号.ul": b"2",

    "引用/引用本地py.ul": b"2",
    "引用/引用本地包内py.ul": b"2",
    "引用/引用本地多py.ul": b"23",
    "引用/引用本地py全部内容.ul": b"32",

    # TODO： 深究 python 中 'from . import *'的含义。参考：
    # https://stackoverflow.com/questions/57774193/what-does-from-dot-import-asterisk-do-in-python-3
    # https://blog.csdn.net/nigelyq/article/details/78930330
    # "引用/引用本地py点.ul": b"2",

    # TODO: 引用 python 标准库, 第三方库
    "引用/引用标准py_math.ul": b"5",
    "引用/引用标准py_random.ul": b"true",

    "引用/引用本地py某内容.ul": b"2",
    "引用/引用木兰.ul": b"2",
    "引用/引用木兰多个.ul": b"21",
    "引用/引用木兰全部内容.ul": b"2",
    "引用/引用木兰某内容.ul": b"2",
    # "引用/引用本地包内木兰.ul": b"1",

    "类型/定义.ul": b"true",
    "类型/定义静态方法.ul": b"1",
    "类型/定义方法.ul": b"1",
    "类型/定义方法self.ul": b"1",
    "类型/定义构造方法.ul": b"1",
    "类型/构造方法原始.ul": b"Mulan",
    "类型/个体属性.ul": b"1",
    "类型/类型属性.ul": b"2",
    "类型/继承.ul": b"1",
    "类型/继承于调用.ul": b"1",
    "类型/操作符/定义操作符.ul": b"31",

    "字符串/双引号.ul": b"okatruetrue",
    "字符串/单引号.ul": b"ok",
    "字符串/相关方法.ul": b"1hi",

    "数据结构/范围.ul": b"range(0, 3)range(0, 3)range(0, 2)range(-1, 5, 2)range(4, -2, -2)02",
    "数据结构/列表.ul": b"[][2][2, 4, 6]",
    "数据结构/列表取值.ul": b"245",
    "数据结构/列表组合.ul": b"['a', 'b', 'b']",
    "数据结构/字典.ul": b"0acfalse",

    "算法/排序/冒泡.ul": b"[1, 2, 4, 5, 8]",
    "算法/排序/插入.ul": b"[1, 2, 4, 5, 8]",
    "算法/排序/快速.ul": b"[1, 2, 4, 5, 8]",

    "综合.ul": b"10",
    #"错误处理/死递归.ul": b"test",
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
    # TODO: 确认报错信息, 现在对语法错误无效
    报错 = 反馈[1]

    if 报错:
        失败表[文件] = 报错
    elif 输出 == 期望值[文件]:
        print("通过： " + 文件)
    # elif 报错 == 期望值[文件]:
    #    print("错误一致: " + 文件)
    else:
        失败表[文件] = 输出

print("===================")
if len(失败表) > 0:
    for 文件 in 失败表:
        print("失败： " + 文件 + " 期望：" + str(期望值[文件]) + " 实际：" + str(失败表[文件]))
else:
    print("！全部通过！")

