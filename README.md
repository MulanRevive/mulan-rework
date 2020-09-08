**_注：本项目的开发管理今后将在 [OSChina](https://www.oschina.net/p/mulan-rework) 继续_**

## 前言
没错，这就是那个木兰。

2020 年一月第一时间提出知乎问题[「木兰」编程语言有什么特色？](https://www.zhihu.com/question/366509495/answer/977696328)的正是本人。

## 项目目标

在[悬赏尚未完成](https://zhuanlan.zhihu.com/p/224600854)时，本项目将持续向[悬赏目标](https://github.com/MulanRevive/bounty/blob/master/%E5%A4%8D%E7%8E%B0%E6%96%87%E6%A1%A3/README.md)推进。过程中的技术文章集结在[木兰编程语言专栏](https://zhuanlan.zhihu.com/ulang)并在[开源中国](https://www.oschina.net/p/mulan-rework)同步更新。

木兰源代码转换为 Python 的中间表示（AST）后执行，可实现各种语法设计与周边功能，并可方便地利用 Python 现有生态。

## 运行

如下运行源码（建议`.ul`后缀）。

```
$ python 中.py 测试/运算/四则运算.ul
4
```

下面[例程](测试/手工测试/草蟒_海龟.ul)调用了[草蟒](https://www.oschina.net/p/grasspy)的中文 API：
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

更多测试用例[在此](测试)。

## 开发环境

使用 Python 3.7。 Mac 和 [Linux](https://gitee.com/MulanRevive/mulan-rework/issues/I1U9O3) 下全部测试通过；windows 下测试[大多数通过](https://gitee.com/MulanRevive/mulan-rework/issues/I1U2HP)。如使用 3.8，语法树测试将失败。

为提高开发维护效率，本项目中尽量使用中文标识符。包括语法规则、Python 代码等等。

依赖 Python 包：
- rply

## 已实现功能

随着项目推进，将同步[语法说明](文档/语法说明.md)。另外，为调试方便，报错等等反馈信息将中文化。短期内的目标细化[在此](https://gitee.com/MulanRevive/mulan-rework/issues/I1SEU5)。

## 测试

```
$ chmod +x 中.py
$ python 运行测试.py
$ python test语法树.py
```

## IDE 辅助

[VS Code 语法高亮插件](https://marketplace.visualstudio.com/items?itemName=CodeInChinese.ulang)：

![](https://raw.githubusercontent.com/MulanRevive/ide-extension-vscode/master/%E6%88%AA%E5%9B%BE/%E8%B0%83%E7%94%A8python%E5%BA%93.png)

【原型状态】[自带的语法高亮编辑器](https://gitee.com/MulanRevive/mulan-rework/blob/master/%E6%BC%94%E7%A4%BA%E9%AB%98%E4%BA%AE.py)：

![](https://raw.githubusercontent.com/MulanRevive/bounty/master/%E8%BF%9B%E5%B1%95%E5%B0%8F%E7%BB%93/%E6%88%AA%E5%9B%BE/2020-06-25_mulan%E6%90%9C%E5%84%BF%E6%AD%8C.png)

## 许可证

GNU GPLv3
