## 支持情况测试

测试平台： Windows 10 AMD64
用于进行测试的 Python3.8 版本详细信息：

```
Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
```

运行重现项目自身测试的结果：

```
$ python -m unittest 测试.unittest.交互 测试.unittest.语法树 测试.unittest.所有用例  测试.unittest.报错 测试.unittest.Python到木兰
....测试\运算\比较.ul:1: SyntaxWarning: "is" with a literal. Did you mean "=="?
  if 2===2 {
测试\运算\比较.ul:4: SyntaxWarning: "is" with a literal. Did you mean "=="?
  if 2===3 {
测试\运算\比较.ul:7: SyntaxWarning: "is not" with a literal. Did you mean "!="?
  if 2!==1 {
测试\运算\比较.ul:10: SyntaxWarning: "is not" with a literal. Did you mean "!="?
  if 2!==2 {
........
----------------------------------------------------------------------
Ran 12 tests in 4.727s

OK
```

*(有关上述的警告输出，请见下文的“警告差异”)*

#### 命令行参数行为对比测试

这里列出测试中用到的 `反汇编测试.ul` ：

```
i = 0

while i <= 10 {
    i += 1

    try {
        if i % 2 {
           continue;
        }   
    } catch Exception {}

    println(i)
}
```

对于上面的这个测试用例，在循环中加入了 try - catch 块的作用在于引导 Python3.7 生成 `CONTINUE_LOOP` 指令，以突出与 Python3.8 的不同之处。



由于 `--语法树` 参数的差异已经在下文说明，且除了 `--反汇编` 选项以外，其他选项的行为在 Py3.8 和 Py3.7 版本间无明显差异，故仅列出 `--反汇编` 选项的输出结果。

##### --反汇编

Py3.7:

```python
$ 木兰 -反 反汇编测试.ul
  2           0 LOAD_CONST               0 (0)
              2 STORE_NAME               0 (i)

  4           4 SETUP_LOOP              72 (to 78)
        >>    6 LOAD_NAME                0 (i)
              8 LOAD_CONST               1 (10)
             10 COMPARE_OP               1 (<=)
             12 POP_JUMP_IF_FALSE       76

  5          14 LOAD_NAME                0 (i)
             16 LOAD_CONST               2 (1)
             18 INPLACE_ADD
             20 STORE_NAME               0 (i)

  7          22 SETUP_EXCEPT            16 (to 40)

  8          24 LOAD_NAME                1 (__rem__)
             26 LOAD_NAME                0 (i)
             28 LOAD_CONST               3 (2)
             30 CALL_FUNCTION            2
             32 POP_JUMP_IF_FALSE       36

  9          34 CONTINUE_LOOP            6
        >>   36 POP_BLOCK
             38 JUMP_FORWARD            26 (to 66)

 11     >>   40 POP_TOP
             42 STORE_NAME               2 (Exception)
             44 POP_TOP
             46 SETUP_FINALLY            4 (to 52)
             48 POP_BLOCK
             50 LOAD_CONST               4 (None)
        >>   52 LOAD_CONST               4 (None)
             54 STORE_NAME               2 (Exception)
             56 DELETE_NAME              2 (Exception)
             58 END_FINALLY
             60 POP_EXCEPT
             62 JUMP_FORWARD             2 (to 66)
             64 END_FINALLY

 13     >>   66 LOAD_NAME                3 (println)
             68 LOAD_NAME                0 (i)
             70 CALL_FUNCTION            1
             72 POP_TOP
             74 JUMP_ABSOLUTE            6
        >>   76 POP_BLOCK
        >>   78 LOAD_CONST               4 (None)
             80 RETURN_VALUE
```

Py3.8:

```python
$ 木兰 -反 反汇编测试.ul
  2           0 LOAD_CONST               0 (0)
              2 STORE_NAME               0 (i)

  4     >>    4 LOAD_NAME                0 (i)
              6 LOAD_CONST               1 (10)
              8 COMPARE_OP               1 (<=)
             10 POP_JUMP_IF_FALSE       76

  5          12 LOAD_NAME                0 (i)
             14 LOAD_CONST               2 (1)
             16 INPLACE_ADD
             18 STORE_NAME               0 (i)

  7          20 SETUP_FINALLY           18 (to 40)

  8          22 LOAD_NAME                1 (__rem__)
             24 LOAD_NAME                0 (i)
             26 LOAD_CONST               3 (2)
             28 CALL_FUNCTION            2
             30 POP_JUMP_IF_FALSE       36

  9          32 POP_BLOCK
             34 JUMP_ABSOLUTE            4
        >>   36 POP_BLOCK
             38 JUMP_FORWARD            26 (to 66)

 11     >>   40 POP_TOP
             42 STORE_NAME               2 (Exception)
             44 POP_TOP
             46 SETUP_FINALLY            4 (to 52)
             48 POP_BLOCK
             50 BEGIN_FINALLY
        >>   52 LOAD_CONST               4 (None)
             54 STORE_NAME               2 (Exception)
             56 DELETE_NAME              2 (Exception)
             58 END_FINALLY
             60 POP_EXCEPT
             62 JUMP_FORWARD             2 (to 66)
             64 END_FINALLY

 13     >>   66 LOAD_NAME                3 (println)
             68 LOAD_NAME                0 (i)
             70 CALL_FUNCTION            1
             72 POP_TOP
             74 JUMP_ABSOLUTE            4
        >>   76 LOAD_CONST               4 (None)
             78 RETURN_VALUE
```

## 差异

就目前而言，在对 Python3.8 版本进行适配的过程中，发现了如下的差异：

### 语法树节点差异

与 Python3.7 版本相比，升级到 Python3.8 对木兰的内部实现的主要影响在于 **部分语法树节点的改变**。 

主要的变化在于一下几点：

- Python3.7 使用了 `Num`, `NameConstant`, `Str` 语法树节点分别代表数字常量、名称常量（如 `None`, `True`, `False`）和字符串字面量。而在 Python3.8 中，使用了 `Constant` 节点来统一替代先前提到的三个节点。
- 对于 `arguments` 节点，Python3.8 加入了`posonlyargs=[]` 参数。
- 对于部分其他节点，加入了 `type_ignores` 参数。

实际差异可见 `测试/unittest/语法树.py`：中对 Python3.8 的[期望值](/测试/unittest/语法树.py#L46)。

因此，在 Python 3.8 下的木兰行为在开启 `--语法树` 选项时，会与原始木兰以及 Python3.7 下的木兰有输出差异。

### 警告差异

相比于 Python3.7，Python3.8 版本增加了对不当使用 `is` 运算符的警告。也就是说当木兰中 `===` 运算符左右两边出现了至少一项 **数字字面量** 或 **字符串字面量** 时，会得到下面的警告：

```
SyntaxWarning: "is" with a literal. Did you mean "=="?
```

测试结果请见[操作符的测试用例](/测试/运算/比较.ul)

警告用户最好不要以这种方式去使用 `===` 运算符。
