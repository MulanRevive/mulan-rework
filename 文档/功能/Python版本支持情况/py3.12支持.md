## 支持情况测试

测试平台： Ubuntu 20.04.3 LTS AMD64 (WSL 1)
用于进行测试的 Python 版本详细信息：

```plaintext
Python 3.12.2 (main, Mar 22 2024, 09:19:58) [GCC 9.4.0] on linux
```

运行重现项目自身测试的结果与 Python 3.9 下的测试结果完全相同，包括警告信息。

## 手工测试命令行选项功能

除了 `--反汇编` 选项以外，其他选项的行为在 Py3.12 和 Py3.11 版本间无明显差异，此处仅列出 `--反汇编` 选项的输出结果。

### 反汇编字节码测试

使用`py3.8支持.md`文件中给出的`反汇编测试.ul`运行`木兰 --反汇编 反汇编测试.ul`，结果如下：

```plaintext
  0           0 RESUME                   0

  1           2 LOAD_CONST               0 (0)
              4 STORE_NAME               0 (i)

  3     >>    6 LOAD_NAME                0 (i)
              8 LOAD_CONST               1 (10)
             10 COMPARE_OP              26 (<=)
             14 POP_JUMP_IF_FALSE       32 (to 80)

  4     >>   16 LOAD_NAME                0 (i)
             18 LOAD_CONST               2 (1)
             20 BINARY_OP               13 (+=)
             24 STORE_NAME               0 (i)

  6          26 NOP

  7          28 PUSH_NULL
             30 LOAD_NAME                1 (__rem__)
             32 LOAD_NAME                0 (i)
             34 LOAD_CONST               3 (2)
             36 CALL                     2
             44 POP_JUMP_IF_FALSE        1 (to 48)

  8          46 JUMP_BACKWARD           21 (to 6)

  7     >>   48 NOP

 12     >>   50 PUSH_NULL
             52 LOAD_NAME                3 (println)
             54 LOAD_NAME                0 (i)
             56 CALL                     1
             64 POP_TOP

  3          66 LOAD_NAME                0 (i)
             68 LOAD_CONST               1 (10)
             70 COMPARE_OP              26 (<=)
             74 POP_JUMP_IF_FALSE        1 (to 78)
             76 JUMP_BACKWARD           31 (to 16)
        >>   78 RETURN_CONST             4 (None)
        >>   80 RETURN_CONST             4 (None)
        >>   82 PUSH_EXC_INFO

 10          84 STORE_NAME               2 (Exception)
             86 POP_EXCEPT
             88 LOAD_CONST               4 (None)
             90 STORE_NAME               2 (Exception)
             92 DELETE_NAME              2 (Exception)
             94 JUMP_BACKWARD           23 (to 50)
             96 LOAD_CONST               4 (None)
             98 STORE_NAME               2 (Exception)
            100 DELETE_NAME              2 (Exception)
            102 RERAISE                  1
        >>  104 COPY                     3
            106 POP_EXCEPT
            108 RERAISE                  1
ExceptionTable:
  28 to 44 -> 82 [0]
  82 to 84 -> 104 [1] lasti
  96 to 102 -> 104 [1] lasti
```

此处的输出字节码仅在内部实现上与 Python 3.10 有所不同，详见[CPython bytecode changes - What’s New In Python 3.12](https://docs.python.org/3/whatsnew/3.12.html#cpython-bytecode-changes)

### 警告差异

自 Python 3.8 以来，[ast.Constant](https://docs.python.org/3.8/library/ast.html#abstract-grammar) 使用`value`字段（而非`n`字段）表示常量值。在 Python 3.12 中，存取`ast.Constant`对象的`n`字段会产生`DeprecationWarning`警告。

自 Python 3.8 以来，`ast`类中的多个特性（`ast.Num`, `ast.Str`, `ast.Bytes`, `ast.NameConstant`, `ast.Ellipsis`）被弃用。在 Python 3.12 中，[访问或使用这些特性会产生`DeprecationWarning`警告](https://docs.python.org/zh-cn/3/whatsnew/3.12.html#deprecated)。

### 移除内容

Python 3.12 中，[自 Python 3.4 起被弃用的`imp`模块](https://docs.python.org/3.11/library/imp.html) [被彻底移除](https://docs.python.org/zh-cn/3/whatsnew/3.12.html#:~:text=%E7%A7%BB%E9%99%A4%E4%BA%86%20asynchat%E3%80%81asyncore%20%E5%92%8C%20imp%20%E6%A8%A1%E5%9D%97%EF%BC%8C%E4%BB%A5%E5%8F%8A%E4%B8%80%E4%BA%9B%20unittest.TestCase%20%E6%96%B9%E6%B3%95%E5%88%AB%E5%90%8D%E3%80%82)，需要使用`importlib`模块替代。
