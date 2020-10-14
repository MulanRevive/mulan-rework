import ast

class 语法树相关:

    def 格式化节点(节点, 层次):
        缩进 = "  "
        输出 = ""
        if isinstance(节点, list):
            输出 += "["
            for 子节点 in 节点:
                输出 += 语法树相关.格式化节点(子节点, 层次 + 1)
            输出 += "]"
        elif isinstance(节点, int):
            输出 += str(节点)
        elif isinstance(节点, str):
            输出 += "'" + 节点 + "'"
        else:
            if 节点 == None:
              return 输出 + "None"
            输出 += type(节点).__name__ + "("
            属性个数 = 0
            for 属性 in ast.iter_fields(节点):
                属性个数 += 1
                输出 += "\n" + 缩进 * 层次 + 属性[0] + "="
                输出 += 语法树相关.格式化节点(属性[1], 层次 + 1)
            if isinstance(节点, ast.stmt) or isinstance(节点, ast.expr):
                输出 += f"\n{缩进 * 层次}lineno={节点.lineno}"
                输出 += f"\n{缩进 * 层次}col_offset={节点.col_offset}"
            if 属性个数 == 0:
                return 输出 + ")"
            return 输出 + "\n" + 缩进 * (层次 - 1) + ")"
        return 输出

'''
TODO:
如果class的decorator_list为空(无NameFixPass), 则报错:
Traceback (most recent call last):
  File "./中.py", line 26, in <module>
    print(语法树相关.格式化节点(节点, 1))
  File "/Users/xuanwu/work/木兰/prototype/功用.py", line 23, in 格式化节点
    输出 += 语法树相关.格式化节点(属性[1], 层次 + 1)
  File "/Users/xuanwu/work/木兰/prototype/功用.py", line 11, in 格式化节点
    输出 += 语法树相关.格式化节点(子节点, 层次 + 1)
  File "/Users/xuanwu/work/木兰/prototype/功用.py", line 23, in 格式化节点
    输出 += 语法树相关.格式化节点(属性[1], 层次 + 1)
  File "/Users/xuanwu/work/木兰/prototype/功用.py", line 11, in 格式化节点
    输出 += 语法树相关.格式化节点(子节点, 层次 + 1)
  File "/Users/xuanwu/work/木兰/prototype/功用.py", line 23, in 格式化节点
    输出 += 语法树相关.格式化节点(属性[1], 层次 + 1)
  File "/Users/xuanwu/work/木兰/prototype/功用.py", line 23, in 格式化节点
    输出 += 语法树相关.格式化节点(属性[1], 层次 + 1)
  File "/Users/xuanwu/work/木兰/prototype/功用.py", line 20, in 格式化节点
    for 属性 in ast.iter_fields(节点):
  File "/opt/miniconda3/lib/python3.7/ast.py", line 177, in iter_fields
    for field in node._fields:
AttributeError: 'NoneType' object has no attribute '_fields'
'''