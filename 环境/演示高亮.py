from tkinter import *
from tkinter.font import Font

root = Tk()

# TODO: 已知问题: 输入中文符号"（"时，实际为退格，"）"时为空格

# 行间距设置, 参考: https://www.javatpoint.com/python-tkinter-text
文本 = Text(root, spacing1=3, spacing3=3)
文本.insert(INSERT,
          "using * in 海龟"
          + "\n"
          + '\n颜色("黄色", "红色")'
          + "\n开始填充()"
          + "\nfor 拐数 in 0..4 {"
          + "\n  前进(200)"
          + "\n  右转(144)"
          + "\n}"
          + "\n结束填充()"
          + "\n主循环()")

文本.pack()

文本.tag_add("紫红", "1.0", "1.5")
文本.tag_add("紫红", "1.8", "1.10")
文本.tag_add("橙", "3.3", "3.7")
文本.tag_add("橙", "3.9", "3.13")
文本.tag_add("紫红", "5.0", "5.3")
文本.tag_add("紫红", "5.7", "5.9")
文本.tag_add("紫红", "5.11", "5.13")
文本.tag_add("黄绿", "5.10", "5.11")
文本.tag_add("黄绿", "5.13", "5.14")
文本.tag_add("黄绿", "6.5", "6.8")
文本.tag_add("黄绿", "7.5", "7.8")

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