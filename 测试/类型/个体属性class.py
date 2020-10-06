class Person:
  def __init__(self):
    self.class = 1

mulan = Person()
print(mulan.class)
''' 对比木兰中的 type 属性定义
  File "测试/类型/个体属性class.py", line 3
    self.class = 1
             ^
SyntaxError: invalid syntax
'''