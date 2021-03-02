import ast, re, sys, traceback
from pathlib import Path

from 木兰.分析器.词法分析器 import 分词器
from 木兰.分析器.语法分析器 import 语法分析器

运行时木兰路径 = str(Path("site-packages/木兰/"))

报错_列表索引 = "取列表内容时，索引超出范围"
报错_层级 = "调用层级如下"
报错_除零 = "请勿除以零"
报错_递归 = "递归过深。请确认: 1、的确需要递归 2、递归的收敛正确"
报错_按索引取项 = "不支持按索引取项"
报错_无属性 = "没有属性"
参考_enter = "\n参考：https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit"

def 反馈信息(例外, 源码文件=None):
    提神符 = " 😰 "
    if sys.platform == 'win32':
        提神符 = "（>﹏<）"
    return 提神符 + "\n".join(中文化(例外, 源码文件))

def 中文化(例外, 源码文件=None):
    类型 = 例外.__class__.__name__
    原信息 = str(例外)
    exc_type, exc_value, 回溯信息 = sys.exc_info()
    各层 = traceback.extract_tb(回溯信息)
    # print(repr(各层))
    各行 = []

    行信息 = 提取(各层)
    if len(行信息) > 0:
        关键 = 取关键信息(提示(类型, 原信息), 行信息[0])
    各行.append(关键)
    for 行号, 行 in enumerate(行信息, start=1):
        if 源码文件 is None and 行.文件名 == "【标准输入】":
            return [关键 + f"，见第{行.行号}行"]
        else:
            # 在第二层前显示
            if 行号 == 2:
                各行.append(报错_层级)

            各行.append(("见" if 行.文件名 == 源码文件 else f"“{行.文件名}”") + f"第{行.行号}行：{行.内容}")
    return 各行

class 层信息:
    def __init__(self, 行号, 内容, 文件名):
        self.行号, self.内容, self.文件名 = 行号, 内容, 文件名

def 提取(各层):
    各行 = []
    for 层号 in range(len(各层) - 1, -1, -1):
        层 = 各层[层号]
        文件名 = 层.filename
        if 文件名.find(运行时木兰路径) == -1:
            各行.append(层信息(层.lineno, 层.line, 文件名))

    return 各行

def 取关键信息(基本信息, 首行):
    代码行 = 首行.内容
    问题变量 = []
    try:
        if 基本信息.find(报错_按索引取项) > 0:
            节点 = 语法分析器(分词器).分析(代码行)
            问题变量 = 诊断问题(节点)
        匹配 = re.search("(.*)" + 报错_无属性 + "‘(.*)’", 基本信息)
        if 匹配:
            节点 = 语法分析器(分词器).分析(代码行)

            # TODO: 重构以避免重复匹配
            问题属性 = 匹配.group(2)
            问题变量 = 诊断无属性问题(节点, 问题属性)
    except ValueError:
        return 基本信息

    if len(问题变量) == 0:
        return 基本信息
    elif len(问题变量) == 1:
        return f"{基本信息}，看看‘{问题变量[0]}’"
    else:
        return f"{基本信息}，看看{问题变量}"


def 诊断问题(节点):
    所有变量 = []
    if isinstance(节点, list):
        for 子节点 in 节点:
            所有变量 += 诊断问题(子节点)
    elif isinstance(节点, int) or isinstance(节点, str):
        pass
    else:
        if 节点 == None:
            return
        for 属性 in ast.iter_fields(节点):
            if type(节点).__name__ == "Subscript":
                if 属性[0] == "value":
                    return [属性[1].id]
            所有变量 += 诊断问题(属性[1])
    return 所有变量

def 诊断无属性问题(节点, 问题属性):
    所有变量 = []
    if isinstance(节点, list):
        for 子节点 in 节点:
            所有变量 += 诊断无属性问题(子节点, 问题属性)
    elif isinstance(节点, int) or isinstance(节点, str):
        pass
    else:
        if 节点 == None:
            return
        有问题 = False
        对象名 = ""
        for 属性 in ast.iter_fields(节点):
            if type(节点).__name__ == "Attribute":
                # print(属性[0] + ": " + 属性[1])
                if 属性[0] == "value":
                    对象名 = 属性[1].id
                elif 属性[0] == "attr" and 属性[1] == 问题属性:
                    有问题 = True
            所有变量 += 诊断无属性问题(属性[1], 问题属性)
        if 有问题:
            return [对象名]
    return 所有变量

def 提示(类型, 原信息):
    if 类型 == 'NameError':
        return re.sub(r"name '(.*)' is not defined", r"请先定义‘\1’再使用", 原信息)
    elif 类型 == 'ZeroDivisionError':
        return 报错_除零
    elif 类型 == 'RecursionError':
        return 报错_递归
    elif 类型 == 'UnboundLocalError':
        return re.sub(
            r"local variable '(.*)' referenced before assignment",
            r"请先对本地变量‘\1’赋值再引用",
            原信息)
    elif 类型 == 'KeyError':
        return "字典中不存在此键：" + 原信息
    elif 类型 == 'TypeError':
        模式 = 'can only concatenate str \(not "(.*)"\) to str'
        无法取项 = "'(.*)' object is not subscriptable"
        if re.match(模式, 原信息):
            return re.sub(模式, r'字符串只能拼接字符串，请将“\1”先用 str() 转换', 原信息)
        匹配 = re.search(无法取项, 原信息)
        if 匹配:
            return f'{类型中文化(匹配.group(1))}{报错_按索引取项}'
    elif 类型 == 'IndexError' and 原信息 == "list index out of range":
        return 报错_列表索引
    elif 类型 == 'AttributeError':
        信息 = "需要添加此属性：" + 原信息
        if 原信息 == "__enter__":
            信息 += 参考_enter
            return 信息

        无属性 = "'(.*)' object has no attribute '(.*)'"
        匹配 = re.search(无属性, 原信息)
        if 匹配:
            return f'{类型中文化(匹配.group(1))}{报错_无属性}‘{匹配.group(2)}’'
    elif 类型 == 'FileNotFoundError':
        return re.sub(r"\[Errno 2\] No such file or directory: '(.*)'",
            r"没找到文件或路径：‘\1’",
            原信息)
    elif 类型 == 'ModuleNotFoundError':
        return re.sub(r"No module named '(.*)'", r"没找到模块：‘\1’", 原信息)
    return 类型 + "：" + 原信息

def 类型中文化(类型):
    中英表 = {
        "NoneType": "空变量",
        "int": "整数变量",
        "bool": "真假变量",
        "function": "函数",
    }
    return 中英表[类型] if 类型 in 中英表 else 类型
