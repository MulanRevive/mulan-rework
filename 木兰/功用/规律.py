
大小写英文 = r"a-zA-Z"
中文 = r"\u4e00-\u9fa5"
数字 = r"0-9"
反斜杠 = r"\\"
左小括号 = r"\("
右小括号 = r"\)"
反引号 = r"`"

'''
如果输入输出都为字符串, 如何串联?
如需串联, 则返回值必须为本类型. 方法都在类型内, 那么不串联(作参数)时, 就需要新建个体, 并调用`表达`方法

注意, 顶层方法不可带 self!
'''
def 一个(*各规律):
    return 规律().一个(*各规律)

def 最多一个(某规律):
    return 规律().最多一个(某规律)

def 不是(*各规律):
    return 规律().不是(*各规律)

def 任意个(*各规律):
    return 规律().任意个(*各规律)

def 皆可(*各规律):
    return 规律().皆可(*各规律)

class 规律:
    def __init__(self):
        self.所有段 = []

    def 一个(self, *各规律):
        if len(各规律) == 1:
            self.所有段.append(各规律[0])
        else:
            self.所有段.append("[" + "".join(各规律) + "]")
        return self

    def 任意个(self, *各规律):
        if len(各规律) == 1:
            # TODO: 提取到方法
            if type(各规律[0]).__name__ == "规律":
                规律表达 = 各规律[0].表达()
                self.所有段.append(规律表达 + "*")
            else:
                self.所有段.append(各规律[0] + "*")
        else:
            self.所有段.append("[" + "".join(各规律) + "]*")
        return self

    def 最多一个(self, 规律):
        self.所有段.append(self.本义(规律) + r"?")
        return self

    def 表达(self):
        return "".join(self.所有段)

    def 皆可(self, *各规律):
        if len(各规律) == 1:
            self.所有段.append(各规律[0])
        else:
            self.所有段.append("|".join(各规律))
        return self

    def 不是(self, *各规律):
        self.所有段.append("[^" + "".join(各规律) + "]") # TODO: 不是每次都需要 []?
        return self

    def 分组(self, 规律):
        # 如果是规律类型, 自动展开, 可省去调用一次"表达", TODO: 需加在其他所有方法内
        if type(规律).__name__ == "规律":
            规律 = 规律.表达()
        self.所有段.append("(" + 规律 + ")")
        return self

    # TODO: 对所有字符操作
    def 本义(self, 字符):
        if 字符 == r'$':
            return r'\$'
        else:
            return 字符