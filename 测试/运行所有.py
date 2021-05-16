#!/usr/bin/env python3

import shutil
import subprocess

from 期望值表 import *

# 原始可执行文件在：https://gitee.com/MulanRevive/bounty/tree/master/%E5%8E%9F%E5%A7%8B%E8%B5%84%E6%96%99/%E5%8F%AF%E6%89%A7%E8%A1%8C%E6%96%87%E4%BB%B6/ulang-0.2.2.exe
# 原始版本不支持中文标识符，且仅支持 gbk 编码的源文件。因此英文版测试文件仅用英文字符串和标识符。

路径 = '测试/'
# 不确定为何输出是bytes：https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal

# 多进程参考：https://shuzhanfan.github.io/2017/12/parallel-processing-python-subprocess/
进程表 = {}
原始可执行文件 = "ulang-0.2.2.exe"
木兰重现 = "木兰"

可执行文件 = 原始可执行文件 if 为win系统 else 木兰重现

if shutil.which(可执行文件) is None:
    print("运行测试需安装'" + 可执行文件 + "'")
    exit()

英文版 = set(["运算/乘.ul",
    "函数/过滤.ul", "函数/map.ul", "函数/返回多值.ul", "函数/匿名函数.ul", "函数/API/文件.ul",
    "特殊字符/注释块.ul",
    "类型/继承.ul", "类型/个体属性.ul", "类型/定义方法self.ul",
    "字符串/双引号.ul", "字符串/相关方法.ul",
    "数据结构/列表取值.ul", "数据结构/枚举.ul",
    "引用/引用木兰多个.ul", "引用/引用本地包内木兰.ul", "引用/引用本地包内木兰某内容.ul",
    "算法/排序/冒泡.ul", "算法/排序/插入.ul", "算法/排序/快速.ul",
    "运算/综合.ul"])
if 为win系统:
    期望值["字符串/双引号.ul"] = b'ok\r\n\t\\"\\natruetruecc'
    期望值["字符串/单引号.ul"] = b"ok\r\n\t\\'\\n"

# 参考：https://stackoverflow.com/questions/748028/how-to-get-output-of-exe-in-python-script
for 文件 in 期望值:
    源码路径 = 路径 + 文件
    if 为win系统:
        if 文件 in 英文版:
            源码路径 = 源码路径[:-3] + "_en.ul"
        if 文件 == "特殊字符/中文标识符.ul":
            continue

    参数 = [可执行文件, 源码路径]
    进程表[文件] = subprocess.Popen(参数, stdout=subprocess.PIPE)

失败表 = {}

for 文件 in 进程表:
    反馈 = 进程表[文件].communicate()
    输出 = 反馈[0]
    # TODO: 确认报错信息, 现在对语法错误无效
    报错 = 反馈[1]

    预期值 = 期望值[文件]
    if 报错:
        失败表[文件] = 报错
    elif 输出 == 预期值:
        print("通过： " + 文件)
    # elif 报错 == 期望值[文件]:
    #    print("错误一致: " + 文件)
    else:
        失败表[文件] = 输出

print("===================")
if len(失败表) > 0:
    for 文件 in 失败表:
        print(f"失败： {文件} 期望：{预期值} 实际：{失败表[文件]}")
else:
    print("！全部通过！")

print("本测试针对木兰原始可执行文件与重现项目的发布版。在此之前先运行`测试/unittest`下的集成测试。")
