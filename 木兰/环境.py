import imp
import math
import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

from 木兰.分析器.语法分析器 import 语法分析器

# 参考：https://docs.python.org/3.7/library/threading.html#thread-objects
class 线程(threading.Thread):
    """
    跟踪线程包装器。
    """

    def __init__(自身, *args, **kw):
        threading.Thread.__init__(自身, *args, **kw)
        自身.已亡 = False

    def start(自身):
        自身._线程__运行_backup = 自身.run
        自身.run = 自身._线程__运行
        threading.Thread.start(自身)

    def __运行(自身):
        sys.settrace(自身.全局跟踪)
        自身._线程__运行_backup()
        自身.run = 自身._线程__运行_backup

    def 全局跟踪(自身, 栈, 事件, 参数):
        if 事件 == 'call':
            return 自身.本地跟踪
        return

    def 本地跟踪(自身, 栈, 事件, 参数):
        if 自身.已亡:
            if 事件 == 'line':
                raise SystemExit
        return 自身.本地跟踪

    def 杀死(自身):
        自身.已亡 = True


def 分析并编译(源码文件名):
    with open(源码文件名, 'r', encoding='utf-8') as 文件:
        源码 = 文件.read()

        分析器 = 语法分析器()
        节点 = 分析器.分析(源码=源码, 源码文件=源码文件名)
        return compile(节点, 源码文件名, 'exec')


def 加载木兰模块(名称, 全局, 源自=(), 目录相对层次=0):
    木兰源码路径 = str(Path(*(名称.split(".")))) + '.ul'
    可执行码 = 分析并编译(木兰源码路径)
    if 可执行码 is None:
        raise ModuleNotFoundError(名称)

    # TODO: 研究何用
    所有模块 = []
    后段 = 名称
    模块名 = lambda 模块名称: 所有模块[-1].__name__ + '.' + 模块名称 if 所有模块 else ""

    点位 = 0
    while 点位 != -1:
        点位 = 后段.find('.')
        前段, 后段 = 后段[:点位], 后段[点位 + 1:]
        if 点位 == -1:
            前段 = 后段
            模块 = imp.new_module(模块名(后段))
            模块.__dict__.update(创建全局变量(argv=(全局['ARGV'])))
            模块.__dict__['__file__'] = os.path.abspath(木兰源码路径)
            exec(可执行码, 模块.__dict__)
        else:
            模块 = imp.new_module(模块名(前段))
        if 所有模块:
            所有模块[-1].__dict__[前段] = 模块
        所有模块.append(模块)

    顶层 = 所有模块[0]
    if len(所有模块) > 1:
        if 源自 is not None:
            for sym in 源自:
                if sym == '*':
                    for k in 模块.__dict__:
                        if k not in 全局:
                            顶层.__dict__[k] = 模块.__dict__[k]
                    break
                else:
                    顶层.__dict__[sym] = 模块.__dict__[sym]

    return 顶层


def 内置扩展(内置项):
    from inspect import isclass
    for k, v in __builtins__.items():
        if isclass(v) and issubclass(v, BaseException):
            内置项[k] = v

    return 内置项


def __内置_除(a, b):
    if isinstance(a, int):
        if isinstance(b, int):
            return math.floor(a / b)
    return a / b


def __内置_求余(a, b):
    # TODO: 不解为何要在 a b 为整数时特殊处理
    return a % b


