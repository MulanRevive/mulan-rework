## 支持情况测试

测试平台： Arch Linux
用于进行测试的 Python 版本详细信息：

```plaintext
Python 3.13.5 (main, Jul 23 2025, 00:37:22) [Clang 20.1.4 ] on linux
```

运行重现项目自身测试的结果与 Python 3.9 下的测试结果完全相同，包括警告信息。

## 手工测试命令行选项功能

除了 `--反汇编` 选项以外，其他选项的行为在 Python 3.13 和 Python 3.12 版本间无明显差异，此处仅列出 `--反汇编` 选项的输出结果。

### 反汇编字节码测试

使用`py3.8支持.md`文件中给出的`反汇编测试.ul`运行`木兰 --反汇编 反汇编测试.ul`，结果如下：

```plaintext
   0            RESUME                   0

   1            LOAD_CONST               0 (0)
                STORE_NAME               0 (i)

   3    L1:     LOAD_NAME                0 (i)
                LOAD_CONST               1 (10)
                COMPARE_OP              58 (bool(<=))
                POP_JUMP_IF_FALSE       40 (to L8)

   4    L2:     LOAD_NAME                0 (i)
                LOAD_CONST               2 (1)
                BINARY_OP               13 (+=)
                STORE_NAME               0 (i)

   6            NOP

   7    L3:     LOAD_NAME                1 (__rem__)
                PUSH_NULL
                LOAD_NAME                0 (i)
                LOAD_CONST               3 (2)
                CALL                     2
                TO_BOOL
                POP_JUMP_IF_FALSE        2 (to L5)

   8    L4:     JUMP_BACKWARD           28 (to L1)

   7    L5:     NOP

  12    L6:     LOAD_NAME                3 (println)
                PUSH_NULL
                LOAD_NAME                0 (i)
                CALL                     1
                POP_TOP

   3            LOAD_NAME                0 (i)
                LOAD_CONST               1 (10)
                COMPARE_OP              58 (bool(<=))
                POP_JUMP_IF_FALSE        2 (to L7)
                JUMP_BACKWARD           39 (to L2)
        L7:     RETURN_CONST             4 (None)
        L8:     RETURN_CONST             4 (None)

  --    L9:     PUSH_EXC_INFO

  10            STORE_NAME               2 (Exception)
       L10:     POP_EXCEPT
                LOAD_CONST               4 (None)
                STORE_NAME               2 (Exception)
                DELETE_NAME              2 (Exception)
                JUMP_BACKWARD_NO_INTERRUPT 25 (to L6)

  --   L11:     LOAD_CONST               4 (None)
                STORE_NAME               2 (Exception)
                DELETE_NAME              2 (Exception)
                RERAISE                  1
       L12:     COPY                     3
                POP_EXCEPT
                RERAISE                  1
ExceptionTable:
  L3 to L4 -> L9 [0]
  L9 to L10 -> L12 [1] lasti
  L11 to L12 -> L12 [1] lasti
```

与 Python 3.12 相比，此处的输出字节码仅有输出格式微调、部分语句顺序改变，无重大差异。

### 警告差异

使用`python -m unittest 测试.unittest.交互 测试.unittest.语法树 测试.unittest.所有用例 测试.unittest.报错 测试.unittest.Python到木兰 2>&1 | sort | uniq`对警告去重后，得到以下三处警告：

```plaintext
/mulan-rework/木兰/分析器/语法树.py:199: DeprecationWarning: withitem.__init__ got an unexpected keyword argument 'col_offset'. Support for arbitrary keyword arguments is deprecated and will be removed in Python 3.15.
/mulan-rework/木兰/分析器/语法树.py:199: DeprecationWarning: withitem.__init__ got an unexpected keyword argument 'lineno'. Support for arbitrary keyword arguments is deprecated and will be removed in Python 3.15.
  return ast.withitem(

/mulan-rework/木兰/分析器/语法树.py:41: DeprecationWarning: Call.__init__ got an unexpected keyword argument 'kwargs'. Support for arbitrary keyword arguments is deprecated and will be removed in Python 3.15.
/mulan-rework/木兰/分析器/语法树.py:41: DeprecationWarning: Call.__init__ got an unexpected keyword argument 'starargs'. Support for arbitrary keyword arguments is deprecated and will be removed in Python 3.15.
  节点 = ast.Call(

/mulan-rework/木兰/分析器/语法树.py:94: DeprecationWarning: ClassDef.__init__ got an unexpected keyword argument 'kwargs'. Support for arbitrary keyword arguments is deprecated and will be removed in Python 3.15.
/mulan-rework/木兰/分析器/语法树.py:94: DeprecationWarning: ClassDef.__init__ got an unexpected keyword argument 'starargs'. Support for arbitrary keyword arguments is deprecated and will be removed in Python 3.15.
  节点 = ast.ClassDef(
```

其中`withitem`自 Python 3.7 以来始终不需要`col_offset`与`lineno`参数，直接移除。

对于`Call`与`ClassDef`，`starargs`与`kwargs`参数（曾用于表示`*args`与`**kwargs`）已在 Python 3.11 中被移除（分别被`keyword(identifier=NULL)`与`Starred`取代）。此前必须提供`starargs`与`kwargs`参数，是因为`木兰到Python`功能使用的`codegen`库读取了这两个参数。由于这两个参数对应的`*args`与`**kwargs`结构并非木兰语法特性，已在`codegen.py`与`语法树.py`中移除对应代码。

完成上述修改后，不再显示警告，且在受支持的 Python 版本中可正常运行及通过测试。

### 函数行为差异

除了上文[警告差异](#警告差异)中内容，Python 3.13 中，`ast`模块还有以下重要变化：

- 如果在构建 AST 节点实例时未提供可选字段，该字段现在将被设置为`None`。此前的版本中，新实例上会缺失对应属性。
- `ast.dump`加入`show_empty`参数，默认为`False`，即在输出省略可选的空列表。
