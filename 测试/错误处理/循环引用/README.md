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