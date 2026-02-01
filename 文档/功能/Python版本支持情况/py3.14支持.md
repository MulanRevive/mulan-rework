## 支持情况测试

测试平台： Arch Linux
用于进行测试的 Python 版本详细信息：

```plaintext
Python 3.14.2 (main, Jan  2 2026, 14:27:39) [GCC 15.2.1 20251112]
```

运行重现项目自身测试的结果与 Python 3.13 下的测试结果基本相同，其中「测试/错误处理/类型定义中使用本类型.ul」无法通过测试。

在 Python 3.14 中，因 PEP 649 与 749 引入的变更，这段在 <= 3.13 会报错的代码已合法。为与 Python <= 3.13 兼容，已移除该测试。

其它测试项目均正常通过。

## 手工测试命令行选项功能

除了 `--反汇编` 选项以外，其他选项的行为在 Python 3.14 和 Python 3.13 版本间无明显差异，此处仅列出 `--反汇编` 选项的输出结果。

### 反汇编字节码测试

使用`py3.8支持.md`文件中给出的`反汇编测试.ul`运行`木兰 --反汇编 反汇编测试.ul`，结果如下：

```plaintext
   0            RESUME                   0

   1            LOAD_SMALL_INT           0
                STORE_NAME               0 (i)

   3    L1:     LOAD_NAME                0 (i)
                LOAD_SMALL_INT          10
                COMPARE_OP              58 (bool(<=))
                POP_JUMP_IF_FALSE       39 (to L6)
                NOT_TAKEN

   4            LOAD_NAME                0 (i)
                LOAD_SMALL_INT           1
                BINARY_OP               13 (+=)
                STORE_NAME               0 (i)

   6            NOP

   7    L2:     LOAD_NAME                1 (__rem__)
                PUSH_NULL
                LOAD_NAME                0 (i)
                LOAD_SMALL_INT           2
                CALL                     2
                TO_BOOL
                POP_JUMP_IF_FALSE        3 (to L4)
        L3:     NOT_TAKEN

   8            JUMP_BACKWARD           34 (to L1)

   7    L4:     NOP

  12    L5:     LOAD_NAME                3 (println)
                PUSH_NULL
                LOAD_NAME                0 (i)
                CALL                     1
                POP_TOP
                JUMP_BACKWARD           45 (to L1)

   3    L6:     LOAD_CONST               1 (None)
                RETURN_VALUE

  --    L7:     PUSH_EXC_INFO

  10            STORE_NAME               2 (Exception)
        L8:     POP_EXCEPT
                LOAD_CONST               1 (None)
                STORE_NAME               2 (Exception)
                DELETE_NAME              2 (Exception)
                JUMP_BACKWARD_NO_INTERRUPT 19 (to L5)

  --    L9:     LOAD_CONST               1 (None)
                STORE_NAME               2 (Exception)
                DELETE_NAME              2 (Exception)
                RERAISE                  1
       L10:     COPY                     3
                POP_EXCEPT
                RERAISE                  1
ExceptionTable:
  L2 to L3 -> L7 [0]
  L7 to L8 -> L10 [1] lasti
  L9 to L10 -> L10 [1] lasti
```

与 Python 3.13 相比，输出字节码有一些变化。

Python 3.14 引入了 LOAD_SMALL_INT 指令直接加载小整数以提升性能，同时大幅精简了循环结构并新增 NOT_TAKEN 等自适应标记，使字节码变得更紧凑且更利于未来的运行时优化。

### 警告差异

使用`python -m unittest 测试.unittest.交互 测试.unittest.语法树 测试.unittest.所有用例 测试.unittest.报错 测试.unittest.Python到木兰 2>&1 | sort | uniq`对警告去重后，与 Python 3.13 结果相同。

### 函数行为差异

除了上文[警告差异](#警告差异)中内容，Python 3.13 中，`ast`模块还有以下重要变化：

- 新增 `compare()` 函数，用于比较两个 AST（抽象语法树）。
- 为 AST 节点新增对 `copy.replace()` 的支持。
- 在优化级别 2 下，现在会从优化后的 AST 中移除文档字符串（Docstrings）。
- AST 节点的 `repr()` 输出现在包含更多信息。
- 当使用 AST 作为输入调用 `parse()` 函数时，现在始终会验证根节点类型是否正确。
- 命令行界面新增选项：`--feature-version`、`--optimize` 和 `--show-empty`。