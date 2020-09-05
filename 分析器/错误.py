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
        return '%s\n%s' % (反馈信息, 行[:出错位置] + '✋' + 行[出错位置:])