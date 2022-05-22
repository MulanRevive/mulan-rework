
from 木兰.生成.python import 代码生成器 as CodegenNow
from 木兰.分析器.词法分析器 import 分词器 as tokenizer
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.分析器.错误 import 语法错误

from os import walk
from os.path import join

from typing import Dict

from json import dump, load as json_load

from subprocess import Popen, PIPE


ORIGINAL_MULAN_CMD = 'C:\\C:\\ulang-0.2.2.exe --dump-python'


def make_all_ul_source_json():
    cont_dict = {}

    for cur_dir, dirs, files in walk('./源码生成', ):
        for filename in files:
            if filename[-3:] == '.ul':
                p = join(cur_dir, filename)
                with open(p) as f:
                    cont = f.read()
                    cont_dict[p] = cont

    dump(cont_dict, open('mulan2py/sources.json', 'w'))


def read_mulan_test_source_json() -> Dict[str, str]:
    return json_load(open('mulan2py/sources.json', 'r'))


def gen_result_by_mulan_now_codegen(source_dict: Dict[str, str], output=False):
    result_dict = {}

    for path, source in source_dict.items():

        print('-----------\ngenerating...: %s' % path)

        try:
            parser = 语法分析器(tokenizer)
            node = parser.分析(source, path)
            codegen = CodegenNow()
            result = codegen.得到源码(node)
            result_dict[path] = result
            if output:
                print(result)
        except 语法错误 as e:
            print(str(e))
    
    dump(result_dict, open('./mulan2py/codegen_now_result.json', 'w'))
    return result_dict


def gen_result_by_original_mulan(mulan_cmd: str, source_dict: Dict[str, str]):
    result_dict = {}

    for path, source in source_dict.items():
        proc = Popen('%s %s' % (mulan_cmd, path), stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()

        print('---generating: %s' % path)
        result = out.decode()

        print(result, err.decode('gbk'))
        
        if err.decode('gbk').startswith('SyntaxError'):
            continue

        result_dict[path] = result

    print('generation finished!')
    
    dump(result_dict, open('mulan2py\\original_mulan_result.json', 'w'))
    return result_dict


def compare(original_result: Dict[str, str], 
        now_result: Dict[str, str], source_dict: Dict[str, str]) -> bool:
    
    for path in source_dict.keys():
        if path in original_result and path in now_result:
            res = original_result[path] == now_result[path]
            print('comparing %s: %s' % (path, res))
            if not res:
                print('----original:\n%s' % repr(original_result[path]))
                print('----now:\n%s' % repr(now_result[path]))
            

def main():
    gen_result_by_mulan_now_codegen(read_mulan_test_source_json())
    # gen_result_by_original_mulan(ORIGINAL_MULAN_CMD, read_mulan_test_source_json())

    if 1:
        original_result = json_load(open('mulan2py\\original_mulan_result.json', 'r'))
        now_result = json_load(open('mulan2py\\codegen_now_result.json', 'r'))
        source_dict = read_mulan_test_source_json()

        compare(original_result, now_result, source_dict)


if __name__ == '__main__':
    main()
