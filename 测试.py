#!/usr/bin/env python3

import subprocess

路径 = '测试/'
# 不确定为何输出是bytes：https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
期望值 = {
    "加.ul": b'5',
    "减.ul": b"1",
    "乘.ul": b"6",
    "除整.ul": b"2",
    "除留整.ul": b"1", # TODO: 多行代码
    "四则运算.ul": b"4",
    #"加小数.ul": b"5.0",
    #"除小数.ul": b"2.0",
}

# 多进程参考：https://shuzhanfan.github.io/2017/12/parallel-processing-python-subprocess/
进程表 = {}

# 参考：https://stackoverflow.com/questions/748028/how-to-get-output-of-exe-in-python-script
for 文件 in 期望值:
    进程表[文件] = subprocess.Popen(["./数.py", 路径 + 文件], stdout=subprocess.PIPE)

失败表 = {}

for 文件 in 进程表:
    输出 = 进程表[文件].communicate()[0]
    if 输出 == 期望值[文件]:
        print("通过： " + 文件)
    else:
        失败表[文件] = 输出

print("===================")
if len(失败表) > 0:
    for 文件 in 失败表:
        print("失败： " + 文件 + " 期望：" + str(期望值[文件]) + " 实际：" + str(失败表[文件]))
else:
    print("！全部通过！")

