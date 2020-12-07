
大小写英文 = r"a-zA-Z"
中文 = r"\u4e00-\u9fa5"
数字 = r"0-9"
反斜杠 = r"\\"
左小括号 = r"\("
右小括号 = r"\)"
反引号 = r"`"
双引号 = r"\""
非换行字符 = r"."

'''
如需串联, 则返回值必须为本类型. 方法都在类型内, 那么不串联(作参数)时, 就需要新建个体, 并调用`表达`方法
'''
def 序列(*各规律):
    return 规律().序列(*各规律)

def 不是(*各规律):
    return 规律().不是(*各规律)

def 任一(*各规律):
    return 规律().任一(*各规律)

# 由于参数可以是一串，如果后置则无法确认分段位置
def 分段(某规律):
    return 规律().分段(某规律)

def 引用分段(序号):
    return f"\{序号}"

class 规律:
    def __init__(self):
        self.__所有段 = []

    def 序列(self, *各规律):
        self.__所有段.append("".join(各规律))
        return self

    def 某字(self, *各规律):
        if len(各规律) == 1:
            self.__所有段.append(各规律[0])
        else:
            self.__所有段.append("[" + "".join(各规律) + "]")
        return self

    def 若干(self, 下限=None, 上限=None):
        if 下限 is None and 上限 is None:
            self.__所有段.append("*")
        elif 上限 is None:
            if 下限 == 1:
                self.__所有段.append("+")
            else:
                self.__所有段.append("{" + 下限 + "}")
        else:
            self.__所有段.append("{" + 下限 + ", " + 上限 + "}")
        return self

    def 可无(self):
        self.__所有段.append(r"?")
        return self

    def 不贪(self):
        return self.可无()

    def 表达(self):
        return "".join(map(self.__本义, self.__所有段))

    def 任一(self, *各规律):
        展开内容 = []
        for 某规律 in 各规律:
            展开内容.append(某规律.表达() if type(某规律).__name__ == "规律" else 某规律)
        self.__所有段.append("|".join(展开内容))
        return self

    def 不是(self, *各规律):
        self.__所有段.append("[^" + "".join(各规律) + "]") # TODO: 不是每次都需要 []?
        return self

    def 分段(self, 规律):
        # 如果是规律类型, 自动展开, 可省去调用一次"表达", TODO: 需加在其他所有方法内
        if type(规律).__name__ == "规律":
            规律 = 规律.表达()
        self.__所有段.append("(" + 规律 + ")")
        return self

    def 前面不是(self, 规律):
        前一位置 = len(self.__所有段) - 1
        self.__所有段[前一位置 : 前一位置] = [r"(?<!" + 规律 + r")"]
        return self

    def 引用分段(self, 序号):
        self.__所有段.append(f"\{序号}")
        return self

    # TODO: 对所有字符操作
    def __本义(self, 规律):
        if 规律 == r'$':
            return r'\$'
        else:
            return 规律