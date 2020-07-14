import random, string

def 随机文本(长度=20):
    字母 = string.ascii_letters
    return ''.join((random.choice(字母) for i in range(长度)))