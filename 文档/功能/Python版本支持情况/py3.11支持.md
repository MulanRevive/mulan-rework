## 支持情况测试

测试平台： Ubuntu 20.04.3 LTS AMD64 (WSL 1)
用于进行测试的 Python 版本详细信息：

```plaintext
Python 3.11.8 (main, Feb 14 2024, 15:43:40) [GCC 9.4.0] on linux
```

运行重现项目自身测试的结果与 Python 3.9 下的测试结果完全相同，包括警告信息。

## 手工测试命令行选项功能

除了 `--反汇编` 选项以外，其他选项的行为在 Py3.11 和 Py3.10 版本间无明显差异，此处仅列出 `--反汇编` 选项的输出结果。

### 反汇编字节码测试

使用`py3.8支持.md`文件中给出的`反汇编测试.ul`运行`木兰 --反汇编 反汇编测试.ul`，结果如下：

```plaintext
  0           0 RESUME                   0

  1           2 LOAD_CONST               0 (0)
              4 STORE_NAME               0 (i)

  3     >>    6 LOAD_NAME                0 (i)
              8 LOAD_CONST               1 (10)
             10 COMPARE_OP               1 (<=)
             16 POP_JUMP_FORWARD_IF_FALSE    53 (to 124)

  4     >>   18 LOAD_NAME                0 (i)
             20 LOAD_CONST               2 (1)
             22 BINARY_OP               13 (+=)
             26 STORE_NAME               0 (i)

  6          28 NOP

  7          30 PUSH_NULL
             32 LOAD_NAME                1 (__rem__)
             34 LOAD_NAME                0 (i)
             36 LOAD_CONST               3 (2)
             38 PRECALL                  2
             42 CALL                     2
             52 POP_JUMP_FORWARD_IF_FALSE     1 (to 56)

  8          54 JUMP_BACKWARD           25 (to 6)

  7     >>   56 JUMP_FORWARD            14 (to 86)
        >>   58 PUSH_EXC_INFO

 10          60 STORE_NAME               2 (Exception)
             62 POP_EXCEPT
             64 LOAD_CONST               4 (None)
             66 STORE_NAME               2 (Exception)
             68 DELETE_NAME              2 (Exception)
             70 JUMP_FORWARD             7 (to 86)
             72 LOAD_CONST               4 (None)
             74 STORE_NAME               2 (Exception)
             76 DELETE_NAME              2 (Exception)
             78 RERAISE                  1
        >>   80 COPY                     3
             82 POP_EXCEPT
             84 RERAISE                  1

 12     >>   86 PUSH_NULL
             88 LOAD_NAME                3 (println)
             90 LOAD_NAME                0 (i)
             92 PRECALL                  1
             96 CALL                     1
            106 POP_TOP

  3         108 LOAD_NAME                0 (i)
            110 LOAD_CONST               1 (10)
            112 COMPARE_OP               1 (<=)
            118 POP_JUMP_BACKWARD_IF_TRUE    51 (to 18)
            120 LOAD_CONST               4 (None)
            122 RETURN_VALUE
        >>  124 LOAD_CONST               4 (None)
            126 RETURN_VALUE
ExceptionTable:
  30 to 52 -> 58 [0]
  58 to 60 -> 80 [1] lasti
  72 to 78 -> 80 [1] lasti
```

此处的输出字节码与 Python 3.10 有所不同，主要为性能优化。详见[CPython bytecode changes - What’s New In Python 3.11](https://docs.python.org/3/whatsnew/3.11.html#cpython-bytecode-changes)

### 警告与报错差异

[UnboundLocalError](https://docs.python.org/3/library/exceptions.html#UnboundLocalError) 报错内容略有更改。

当试图对未实现`__enter__`的类的对象使用形如`with obj:`的上下文管理器操作时，报错类型由`AttributeError`改为`TypeError`，并完善了报错信息。
