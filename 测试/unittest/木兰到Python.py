
from 木兰.生成.python import 代码生成器 as CodegenNow
from 木兰.分析器.词法分析器 import 分词器 as tokenizer
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.分析器.错误 import 语法错误

from os import walk
from os.path import join

from typing import Dict
from json import dump, load as json_load
from subprocess import Popen, PIPE
from unittest import TestCase


木兰原始文件执行命令 = 'ulang-0.2.2.exe --dump-python'

原始木兰无法运行 = (
    'signature.ul'
)


def 生成测试用例json文件():
    cont_dict = {}

    for cur_dir, dirs, files in walk('测试/unittest/源码生成/木兰到Python', ):
        for filename in files:
            if filename[-3:] == '.ul' and '失效' not in filename:
                p = join(cur_dir, filename)
                print('loading %s...' % p)
                with open(p,) as f:
                    cont = f.read()
                    cont_dict[p] = cont

    dump(cont_dict, open('测试/unittest/sources.json', 'w'))


def 读取测试用例json() -> Dict[str, str]:
    with open('测试/unittest/sources.json', 'r') as f:
        return json_load(f)


def 生成当前木兰codegen的测试结果(source_dict: Dict[str, str], 输出log=False):
    结果 = {}

    for 路径, 源码 in source_dict.items():
        if 输出log:
            print('-----------\ngenerating...: %s' % 路径)

        try:
            语法分析器_ = 语法分析器(tokenizer)
            节点 = 语法分析器_.分析(源码, 路径)
            代码生成器 = CodegenNow()
            源码结果 = 代码生成器.得到源码(节点)
            结果[路径] = 源码结果
            if 输出log:
                print(源码结果)
        except 语法错误 as e:
            print(str(e))

    with open('测试/unittest/codegen_now_result.json', 'w') as f:
        dump(结果, f)
    return 结果


def 生成原始木兰的测试结果(原始木兰执行命令: str, 源码字典: Dict[str, str]):
    结果 = {}

    计数 = 0
    源码字典长度 = len(源码字典)

    print('得到原始木兰生成结果中...')

    for 路径, source in 源码字典.items():
        进程 = Popen('%s %s' % (原始木兰执行命令, 路径), stdout=PIPE, stderr=PIPE)
        输出流, 错误输出流 = 进程.communicate()

        # print('---generating: %s' % 路径)
        原始木兰输出结果 = 输出流.decode()

        # print(原始木兰输出结果, 错误输出流.decode('gbk'))
        
        if 错误输出流.decode('gbk').startswith('SyntaxError') or \
                错误输出流.decode('gbk').startswith('UnicodeDecodeError'):
            continue

        结果[路径] = 原始木兰输出结果.replace('\r\n', '\n')[:-1]  # 除去末尾因为popen读取而导致的 \n

        print('\r进度: （%s/%s）' % (计数, 源码字典长度), end='')

    # print('原始木兰输出结果生成完毕!')
    print()  # 换行
    
    with open('测试/unittest/original_mulan_result.json', 'w') as f:
        dump(结果, f)
    return 结果


def _转换Windows路径到Linux路径(result):
    return {x.replace('\\', '/'): v for x, v in result.items()}


class 木兰到Python测试(TestCase):
    def test(self):
        生成测试用例json文件()
        生成当前木兰codegen的测试结果(读取测试用例json())
        生成原始木兰的测试结果(木兰原始文件执行命令, 读取测试用例json())

        with open('测试/unittest/original_mulan_result.json', 'r') as f:
            原始木兰输出结果 = json_load(f)
        with open('测试/unittest/codegen_now_result.json', 'r') as f:
            当前木兰输出结果 = json_load(f)
        源码字典 = 读取测试用例json()

        # original_result = _adopt_origin_result_dict(original_result)

        for 路径 in 源码字典.keys():
            if 路径 in 原始木兰输出结果 and 路径 in 当前木兰输出结果:
                print('comparing %s' % 路径)
                self.assertEqual(
                    原始木兰输出结果[路径], 当前木兰输出结果[路径], "输出与原始木兰不一致：\n%s%s" % 
                        ('----original:\n%s' % repr(原始木兰输出结果[路径]),
                         '----now:\n%s' % repr(当前木兰输出结果[路径]),
                        ))
