import ast, sys
from io import StringIO
from pathlib import Path

from 木兰.分析器.词法分析器 import 分词器
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.环境 import 创建全局变量
from 木兰.交互 import 开始交互
from 木兰.功用.反馈信息 import 中文化
from 木兰.功用.调试辅助 import 语法树相关

# 木兰不支持 compile, exec, 因此不改写为木兰代码
def 运行木兰代码(源码文件):
    with open(源码文件, 'r', encoding='utf-8') as f:
        源码 = f.read()

    分析器 = 语法分析器(分词器)
    节点 = 分析器.分析(源码, 源码文件)

    # 参考： https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement
    原标准输出 = sys.stdout

    # 默认换行符为 \n，见 https://docs.python.org/zh-cn/3.7/library/io.html#io.StringIO
    重定向输出 = sys.stdout = StringIO()

    # 参考：https://docs.python.org/3.7/library/functions.html?highlight=compile#compile
    try:
        可执行码 = compile(节点, 源码文件, 'exec')

        环境变量 = 创建全局变量(文件名=源码文件)

        try:
            exec(可执行码, 环境变量)
        except Exception as e:
            return 中文化(e, 源码文件)
    except SyntaxError as 语法错误:
        return f"语法错误: {语法错误}\n"
    finally:
        sys.stdout = 原标准输出

    return 重定向输出.getvalue()
