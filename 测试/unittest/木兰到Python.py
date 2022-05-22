
from 木兰.生成.python import 代码生成器 as CodegenNow
from 木兰.分析器.词法分析器 import 分词器 as tokenizer
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.分析器.错误 import 语法错误

from os import walk
from os.path import join

from typing import Dict

from json import dump, load as json_load


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


def gen_result_by_mulan_now_codegen(source_dict: Dict[str, str]):
    codegen = CodegenNow('    ')
    result_dict = {}

    for path, source in source_dict.items():

        print('-----------\ngenerating...: %s' % path)

        try:
            parser = 语法分析器(tokenizer)
            node = parser.分析(source, path)
            result = codegen.得到源码(node)
            result_dict[path] = result
            print(result)
        except 语法错误 as e:
            print(str(e))
    
    dump(result_dict, open('./mulan2py/codegen_now_result.json', 'w'))
    return result_dict


def main():
    gen_result_by_mulan_now_codegen(read_mulan_test_source_json())


if __name__ == '__main__':
    main()
