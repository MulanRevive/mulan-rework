import math, sys

def __内置_除(a, b):
    if isinstance(a, int):
        if isinstance(b, int):
            return math.floor(a / b)
    return a / b

def 创建全局变量():

    def 转字符串(x):
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

    return {
        'print': 自定义输出,
        '__div__': __内置_除
    }