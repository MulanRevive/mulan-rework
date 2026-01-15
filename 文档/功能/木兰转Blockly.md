原始可执行文件`ulang-0.2.2.exe`中，使用`--dump-blockly`选项，可以将木兰源码转为[Blockly 的 XML 格式代码](https://developers.google.com/blockly/guides/configure/web/serialization?hl=zh-cn#xml_system)。生成 XML 并在 Blockly 编辑区加载显示的步骤如下：

1. 创建`和.ul`，内容如下：

```python
total = 0
for current in 1..10 {
 total += current
}
print(total)
```

2. 使用`ulang-0.2.2.exe --dump-blockly 和.ul >和.blockly.xml`，得到`和.blockly.xml`

3. 打开`https://raspberrypifoundation.github.io/blockly-samples/examples/devsite-landing-demo/index.html`，启动开发者工具，切换到控制台。

4. 粘贴以下代码，即可看到 Blockly 编辑区出现对应功能的“代码”。

```js
/**
 * 将特定的 Blockly XML 字符串加载到工作区
 * @param {string} xmlText - 传入的 XML 字符串
 * @param {Blockly.Workspace} workspace - 当前的 Blockly 工作区实例
 */
function loadSecondaryXmlToBlockly(xmlText, workspace) {
    try {
        // 1. 清理字符串：去除可能导致解析错误的 XML 声明头部的多余空格
        const cleanedXml = xmlText.trim();

        // 2. 将字符串解析为 DOM 结构
        // Blockly 内部使用 DOMParser 处理命名空间和声明
        const xmlDom = Blockly.utils.xml.textToDom(cleanedXml);

        // 3. (可选) 清空当前工作区，如果不清空则是追加块
        workspace.clear();

        // 4. 将 DOM 加载到工作区
        // domToWorkspace 会返回加载后的 Block ID 数组
        const newBlockIds = Blockly.Xml.domToWorkspace(xmlDom, workspace);

        console.log('加载成功，生成的块数量:', newBlockIds.length);

        // 5. 自动整理布局 (可选)
        // 因为 XML 缺少 x, y 坐标，块会堆叠在 (0,0)
        // 如果是导入到主工作区，建议进行一次布局排布
        if (workspace.cleanUp) {
            workspace.cleanUp();
        }

    } catch (e) {
        console.error('加载 Blockly XML 出错:', e);
    }
}

// 使用示例：
和BlocklyXml = `
<?xml version="1.0" ?>
<xml xmlns="http://www.w3.org/1999/xhtml">
  <variables>
    <variable id="tHaBReuKboBKFETzXSTR" type="">total</variable>
    <variable id="yJIZtLhVuKZaHJjUDqOA" type="">current</variable>
  </variables>
  <block id="xDdGzOPbVmwWqelLNHJw" type="variables_set">
    <field id="tHaBReuKboBKFETzXSTR" name="VAR" variabletype="">total</field>
    <value name="VALUE">
      <block id="FKwxxLrYLBCtgwFcQqKL" type="math_number">
        <field name="NUM">0</field>
      </block>
    </value>
    <next>
      <block id="FrOktgWbdHkhdzQtaZgI" type="controls_for">
        <field name="VAR">current</field>
        <value name="FROM">
          <block id="yEPhgJlwztcYocMngRAt" type="math_number">
            <field name="NUM">1</field>
          </block>
        </value>
        <value name="TO">
          <block id="QdmpfnqlWedTNMPAKXPy" type="math_arithmetic">
            <field name="OP">SUB</field>
            <value name="A">
              <block id="OILIBlQnRUZfsEYqUivB" type="math_arithmetic">
                <field name="OP">ADD</field>
                <value name="A">
                  <block id="ylTYyttHKhfdAavGEKsc" type="math_number">
                    <field name="NUM">10</field>
                  </block>
                </value>
                <value name="B">
                  <block id="GAEAFEJbjHEuSspkduTj" type="math_number">
                    <field name="NUM">1</field>
                  </block>
                </value>
              </block>
            </value>
            <value name="B">
              <block id="TnRSnWcCTGCHLllYVjnE" type="math_number">
                <field name="NUM">1</field>
              </block>
            </value>
          </block>
        </value>
        <value name="BY">
          <block id="oyLcLlDDnuSFtYITiNbj" type="math_number">
            <field name="NUM">1</field>
          </block>
        </value>
        <statement name="DO">
          <block id="DtKztbPqmWrIBuJwgmyz" type="variables_set">
            <field id="tHaBReuKboBKFETzXSTR" name="VAR" variabletype="">total</field>
            <value name="VALUE">
              <block id="pnEGRviZFtixDTkkNqJD" type="math_arithmetic">
                <field name="OP">ADD</field>
                <value name="A">
                  <block id="hKZYbhLszOOODMqlfvvd" type="variables_get">
                    <field id="tHaBReuKboBKFETzXSTR" name="VAR" variabletype="">total</field>
                  </block>
                </value>
                <value name="B">
                  <block id="FifOeyjfgxZqSdydTbJG" type="variables_get">
                    <field id="yJIZtLhVuKZaHJjUDqOA" name="VAR" variabletype="">current</field>
                  </block>
                </value>
              </block>
            </value>
          </block>
        </statement>
        <next>
          <block id="xHllqSCOcWJcsovJjjJW" type="text_print">
            <value name="TEXT">
              <block id="LnIAkFssDVHbTKRUiBRW" type="variables_get">
                <field id="tHaBReuKboBKFETzXSTR" name="VAR" variabletype="">total</field>
              </block>
            </value>
          </block>
        </next>
      </block>
    </next>
  </block>
</xml>
`;
primaryWorkspace = Blockly.getMainWorkspace()
loadSecondaryXmlToBlockly(和BlocklyXml, primaryWorkspace);
```

需要注意的是，实际使用中，Blockly一般是嵌入其他网页应用的，开发者应当向用户提供解析XML的功能。具体的实现方式可以参考[此示例](https://gitee.com/lordy/mulan-to-block-example)。

![示例图片](../截图/木兰转Blockly.jpg)
