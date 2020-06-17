from tkinter import *
from tkinter.font import Font

from 分析器 import 词法分析器

root = Tk()

# TODO: 已知问题: 输入中文符号"（"时，实际为退格，"）"时为空格。thonny 也有同样问题。

源码 = """using * in 海龟

颜色("黄色", "红色")
开始填充()
for 拐数 in 0..4 {
  前进(200)
  右转(144)
}
结束填充()
主循环()
"""

# 行间距设置, 参考: https://www.javatpoint.com/python-tkinter-text
文本 = Text(root, spacing1=3, spacing3=3)
文本.insert(INSERT, 源码)

文本.pack()

高亮风格 = {
    "动词_引用": "紫红",
    "连词_于": "紫红",
    "连词_对": "紫红",
    "整数": "黄绿",
    "字符串字面量": "橙",
}
各词 = 词法分析器.分词器.lex(源码)
for 词 in 各词:
    行号 = 词.getsourcepos().lineno
    列号 = 词.getsourcepos().colno
    词长 = len(词.getstr())
    #print(词.name + " " + 词.getstr() + " " + str(行号) + "." + str(列号))
    if 词.name in 高亮风格:
        文本.tag_add(高亮风格[词.name], str(行号) + "." + str(列号 - 1), str(行号) + "." + str(列号 - 1 + 词长))

# 颜色表: https://www.w3schools.com/colors/colors_names.asp
文本.tag_config("蓝", foreground="blue")
文本.tag_config("红", foreground="red")
文本.tag_config("橙", foreground="orange")
文本.tag_config("绿黄", foreground="GreenYellow")
文本.tag_config("黄绿", foreground="YellowGreen")
文本.tag_config("紫红", foreground="VioletRed")

myFont = Font(family="Courier", size=16)
文本.configure(font=myFont)

# 参考: https://www.delftstack.com/howto/python-tkinter/how-to-set-tkinter-backgroud-color/
#root.configure(background='black')
root.mainloop()