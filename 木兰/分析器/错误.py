class 语法错误(ValueError):

    def __init__(self, 信息, 文件名, 行号, 列号, 源码=None):
        self.信息 = 信息
        self.文件名 = 文件名
        self.行号 = 行号 if 行号 > 0 else 1
        self.列号 = 列号 if 列号 > 0 else 1
        self.源码 = 源码

    # TODO: 应使错误更易定位
    def __str__(self):
        反馈信息 = '文件 "%s", 第%d行, 第%d列, %s' % (
                self.文件名, self.行号, self.列号, self.信息)
        if self.源码:
            行 = self.源码[(self.行号 - 1)]
            出错位置 = self.列号 - 1

        # 为规避中文字符在命令行中宽度与英文不等导致的^指向不准问题, 直接在错误位置插入指示符
        return '%s\n%s' % (反馈信息, 行[:出错位置] + '✋' + 行[出错位置:])

class 词法错误(语法错误):

    def __init__(self, 异常, 文件名, 源码=None):
        self.信息='分词时没认出这个词 "%s"' % 源码[异常.getsourcepos().idx]
        self.文件名=文件名
        self.行号=异常.getsourcepos().lineno
        self.列号=异常.getsourcepos().colno
        self.源码=源码.split("\n")