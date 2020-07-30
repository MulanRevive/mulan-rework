import math, sys, imp, os
from 分析器.语法分析器 import 语法分析器


def 分析并编译(源码文件名):
    with open(源码文件名, 'r') as 文件:
        源码 = 文件.read()

        分析器 = 语法分析器()
        节点 = 分析器.分析(源码=源码, 源码文件=源码文件名)
        return compile(节点, 源码文件名, 'exec')

def 加载木兰模块(名称, 全局, 源自=(), 目录相对层次=0):
    木兰源码路径 = 名称.replace('.', '/') + '.ul'
    if sys.platform == 'win32':
        木兰源码路径 = 木兰源码路径.replace('/', '\\')
    可执行码 = 分析并编译(木兰源码路径)
    if 可执行码 is None:
        raise ModuleNotFoundError(名称)

    模块 = imp.new_module(名称)

    # TODO: 研究何用
    模块.__dict__.update(创建全局变量(argv=(全局['ARGV'])))
    模块.__dict__['__file__'] = os.path.abspath(木兰源码路径)
    exec(可执行码, 模块.__dict__)

    return 模块

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

def 创建全局变量(argv=[]):

    def 转字符串(x):
        if x is None:
            return 'nil'
        if isinstance(x, bool):
            return 'true' if x else 'false'
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
        except:
            return __import__(名称, 全局, 本地, 源自, 目录相对层次)

    def 本地断言(表达式, 反馈=None):
        assert 表达式, 反馈

    return {
        'print': 自定义输出,
        'println': lambda *各物件: 自定义输出(*各物件, **{'终止符': '\n'}),
        'assert': 本地断言,
        'len': len,
        'any':any,
        'range': range,
        'list': list,
        'set': set,
        'map': map,
        'filter': filter,
        'staticmethod': staticmethod,
        'open':open,
        'ARGV': argv,
        '__builtins__': 内置扩展({
            '__import__': 自定义导入,
            '__build_class__': __build_class__,
            '__name__': '__main__',
            '__div__': __内置_除})
    }