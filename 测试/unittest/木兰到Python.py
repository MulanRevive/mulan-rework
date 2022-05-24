
from 木兰.生成.python import 代码生成器 as CodegenNow
from 木兰.分析器.词法分析器 import 分词器 as tokenizer
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.分析器.错误 import 语法错误

from os import walk
from os.path import join

from typing import Dict

from json import dump, load as json_load

from subprocess import Popen, PIPE


木兰原始文件执行命令 = 'C:\\ulang-0.2.2.exe --dump-python'


def 生成测试用例json文件():
    cont_dict = {}

    for cur_dir, dirs, files in walk('./源码生成', ):
        for filename in files:
            if filename[-3:] == '.ul':
                p = join(cur_dir, filename)
                with open(p, encoding='UTF-8') as f:
                    cont = f.read()
                    cont_dict[p] = cont

    dump(cont_dict, open('mulan2py/sources.json', 'w'))


def 读取测试用例json() -> Dict[str, str]:
    return json_load(open('mulan2py/sources.json', 'r'))


def 生成当前木兰codegen的测试结果(source_dict: Dict[str, str], 输出log=False):
    结果 = {}

    for 路径, 源码 in source_dict.items():
        if 输出log:
            print('-----------\ngenerating...: %s' % 路径)

        try:
            语法分析器 = 语法分析器(tokenizer)
            节点 = 语法分析器.分析(源码, 路径)
            代码生成器 = CodegenNow()
            源码结果 = 代码生成器.得到源码(节点)
            结果[路径] = 源码结果
            if 输出log:
                print(源码结果)
        except 语法错误 as e:
            if 输出log:
                print(str(e))
    
    dump(结果, open('./mulan2py/codegen_now_result.json', 'w'))
    return 结果


def 生成原始木兰的测试结果(原始木兰执行命令: str, 源码字典: Dict[str, str]):
    结果 = {}

    for 路径, source in 源码字典.items():
        进程 = Popen('%s %s' % (原始木兰执行命令, 路径), stdout=PIPE, stderr=PIPE)
        输出流, 错误输出流 = 进程.communicate()

        print('---generating: %s' % 路径)
        原始木兰输出结果 = 输出流.decode()

        print(原始木兰输出结果, 错误输出流.decode('gbk'))
        
        if 错误输出流.decode('gbk').startswith('SyntaxError') or \
                错误输出流.decode('gbk').startswith('UnicodeDecodeError'):
            continue

        结果[路径] = 原始木兰输出结果

    print('原始木兰输出结果生成完毕!')
    
    dump(结果, open('mulan2py\\original_mulan_result.json', 'w'))
    return 结果


def 比较结果(原始木兰输出结果: Dict[str, str], 
        当前木兰输出结果: Dict[str, str], 源码字典: Dict[str, str]) -> bool:
    
    for 路径 in 源码字典.keys():
        if 路径 in 原始木兰输出结果 and 路径 in 当前木兰输出结果:
            比较的结果 = 原始木兰输出结果[路径] == 当前木兰输出结果[路径]
            print('comparing %s: %s' % (路径, 比较的结果))
            if not 比较的结果:
                print('----original:\n%s' % repr(原始木兰输出结果[路径]))
                print('----now:\n%s' % repr(当前木兰输出结果[路径]))


def _转换Windows路径到Linux路径(result):
    return {x.replace('\\', '/'): v for x, v in result.items()}


def 主函数():
    生成测试用例json文件()
    生成当前木兰codegen的测试结果(读取测试用例json())
    # gen_result_by_original_mulan(ORIGINAL_MULAN_CMD, read_mulan_test_source_json())

    if 1:
        原始木兰输出结果 = json_load(open('mulan2py/original_mulan_result.json', 'r'))
        当前木兰输出结果 = json_load(open('mulan2py/codegen_now_result.json', 'r'))
        测试用例的源码 = 读取测试用例json()

        # original_result = _adopt_origin_result_dict(original_result)

        比较结果(原始木兰输出结果, 当前木兰输出结果, 测试用例的源码)


if __name__ == '__main__':
    主函数()
