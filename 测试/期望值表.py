from sys import platform
import datetime

为win系统 = platform == 'win32'

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
    "运算/一元操作.ul": b"2-1-2",
    "运算/赋值多项.ul": b"2112123",
    "运算/其他.ul": b"82",
    "运算/综合.ul": b"10",

    # TODO: 加上 `(2<1)!=nil and`
    "运算/空.ul": b"truetrue",

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
    "流程控制/try.ul": b"030",
    "流程控制/catch.ul": b"vi",
    "流程控制/catch名称.ul": b"list index out of range",

    "函数/无参数.ul": b"223", # 最后无4是因为返回了函数, 而非它的返回值
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
    "函数/API/内置.ul": (
        "truefalsea[1]200 a1 b2 ctruefalse32b'ab'12.55cba{{}}true1.1a 149int211.02.00.01.0"
        "2.718281828459045"  # exp(1)
        "729.0"  # pow(9, 3)
        # 不同 python3.7小版本的值不同，如 3.7.9 cos(1) 0.5403023058681397 3.7.4 为 0.5403023058681398。因此使用特殊角度规避
        "sin(0):0.0"
        "cos(0):1.0"
        "tan(0):0.0"
        "asin(0):0.0"
        "acos(1):0.0"
        "atan(0):0.0"
        "16"  # str(time())[:2]
        "a"  # spawn
        ""   # kill
        "{}"  # year
        "{}"  # month
        "{}"  # day
        "{}"  # hour
        # 当原始可执行文件运行测试时间过长，常导致开始测试时刻的分钟数值与运行到此测试的分钟数值不同
        "function"  # typeof(minute)
        "function"  # typeof(second)
        "function"  # typeof(microsecond)
        "3.141592653589793"  # PI
    ).format(
        datetime.datetime.now().year,
        datetime.datetime.now().month,
        datetime.datetime.now().day,
        datetime.datetime.now().hour,
    ).encode(),
    "函数/API/文件.ul": b"hi",
    "函数/API/self.ul": b"true",
    "函数/API/file.ul": b"true",
    "函数/形参默认值.ul": b"2",
    "函数/指名参数.ul": b"466",
    "函数/指定返回类型.ul": b"Mulan1",
    "函数/指定形参类型.ul": b"hi Mulan1",
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

    "引用/枚举/b.ul": b"T.Xfalsetrue",
    "引用/外部/修改成功.ul": b"13",
    "引用/外部/修改失败.ul": b"11",

    "引用/isa/先引用包内类型.ul": b"false",
    "引用/isa/后引用包内类型.ul": b"true",
    "引用/isa/先引用类型.ul": b"true",
    "引用/isa/后引用类型.ul": b"false",
    "引用/isa/先引用类型_绝对路径.ul": b"false",
    "引用/isa/后引用类型_绝对路径.ul": b"false",
    "引用/isa/先引用包内类型_绝对路径.ul": b"false",
    "引用/isa/后引用包内类型_绝对路径.ul": b"false",

    "类型/定义.ul": b"true",
    "类型/定义静态方法.ul": b"11",
    "类型/定义方法.ul": b"1",
    "类型/定义方法self.ul": b"11",
    "类型/定义构造方法.ul": b"1",
    "类型/构造方法原始.ul": b"Mulan",
    "类型/个体属性.ul": b"111",
    "类型/类型属性.ul": b"2[2]",
    "类型/应变属性.ul": b"343",
    "类型/继承.ul": b"1",
    "类型/继承于调用.ul": b"1",
    "类型/操作符/定义操作符.ul": b"31true",
    "类型/超类.ul": b"animalwowo",
    "类型/返回值属性.ul": b"ok",

    "字符串/双引号.ul": b'ok\n\t\\"\\natruetruecc',
    "字符串/单引号.ul": b"ok\n\t\\'\\n",
    "字符串/相关方法.ul": b"1hi[fish]",
    "字符串/插值.ul": b"b3b3o44ta3a44t`a3a",

    "数据结构/范围.ul": b"range(0, 3)range(0, 3)range(0, 2)range(-1, 5, 2)range(4, -2, -2)02",
    "数据结构/列表.ul": b"[][2][2, 4, 6][[1], [2]]",
    "数据结构/列表取值.ul": b"245[1, 4][3, 5][1, 4][1, 4, 3, 5]",
    "数据结构/列表组合.ul": b"[a, b, b][0, 0]",
    "数据结构/字典.ul": b"0acfalsefalse1a1b21",
    "数据结构/集合.ul": b"{1, 2, 3}",
    "数据结构/多项.ul": b"1, 2, 3",
    "数据结构/枚举.ul": b"12",
    "数据结构/标识符.ul": b"36",

    "算法/排序/冒泡.ul": b"[1, 2, 4, 5, 8]",
    "算法/排序/插入.ul": b"[1, 2, 4, 5, 8]",
    "算法/排序/快速.ul": b"[1, 2, 4, 5, 8]",
}
