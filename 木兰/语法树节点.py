import ast
from 木兰.共享 import python3版本号


def 节点为字符串(节点):
    if python3版本号 <= 7:
        return isinstance(节点, ast.Str)
    return isinstance(节点, ast.Constant) and isinstance(节点.value, str)


def 节点为真假值(节点):
    if python3版本号 <= 7:
        return isinstance(节点, ast.NameConstant) and isinstance(节点.value, bool)
    return isinstance(节点, ast.Constant) and isinstance(节点.value, bool)


def 节点为空(节点):
    if python3版本号 <= 7:
        return isinstance(节点, ast.NameConstant) and 节点.value is None
    return isinstance(节点, ast.Constant) and 节点.value is None


def 节点为数字(节点):
    if 节点为真假值(节点):
        return False
    if python3版本号 <= 7:
        return isinstance(节点, ast.Num)
    return isinstance(节点, ast.Constant) and isinstance(节点.value, (int, float))
