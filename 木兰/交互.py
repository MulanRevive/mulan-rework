import sys, cmd
from rply.errors import LexingError

from 木兰.分析器.词法分析器 import *
from 木兰.分析器.语法分析器 import 语法分析器
from 木兰.环境 import 创建全局变量
from 木兰.功用.反馈信息 import 反馈信息
from 木兰.分析器.错误 import 语法错误, 词法错误

# TODO: 更多测试
def 括号已配对(源码):
    关键词 = {
        名词_操作符, 名词_函数, 名词_类型, #'OPERATOR', 'FUNC', 'ATTR', 'TYPE',
        连词_对, 动词_循环, 连词_每当,
        连词_如果, 连词_否则如果, 连词_否则,
        #'TRY', 'CATCH', 'FINALLY'
    }
    未配对之和 = 0
    未闭合的个数 = 0
    if len(源码) > 1:
        if 源码[-2] == '\\':
            return False
        else:
            各词 = 分词器.lex(源码)
            未闭合的 = []
            未配对 = [0, 0, 0]
            末两词 = 2 * ['']
            for 词 in 各词:
                c = 词.gettokentype()
                末两词[0], 末两词[1] = 末两词[1], c
                if c in 关键词:
                    未闭合的.append(c)
                if c == 前大括号:
                    未配对[0] += 1
                elif c == 后大括号:
                    未配对[0] -= 1
                    if len(未闭合的):
                        未闭合的.pop(-1)
                elif c == 前小括号:
                    未配对[1] += 1
                elif c == 后小括号:
                    未配对[1] -= 1
                elif c == 前中括号:
                    未配对[2] += 1
                elif c == 后中括号:
                    未配对[2] -= 1
            未配对之和 = sum(未配对)
            未闭合的个数 = len(未闭合的)
            if 未闭合的个数 > 0:
                if 未配对之和 == 0:
                    if 末两词[1] == 换行:
                        if 末两词[0] == 换行 or 末两词[0] == 分号:
                            return True
    return 未闭合的个数 == 0 and 未配对之和 == 0


def input_swallowing_interrupt(_input):

    def _input_swallowing_interrupt(*args):
        try:
            return _input(*args)
        except KeyboardInterrupt:
            # TODO: 何用？
            print('^C')
            return '\n'

    return _input_swallowing_interrupt


class 交互(cmd.Cmd):
    # 本地变量暂时无用
    def __init__(self, 提示符1='> ', 提示符2='>> ', 全局变量=None):
        super().__init__()
        self.提示符1 = 提示符1
        self.提示符2 = 提示符2
        self.全局变量 = 全局变量
        self.分析器 = 语法分析器(分词器)
        self.prompt = 提示符1
        self.声明 = ''

    def do_EOF(self, arg):
        self.default('再会()')

    def onecmd(self, 行):
        if 行 == 'EOF':
            return self.do_EOF(行)
        self.default(行)
        self.prompt = self.提示符1 if len(self.声明) == 0 else self.提示符2

    def default(self, 行):
        if 行 is not None:
            self.声明 += '%s\n' % 行
            try:
                if not self.括号已配对():
                    return
            except LexingError as e:
                错误 = 词法错误(异常=e,
                    文件名='【标准输入】',
                    源码=self.声明)
                sys.stderr.write('%s\n' % 反馈信息(错误))
                self.声明 = ''
            try:
                try:
                    节点 = self.分析器.分析('___=(%s);__print__(___)' % self.声明, '【标准输入】')
                except Exception:
                    节点 = self.分析器.分析(self.声明, '【标准输入】')

                可执行码 = compile(节点, '【标准输入】', 'exec')
                exec(可执行码, self.全局变量)
            except SystemExit:
                sys.exit()
            except BaseException as e:
                try:
                    sys.stderr.write('%s\n' % 反馈信息(e))
                finally:
                    e = None
                    del e

            finally:
                self.声明 = ''

    def 括号已配对(self):
        return 括号已配对(self.声明)

    def cmdloop(self, *args, **kwargs):
        原始输入函数 = cmd.__builtins__['input']
        cmd.__builtins__['input'] = input_swallowing_interrupt(原始输入函数)
        try:
            (super().cmdloop)(*args, **kwargs)
        finally:
            cmd.__builtins__['input'] = 原始输入函数


def 开始交互(提示符1='> ', 提示符2='>> ', 全局变量=None):
    """
    简易的木兰交互环境
    """
    介绍 = [
     '\t详情: 列出内置功能',
     '\t再会: 结束对话',
     '\t你好: 显示这段']
    if not 全局变量:
        # TODO: 何时会用
        全局变量 = 创建全局变量(文件名='<STDIN>')
    全局变量['详情'] = lambda : print('\n'.join([' %s (%s)' % (k, v.__class__.__name__) for k, v in 全局变量.items() if k != '__builtins__' if k != '___']))
    全局变量['globals'] = lambda: 全局变量['详情']()
    全局变量['你好'] = lambda *args: print('\n'.join(介绍)) if not args else print()
    全局变量['help'] = lambda: 全局变量['你好']()
    交互(提示符1, 提示符2, 全局变量).cmdloop("木兰向您问好\n更多信息请说'你好'")
    sys.exit(0)