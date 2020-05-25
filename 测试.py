#!/usr/bin/env python3

import subprocess

路径 = '测试/'
# 不确定为何输出是bytes：https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
期望值 = {
    # TODO: 整理到不同文件夹, 比如函数相关的一起
    "加.ul": b'5',
    "减.ul": b"1",
    "乘.ul": b"6",
    "除整.ul": b"2",
    "除留整.ul": b"1", # TODO: 多行代码
    "四则运算.ul": b"4",
    "加小数.ul": b"5.0",
    "除小数.ul": b"2.0",
    "多行.ul": b"23", # TODO: 如果末尾加空行, 报错 rply.errors.ParsingError: (None, None)
    "赋值.ul": b"2",
    "赋值两次.ul": b"6",
    "块.ul": b"2",
    "块多行.ul": b"3",
    "空格.ul": b"2",
    "制表符.ul": b"2",
    "条件.ul": b"3",
    "条件否则如果.ul": b"2",
    "条件否则.ul": b"4",
    "条件三段.ul": b"5",
    "条件倒置.ul": b"6",
    "条件否则多行.ul": b"34",
    "比较.ul": b"2222222222222",
    "每当.ul": b"6",
    "循环控制.ul": b"23",
    "函数_无参数.ul": b"2",
    "函数_单参数.ul": b"2",
    "函数_多参数.ul": b"123",
    "函数_多层调用.ul": b"3",
    "返回空.ul": b"2",
    "返回单值.ul": b"2",
    "二阶函数.ul": b"11",
    "缩进.ul": b"2",
    "复杂.ul": b"10",
    "注释块.ul": b"2",
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

