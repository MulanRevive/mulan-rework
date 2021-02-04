报错：
```
 😰 递归过深。请确认: 1、的确需要递归 2、递归的收敛正确
“/opt/anaconda3/lib/python3.7/ast.py”第188行：yield field, getattr(node, field)
“/opt/anaconda3/lib/python3.7/ast.py”第271行：return visitor(node)
“/opt/anaconda3/lib/python3.7/ast.py”第271行：return visitor(node)
“/opt/anaconda3/lib/python3.7/ast.py”第271行：return visitor(node)
“/opt/anaconda3/lib/python3.7/ast.py”第271行：return visitor(node)
“/opt/anaconda3/lib/python3.7/ast.py”第271行：return visitor(node)
“a.ul”第1行：using b
见第1行：using a
“a.ul”第1行：using b
见第1行：using a
“a.ul”第1行：using b
见第1行：using a
“a.ul”第1行：using b
```

python 中，并无循环引用，报错：
```
Traceback (most recent call last):
  File "b.py", line 1, in <module>
    import a
  File "/Users/xuanwu/work/木兰/木兰重现/testpy/a.py", line 1, in <module>
    import b
  File "/Users/xuanwu/work/木兰/木兰重现/testpy/b.py", line 3, in <module>
    bb = a.aa
AttributeError: module 'a' has no attribute 'aa'
```