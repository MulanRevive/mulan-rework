from tkinter import *
from tkinter.font import Font

from 分析器 import 词法分析器

root = Tk()
root.title("木兰笔谈")

# TODO: 已知问题: 输入中文符号"（"时，实际为退格，"）"时为空格。thonny 也有同样问题。
源码文件 = sys.argv[1]
with open(源码文件, 'r', encoding='utf-8') as f:
    源码 = f.read()

# 行间距设置, 参考: https://www.javatpoint.com/python-tkinter-text
文本 = Text(root, spacing1=3, spacing3=3)
文本.insert(INSERT, 源码)

文本.pack()

高亮风格 = {
    "紫红": ["动词_引用", "连词_于", "连词_对", "连词_每当", "连词_如果", "连词_否则", "点点小于", "点点"],
    "黄绿": ["整数"],
    "橙": ["字符串字面量"],
    "蓝": ["名词_函数", "名词_类型", "名词_真", "名词_假"],
    "绿": ["注释"]
}

高亮风格表 = {}
for 颜色 in 高亮风格:
    for 词性 in 高亮风格[颜色]:
        高亮风格表[词性] = 颜色

# 颜色表: https://www.w3schools.com/colors/colors_names.asp
颜色表 = {
    "紫红": "VioletRed",
    "黄绿": "YellowGreen",
    "橙": "orange",
    "蓝": "blue",
    "绿": "green",
}
各词 = 词法分析器.分词器.lex(源码)

跳过部分 = []
每行位置 = {}

# 基于 token 列表获取跳过的源码部分, 将 ignore 的注释部分也高亮
for 词 in 各词:
    行号 = 词.getsourcepos().lineno
    列号 = 词.getsourcepos().colno - 1
    词长 = len(词.getstr())

    #print(词.name + " " + 词.getstr() + " -> " + str([f'{行号}.0', f'{行号}.{列号}']))
    if 行号 not in 每行位置:
        if 列号 != 0 and 列号 > 1:
            跳过部分.append([f'{行号}.0', f'{行号}.{列号}'])
        每行位置[行号] = 列号
    # print(词.name + " " + 词.getstr() + " " + str(行号) + "." + str(列号))
    if 词.name in 高亮风格表:
        文本.tag_add(高亮风格表[词.name], f'{行号}.{列号}', f'{行号}.{列号 + 词长}')

# 遍历所有行, 看是否无 token
所有行 = 源码.splitlines()
for 索引 in range(len(所有行)):
    行号 = 索引 + 1
    if 行号 not in 每行位置:
        #print(str(行号))
        跳过部分.append([f'{行号}.0', f'{行号}.{len(所有行[索引])}'])

for i in 跳过部分:
    #print(i)
    文本.tag_add("绿", i[0], i[1])

for 颜色 in 颜色表:
    文本.tag_config(颜色, foreground=颜色表[颜色])

文本.configure(font=Font(family="Courier", size=16))

# 参考: https://www.delftstack.com/howto/python-tkinter/how-to-set-tkinter-backgroud-color/
#root.configure(background='black')
root.mainloop()