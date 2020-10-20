
## 前言

没错，这就是那个木兰。

2020 年一月第一时间提出知乎问题[「木兰」编程语言有什么特色？](https://www.zhihu.com/question/366509495)的正是本人，[这是那段暴风骤雨的亲历记](https://zhuanlan.zhihu.com/p/265091649)。

## 目标

在[悬赏尚未完成](https://zhuanlan.zhihu.com/p/224600854)时，将努力向[重现「木兰」编程语言的目标](https://gitee.com/MulanRevive/bounty/blob/master/%E5%A4%8D%E7%8E%B0%E6%96%87%E6%A1%A3/README.md)迈进。过程中的技术文章集结在[知乎专栏](https://zhuanlan.zhihu.com/ulang)并在[开源中国](https://www.oschina.net/p/mulan-rework)同步更新。

木兰源代码转换为 Python 的中间表示（AST）后执行，可实现各种语法设计与周边功能，并可方便地利用 Python 现有生态。

## 运行

***！必需 Python 3.7 ！***

通过 `pip install ulang` 安装木兰。

### 命令行交互环境

```
$ 木兰
木兰向您问好
更多信息请说'你好'
> 和 = 0
> for 数 in 1..10 {
>> 和 += 数
>> }
> print(和)
55
```

### IDE 辅助

[VS Code 语法高亮插件](https://marketplace.visualstudio.com/items?itemName=CodeInChinese.ulang)：

![vsc截图](https://gitee.com/MulanRevive/ide-extension-vscode/raw/master/%E6%88%AA%E5%9B%BE/%E8%B0%83%E7%94%A8python%E5%BA%93.png)

【原型】[自带的编辑器](https://gitee.com/MulanRevive/mulan-rework/tree/master/编辑器)：

![自带IDE截图](https://gitee.com/MulanRevive/bounty/raw/master/%E8%BF%9B%E5%B1%95%E5%B0%8F%E7%BB%93/%E6%88%AA%E5%9B%BE/2020-06-25_mulan%E6%90%9C%E5%84%BF%E6%AD%8C.png)

### 运行木兰源码文件

建议`.ul`后缀
```
$ 木兰 测试/运算/四则运算.ul
4
```

下面[例程](https://gitee.com/MulanRevive/mulan-rework/tree/master/测试/手工测试/草蟒_海龟.ul)调用了[草蟒](https://www.oschina.net/p/grasspy)的中文 API：
```javascript
using * in 海龟

颜色("黄色", "红色")
开始填充()
for 转角 in 0..4 {
  前进(200); 右转(144)
}
结束填充()
主循环()
/* 需安装 Python 库“草蟒”： grasspy-modules */
```

### 中文报错信息

交互环境中仅提示出错所在位置简要信息：
```
> func a(n) { return n1+1 }
> func b(n) { print(n) }
> b(a(2))
 😰 请先定义'n1'再使用, 见第1行
```
运行源码时，可以看到调用各层详细信息：
```
$ 木兰 测试/错误处理/未定义变量于多层函数.ul
 😰 请先定义'数1'再使用
见第2行：return 数1 + 1
调用层级如下
见第7行：输出(加(2))
```

## 参考例程[在此](https://gitee.com/MulanRevive/mulan-rework/tree/master/测试)

其中[实用](https://gitee.com/MulanRevive/mulan-rework/tree/master/测试/实用)为较接近实用的部分。另外[木兰代码编辑器](https://gitee.com/MulanRevive/mulan-rework/tree/master/编辑器)也用木兰代码编写。

所有例程演示的语法可用原始的木兰可执行文件 [ulang-0.2.2.exe](https://gitee.com/MulanRevive/bounty/tree/master/%E5%8E%9F%E5%A7%8B%E8%B5%84%E6%96%99/%E5%8F%AF%E6%89%A7%E8%A1%8C%E6%96%87%E4%BB%B6) 检验。***如发现有异烦请告知，定将[同样礼谢](https://gitee.com/MulanRevive/bounty)。***

### 新手入门

如果无编程经验，请入[此门](https://gitee.com/MulanRevive/mulan-rework/tree/master/文档/用户手册/编程新手/1猜数字.md)。

## 功能说明

随着逐渐缩小[与原版木兰的差距](https://gitee.com/MulanRevive/mulan-rework/issues/I1SEU5)，将补充[语言语法规则](文档/语法说明.md)。用户手册[尚待更新](https://gitee.com/MulanRevive/mulan-rework/issues/I1U36D)。为调试方便，报错等等反馈信息会[逐渐中文化](https://zhuanlan.zhihu.com/p/148065426)。

交互环境功能说明[在此](https://gitee.com/MulanRevive/mulan-rework/tree/master/文档/功能/交互环境.md)。

## 开发

使用 Python 3.7。 Mac 和 [Linux](https://gitee.com/MulanRevive/mulan-rework/issues/I1U9O3) 下全部测试通过；windows 下测试[大多数通过](https://gitee.com/MulanRevive/mulan-rework/issues/I1U2HP)。如使用 3.8，语法树测试将失败。

为提高开发维护效率，本项目中尽量使用中文标识符。包括语法规则、Python 代码等等。

依赖 Python 包：
- [rply](https://pypi.org/project/rply/)

### 本地运行

```
$ python -m 木兰
```

### 运行测试

```
$ python 测试/运行所有.py
$ python -m unittest 测试.unittest.交互 测试.unittest.语法树
```
为检验[与原始木兰可执行文件功能一致](https://zhuanlan.zhihu.com/p/230155471)，需先阅读“win32”部分注释并手动修改。

## 许可证

GNU GPLv3

## [版本历史介绍](CHANGELOG.md)