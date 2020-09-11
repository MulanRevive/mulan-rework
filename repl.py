import sys, cmd
from 分析器.词法分析器 import *
from 分析器.语法分析器 import 语法分析器
from 环境 import 创建全局变量
from 功用.反馈信息 import 反馈信息

def is_close(源码):
    """
    Check if the given 源码 is closed,
    which means each '{' has a matched '}' 
    """
    关键词 = {
     名词_函数, #'OPERATOR', 'ATTR', 'TYPE',
     #'FOR', 'LOOP', 'WHILE',
     #'IF', 'ELIF', 'ELSE',
     #'TRY', 'CATCH', 'FINALLY'
    }
    未配对之和 = 0
    unclosed_sum = 0
    if len(源码) > 1:
        if 源码[-2] == '\\':
            return False
        else:
            tokens = 分词器.lex(源码)
            unclosed = []
            未配对 = [
            0, 0, 0]
            last = 2 * ['']
            for tok in tokens:
                c = tok.gettokentype()
                last[0], last[1] = last[1], c
                if c in 关键词:
                    unclosed.append(c)
                if c == 前大括号:
                    未配对[0] += 1
                elif c == 后大括号:
                    未配对[0] -= 1
                    if len(unclosed):
                        unclosed.pop(-1)
                elif c == '(':
                    未配对[1] += 1
                elif c == ')':
                    未配对[1] -= 1
                elif c == '[':
                    未配对[2] += 1
                elif c == ']':
                    未配对[2] -= 1
            未配对之和 = sum(未配对)
            unclosed_sum = len(unclosed)
            if unclosed_sum > 0:
                if 未配对之和 == 0:
                    if last[1] == 'NEWLINE':
                        if (last[0] == 'NEWLINE' or last[0]) == ';':
                            pass
                        return True
    return unclosed_sum == 0 and 未配对之和 == 0


def input_swallowing_interrupt(_input):

    def _input_swallowing_interrupt(*args):
        try:
            return _input(*args)
        except KeyboardInterrupt:
            print('^C')
            return '\n'

    return _input_swallowing_interrupt


class Repl(cmd.Cmd):
    """
    A simple wrapper for REPL using the python cmd module.
    """

    def __init__(self, ps1='> ', ps2='>> ', globals=None, locals=None):
        super().__init__()
        self.ps1 = ps1
        self.ps2 = ps2
        self.globals = globals
        self.locals = locals
        self.parser = 语法分析器(分词器)
        self.prompt = ps1
        self.stmt = ''

    def do_help(self, arg):
        self.default('help(%s)' % arg)

    def do_quit(self, arg):
        self.default('quit(%s)' % arg)

    def do_EOF(self, arg):
        self.default('quit()')

    def onecmd(self, line):
        if line == 'EOF':
            return self.do_EOF(line)
        self.default(line)
        self.prompt = self.ps1 if len(self.stmt) == 0 else self.ps2

    def default(self, line):
        if line is not None:
            self.stmt += '%s\n' % line
            if not self.is_close():
                return
            try:
                try:
                    node = self.parser.分析('___=(%s);__print__(___)' % self.stmt, '<STDIN>')
                except Exception:
                    node = self.parser.分析(self.stmt, '<STDIN>')

                code = compile(node, '<STDIN>', 'exec')
                exec(code, self.globals, self.locals)
            except SystemExit:
                sys.exit()
            except BaseException as e:
                try:
                    sys.stderr.write('%s\n' % 反馈信息(e))
                finally:
                    e = None
                    del e

            finally:
                self.stmt = ''

    def is_close(self):
        return is_close(self.stmt)

    def cmdloop(self, *args, **kwargs):
        orig_input_func = cmd.__builtins__['input']
        cmd.__builtins__['input'] = input_swallowing_interrupt(orig_input_func)
        try:
            (super().cmdloop)(*args, **kwargs)
        finally:
            cmd.__builtins__['input'] = orig_input_func


def repl(ps1='> ', ps2='>> ', globals=None):
    """
    A simple read-eval-print-loop for the µLang program
    """
    info = [
     '\t详情: 列出内置功能',
     '\t再会: 结束对话',
     '\t你好: 显示这段']
    if not globals:
        globals = 创建全局变量(文件名='<STDIN>')
    globals['详情'] = lambda : print('\n'.join([' %s (%s)' % (k, v.__class__.__name__) for k, v in globals.items() if k != '__builtins__' if k != '___']))
    globals['你好'] = lambda *args: print('\n'.join(info)) if not args else print()
    Repl(ps1, ps2, globals).cmdloop("木兰向您问好\n更多信息请说'你好'")
    sys.exit(0)