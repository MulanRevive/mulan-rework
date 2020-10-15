#!/usr/bin/env python3

import subprocess

from sys import platform

# TODO: 合并 test语法树

路径 = '测试/'
# 不确定为何输出是bytes：https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
期望值 = {
    "运算/加.ul": b'5',
    "运算/减.ul": b"1",
    "运算/乘.ul": b"6181",
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
    "运算/赋值多项.ul": b"2112",
    "运算/其他.ul": b"8",

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
    "流程控制/循环for.ul": b"0120120212301251a2b",
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
    "函数/匿名函数.ul": b"[1][1][3][3][1, 4]12true",
    "函数/API/内置.ul": b"truefalsea[1]20",
    "函数/API/文件.ul": b"hi",
    "函数/API/self.ul": b"true",
    "函数/形参默认值.ul": b"2",
    "函数/指名参数.ul": b"466",
    "函数/指定返回类型.ul": b"Mulan1",
    # "函数/变长参数.ul": b"1 2 3",

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
    "特殊字符/美元.ul": b"566787",

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
    "引用/引用木兰多个.ul": b"21",
    "引用/引用木兰全部内容.ul": b"2",
    "引用/引用本地包内木兰.ul": b"2",
    "引用/引用本地包内木兰某内容.ul": b"2",

    "类型/定义.ul": b"true",
    "类型/定义静态方法.ul": b"1",
    "类型/定义方法.ul": b"1",
    "类型/定义方法self.ul": b"11",
    "类型/定义构造方法.ul": b"1",
    "类型/构造方法原始.ul": b"Mulan",
    "类型/个体属性.ul": b"111",
    "类型/类型属性.ul": b"2",
    "类型/应变属性.ul": b"343",
    "类型/继承.ul": b"1",
    "类型/继承于调用.ul": b"1",
    "类型/操作符/定义操作符.ul": b"31true",

    "字符串/双引号.ul": b"okatruetrue",
    "字符串/单引号.ul": b"ok",
    "字符串/相关方法.ul": b"1hi[fish]",
    "字符串/插值.ul": b"b3b3o44ta3a44t`a3a",

    "数据结构/范围.ul": b"range(0, 3)range(0, 3)range(0, 2)range(-1, 5, 2)range(4, -2, -2)02",
    "数据结构/列表.ul": b"[][2][2, 4, 6]",
    "数据结构/列表取值.ul": b"245[1, 4][3, 5][1, 4][1, 4, 3, 5]",
    "数据结构/列表组合.ul": b"[a, b, b]",
    "数据结构/字典.ul": b"0acfalsefalse",
    "数据结构/集合.ul": b"{1, 2, 3}",
    "数据结构/多项.ul": b"1, 2, 3",

    "算法/排序/冒泡.ul": b"[1, 2, 4, 5, 8]",
    "算法/排序/插入.ul": b"[1, 2, 4, 5, 8]",
    "算法/排序/快速.ul": b"[1, 2, 4, 5, 8]",

    "综合.ul": b"10",
    #"错误处理/死递归.ul": b"test",
}

# 多进程参考：https://shuzhanfan.github.io/2017/12/parallel-processing-python-subprocess/
进程表 = {}

英文版 = set(["运算/乘.ul",
    "函数/过滤.ul", "函数/map.ul", "函数/返回多值.ul", "函数/匿名函数.ul", "函数/API/文件.ul",
    "特殊字符/注释块.ul",
    "类型/继承.ul", "类型/个体属性.ul", "类型/定义方法self.ul",
    "字符串/双引号.ul", "字符串/相关方法.ul",
    "数据结构/列表取值.ul",
    "引用/引用木兰多个.ul", "引用/引用本地包内木兰.ul", "引用/引用本地包内木兰某内容.ul",
    "算法/排序/冒泡.ul", "算法/排序/插入.ul", "算法/排序/快速.ul",
    "综合.ul"])
# 参考：https://stackoverflow.com/questions/748028/how-to-get-output-of-exe-in-python-script
for 文件 in 期望值:
    源码路径 = 路径 + 文件
    if platform == 'win32':
        # https://stackoverflow.com/questions/25651990/oserror-winerror-193-1-is-not-a-valid-win32-application
        参数 = ["python.exe", "中.py", 源码路径]

        # 原始可执行文件在：https://gitee.com/MulanRevive/bounty/tree/master/%E5%8E%9F%E5%A7%8B%E8%B5%84%E6%96%99/%E5%8F%AF%E6%89%A7%E8%A1%8C%E6%96%87%E4%BB%B6/ulang-0.2.2.exe
        # 原始版本不支持中文标识符，且仅支持 gbk 编码的源文件。因此英文版测试文件仅用英文字符串和标识符。
        # 在验证与原始版本功能一致时，将可执行文件拷贝到项目根目录，手动打开下面这段。
        # if 文件 in 英文版:
        #     源码路径 = 源码路径[:-3] + "_en.ul"
        # if 文件 == "特殊字符/中文标识符.ul":
        #     continue
        # 参数 = ["ulang-0.2.2.exe",  源码路径]
    else:
        参数 = ["python3", "-m", "木兰", 源码路径]
    进程表[文件] = subprocess.Popen(参数, stdout=subprocess.PIPE)

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
        print(f"失败： {文件} 期望：{期望值[文件]} 实际：{失败表[文件]}")
else:
    print("！全部通过！")