def 创建全局变量(argv=[], 文件名=''):
    def 转字符串(x):

        def 容器转为字符串(容器, 始='', 末=''):
            字符串 = 始
            for 序号, 该项 in enumerate(容器):
                if 序号:
                    字符串 += ', '
                字符串 += 转字符串(该项)

            字符串 += 末
            return 字符串

        if x is None:
            return 'nil'
        if isinstance(x, bool):
            return 'true' if x else 'false'
        if isinstance(x, list):
            return 容器转为字符串(x, '[', ']')
        if isinstance(x, tuple):
            return 容器转为字符串(x)
        return str(x)

    def 自定义输出(*各物件, 分隔符=' ', 终止符='', 文件=sys.stdout, flush=False):
        """打印内容到流, 默认到标准输出."""
        for 物件 in 各物件:
            文件.write(转字符串(物件))
            if 物件 != 各物件[(-1)]:
                文件.write(分隔符)

        文件.write(终止符)
        if flush:
            文件.flush()

    def 自定义导入(名称, 全局=None, 本地=None, 源自=(), 目录相对层次=0):
        """导入一个木兰模块, 如果没找到, 则导入 Python 模块
        """
        try:
            return 加载木兰模块(名称, 全局, 源自, 目录相对层次)
        except FileNotFoundError:
            return __import__(名称, 全局, 本地, 源自, 目录相对层次)
        except Exception as 例外:
            raise 例外

    def 本地断言(表达式, 反馈=None):
        assert 表达式, 反馈

    def 内置自身():
        """ 当前任务 ID """
        return threading.currentThread()

    def 生成新任务(任务名, *参数列表):

        # 待研究：各参数作用
        私有线程 = 线程(target=任务名, args=参数列表, daemon=True)
        私有线程.start()
        return 私有线程

    def 杀死任务(任务线程):
        if isinstance(任务线程, 线程):
            if 任务线程 == threading.currentThread():
                sys.exit()
            elif 任务线程.is_alive():
                任务线程.杀死()

    def 用pip安装(*包, 命令='install'):
        import pip._internal
        return pip._internal.main([命令, *包])

    def eval_print(expr):
        if expr is None:
            return
        try:
            expr()
        except Exception:
            自定义输出(expr, 终止符='\n')

    当前目录 = os.getcwd()
    if 当前目录 not in sys.path:
        sys.path.append(当前目录)
    return {
        'print': 自定义输出,
        'println': lambda *各物件: 自定义输出(*各物件, **{'终止符': '\n'}),
        'assert': 本地断言,
        'len': len,
        'enumerate': enumerate,
        'all': all,
        'any': any,
        'range': range,
        'round': round,
        'input': input,
        'reverse': reversed,
        'super': super,
        'locals': lambda: locals(),
        'bool': bool,
        'float': float,
        'int': int,
        'str': str,
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': lambda *各实参: 各实参,
        'char': chr,
        'ord': ord,
        'bytes': lambda 文本, 编码='ascii': bytes(文本, encoding=编码),
        'typeof': lambda 对象: 对象.__class__.__name__,
        'isa': lambda x, 类型: isinstance(x, 类型),
        'max': max,
        'min': min,
        'map': map,
        'filter': filter,
        'zip': zip,
        'staticmethod': staticmethod,
        'property': property,
        'ceil': math.ceil,
        'floor': math.floor,
        'fabs': math.fabs,
        'sqrt': math.sqrt,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'pow': math.pow,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'spawn': 生成新任务,
        'kill': 杀死任务,
        'self': 内置自身,
        '再会': sys.exit,
        'quit': sys.exit,
        'open': open,
        'install': 用pip安装,
        'time': time.time,
        'year': lambda: datetime.now().year,
        'month': lambda: datetime.now().month,
        'day': lambda: datetime.now().day,
        'hour': lambda: datetime.now().hour,
        'minute': lambda: datetime.now().minute,
        'second': lambda: datetime.now().second,
        'microsecond': lambda: datetime.now().microsecond,
        'sleep': time.sleep,
        'delay': lambda 毫秒数: time.sleep(毫秒数 / 1000),
        'delayMicroseconds': lambda 微秒数: time.sleep(微秒数 / 1000000),
        'PI': math.pi,
        'ARGV': argv,
        '__builtins__': 内置扩展({
            '__import__': 自定义导入,
            '__build_class__': __build_class__,
            '__name__': '__main__',
            '__file__': 文件名,
            '__print__': eval_print,
            '__div__': __内置_除,
            '__rem__': __内置_求余})
    }
