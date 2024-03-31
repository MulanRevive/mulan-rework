## 支持情况测试

测试平台： Ubuntu 20.04.3 LTS AMD64 (WSL 1)
用于进行测试的 Python 版本详细信息：

```plaintext
Python 3.10.13 (main, Mar 20 2024, 18:21:50) [GCC 9.4.0] on linux
```

运行重现项目自身测试的结果与 Python 3.9 下的测试结果完全相同，包括警告信息。

## 手工测试命令行选项功能

除了 `--反汇编` 选项以外，其他选项的行为在 Py3.10 和 Py3.9 版本间无明显差异，此处仅列出 `--反汇编` 选项的输出结果。

### 反汇编字节码测试

使用`py3.8支持.md`文件中给出的`反汇编测试.ul`运行`木兰 --反汇编 反汇编测试.ul`，结果如下：

```plaintext
  1           0 LOAD_CONST               0 (0)
              2 STORE_NAME               0 (i)

  3     >>    4 LOAD_NAME                0 (i)
              6 LOAD_CONST               1 (10)
              8 COMPARE_OP               1 (<=)
             10 POP_JUMP_IF_FALSE       44 (to 88)

  4     >>   12 LOAD_NAME                0 (i)
             14 LOAD_CONST               2 (1)
             16 INPLACE_ADD
             18 STORE_NAME               0 (i)

  6          20 SETUP_FINALLY            9 (to 40)

  7          22 LOAD_NAME                1 (__rem__)
             24 LOAD_NAME                0 (i)
             26 LOAD_CONST               3 (2)
             28 CALL_FUNCTION            2
             30 POP_JUMP_IF_FALSE       18 (to 36)

  8          32 POP_BLOCK
             34 JUMP_ABSOLUTE            2 (to 4)

  7     >>   36 POP_BLOCK
             38 JUMP_FORWARD            14 (to 68)

 10     >>   40 POP_TOP
             42 STORE_NAME               2 (Exception)
             44 POP_TOP
             46 SETUP_FINALLY            6 (to 60)
             48 POP_BLOCK
             50 POP_EXCEPT
             52 LOAD_CONST               4 (None)
             54 STORE_NAME               2 (Exception)
             56 DELETE_NAME              2 (Exception)
             58 JUMP_FORWARD             4 (to 68)
        >>   60 LOAD_CONST               4 (None)
             62 STORE_NAME               2 (Exception)
             64 DELETE_NAME              2 (Exception)
             66 RERAISE                  1

 12     >>   68 LOAD_NAME                3 (println)
             70 LOAD_NAME                0 (i)
             72 CALL_FUNCTION            1
             74 POP_TOP

  3          76 LOAD_NAME                0 (i)
             78 LOAD_CONST               1 (10)
             80 COMPARE_OP               1 (<=)
             82 POP_JUMP_IF_TRUE         6 (to 12)
             84 LOAD_CONST               4 (None)
             86 RETURN_VALUE
        >>   88 LOAD_CONST               4 (None)
             90 RETURN_VALUE
```

此处的输出字节码仅在内部实现上与 Python 3.9 有所不同。

### 警告与报错差异

[threading.currentThread()](https://docs.python.org/zh-cn/3.10/library/threading.html#threading.current_thread)此函数名自 Python 3 以来已被弃用，只是作为`threading.current_thread()`功能相同的别名。在 Python 3.10 中，使用此名字调用该函数会产生警告，替换为`threading.current_thread()`即可。

Python 3.10 中，调用类的方法时，若参数列表不匹配，报错信息由前版本的`函数名`改为`类名.函数名`，如：`类型错误：getAge() missing 1 required positional argument: 'self'`改为`类型错误：Person.getAge() missing 1 required positional argument: 'self'`

Python 3.10 中，`SyntaxError: default 'except:' must be last`报错的行号有所不同，如下：

```plaintext
>>> try:
...  1
... except:
...  1
... except:
...  1
...
  File "<stdin>", line 3 # 在旧版本中为 2
SyntaxError: default 'except:' must be last
```
