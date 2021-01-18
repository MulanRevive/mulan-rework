from 木兰.分析器.语法分析器 import 语法分析器


def 生成语法树(源码):
    分析器 = 语法分析器()
    return 分析器.分析(源码, '')

def 读源码生成树(源码文件):
    with open(源码文件, 'r', encoding='utf-8') as f:
        源码 = f.read()
        return 生成语法树(源码)