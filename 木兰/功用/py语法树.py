import ast
from 木兰.功用.调试辅助 import 语法树相关

with open('测试/流程控制/except.py', 'r', encoding='utf-8') as f:
    源码 = f.read()

print(语法树相关.格式化节点(ast.parse(源码), 1))
