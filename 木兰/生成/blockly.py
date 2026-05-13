import ast
from xml.etree import ElementTree


算符表 = {
    ast.Add: "ADD",
    ast.Sub: "SUB",
    ast.Mult: "MULTIPLY",
    ast.Div: "DIVIDE",
}


class 代码生成器:
    def __init__(self):
        self.编号 = 0
        self.变量 = {}

    def 新编号(self):
        self.编号 += 1
        return f"mulan_{self.编号}"

    def 变量编号(self, 名称):
        if 名称 not in self.变量:
            self.变量[名称] = f"var_{len(self.变量) + 1}_{名称}"
        return self.变量[名称]

    def 生成(self, 节点):
        self.收集变量(节点)
        根 = ElementTree.Element("xml", {"xmlns": "http://www.w3.org/1999/xhtml"})
        变量列表 = ElementTree.SubElement(根, "variables")
        for 名称, 编号 in self.变量.items():
            变量 = ElementTree.SubElement(变量列表, "variable", {"id": 编号, "type": ""})
            变量.text = 名称

        首块 = self.语句链(节点.body)
        if 首块 is not None:
            根.append(首块)

        return '<?xml version="1.0" ?>\n' + ElementTree.tostring(根, encoding="unicode")

    def 收集变量(self, 节点):
        for 子节点 in ast.walk(节点):
            if isinstance(子节点, ast.Name) and isinstance(子节点.ctx, (ast.Store, ast.Load)):
                if 子节点.id not in ("print", "println", "range"):
                    self.变量编号(子节点.id)

    def 语句链(self, 语句列表):
        首块 = None
        当前 = None
        for 语句 in 语句列表:
            块 = self.语句(语句)
            if 块 is None:
                continue
            if 首块 is None:
                首块 = 块
            else:
                下个 = ElementTree.SubElement(当前, "next")
                下个.append(块)
            当前 = 块
        return 首块

    def 语句(self, 节点):
        if isinstance(节点, ast.Assign) and len(节点.targets) == 1 and isinstance(节点.targets[0], ast.Name):
            return self.赋值块(节点.targets[0].id, self.表达式(节点.value))

        if isinstance(节点, ast.AugAssign) and isinstance(节点.target, ast.Name):
            运算 = ElementTree.Element("block", {"id": self.新编号(), "type": "math_arithmetic"})
            ElementTree.SubElement(运算, "field", {"name": "OP"}).text = 算符表.get(type(节点.op), "ADD")
            值A = ElementTree.SubElement(运算, "value", {"name": "A"})
            值A.append(self.变量块(节点.target.id))
            值B = ElementTree.SubElement(运算, "value", {"name": "B"})
            值B.append(self.表达式(节点.value))
            return self.赋值块(节点.target.id, 运算)

        if isinstance(节点, ast.Expr) and isinstance(节点.value, ast.Call):
            调用 = 节点.value
            if isinstance(调用.func, ast.Name) and 调用.func.id in ("print", "println") and 调用.args:
                块 = ElementTree.Element("block", {"id": self.新编号(), "type": "text_print"})
                值 = ElementTree.SubElement(块, "value", {"name": "TEXT"})
                值.append(self.表达式(调用.args[0]))
                return 块

        if isinstance(节点, ast.For) and isinstance(节点.target, ast.Name):
            return self.for块(节点)

        raise NotImplementedError(f"暂不支持生成 Blockly XML：{type(节点).__name__}")

    def 赋值块(self, 名称, 值块):
        块 = ElementTree.Element("block", {"id": self.新编号(), "type": "variables_set"})
        ElementTree.SubElement(
            块, "field", {"id": self.变量编号(名称), "name": "VAR", "variabletype": ""}
        ).text = 名称
        值 = ElementTree.SubElement(块, "value", {"name": "VALUE"})
        值.append(值块)
        return 块

    def for块(self, 节点):
        块 = ElementTree.Element("block", {"id": self.新编号(), "type": "controls_for"})
        ElementTree.SubElement(块, "field", {"name": "VAR"}).text = 节点.target.id

        起始, 结束, 步长 = self.range参数(节点.iter)
        for 名称, 值节点 in (("FROM", 起始), ("TO", 结束), ("BY", 步长)):
            值 = ElementTree.SubElement(块, "value", {"name": 名称})
            值.append(self.表达式(值节点))

        语句 = ElementTree.SubElement(块, "statement", {"name": "DO"})
        子链 = self.语句链(节点.body)
        if 子链 is not None:
            语句.append(子链)
        return 块

    def range参数(self, 节点):
        if not (
            isinstance(节点, ast.Call)
            and isinstance(节点.func, ast.Name)
            and 节点.func.id == "range"
            and 1 <= len(节点.args) <= 3
        ):
            raise NotImplementedError("Blockly for 块目前仅支持 range 形式")

        if len(节点.args) == 1:
            起始 = ast.Constant(value=0)
            结束 = self.排除上限转包含上限(节点.args[0])
            步长 = ast.Constant(value=1)
        elif len(节点.args) == 2:
            起始 = 节点.args[0]
            结束 = self.排除上限转包含上限(节点.args[1])
            步长 = ast.Constant(value=1)
        else:
            起始 = 节点.args[0]
            结束 = self.排除上限转包含上限(节点.args[1])
            步长 = 节点.args[2]
        return 起始, 结束, 步长

    def 排除上限转包含上限(self, 节点):
        if (
            isinstance(节点, ast.BinOp)
            and isinstance(节点.op, ast.Add)
            and isinstance(节点.right, ast.Constant)
            and 节点.right.value == 1
        ):
            return 节点.left
        return ast.BinOp(left=节点, op=ast.Sub(), right=ast.Constant(value=1))

    def 表达式(self, 节点):
        if isinstance(节点, ast.Constant):
            if isinstance(节点.value, bool):
                块 = ElementTree.Element("block", {"id": self.新编号(), "type": "logic_boolean"})
                ElementTree.SubElement(块, "field", {"name": "BOOL"}).text = str(节点.value).upper()
                return 块
            if isinstance(节点.value, (int, float)):
                块 = ElementTree.Element("block", {"id": self.新编号(), "type": "math_number"})
                ElementTree.SubElement(块, "field", {"name": "NUM"}).text = str(节点.value)
                return 块
            if isinstance(节点.value, str):
                块 = ElementTree.Element("block", {"id": self.新编号(), "type": "text"})
                ElementTree.SubElement(块, "field", {"name": "TEXT"}).text = 节点.value
                return 块
        if isinstance(节点, ast.Name):
            return self.变量块(节点.id)

        if isinstance(节点, ast.BinOp):
            块 = ElementTree.Element("block", {"id": self.新编号(), "type": "math_arithmetic"})
            ElementTree.SubElement(块, "field", {"name": "OP"}).text = 算符表.get(type(节点.op), "ADD")
            值A = ElementTree.SubElement(块, "value", {"name": "A"})
            值A.append(self.表达式(节点.left))
            值B = ElementTree.SubElement(块, "value", {"name": "B"})
            值B.append(self.表达式(节点.right))
            return 块

        raise NotImplementedError(f"暂不支持生成 Blockly 表达式：{type(节点).__name__}")

    def 变量块(self, 名称):
        块 = ElementTree.Element("block", {"id": self.新编号(), "type": "variables_get"})
        ElementTree.SubElement(
            块, "field", {"id": self.变量编号(名称), "name": "VAR", "variabletype": ""}
        ).text = 名称
        return 块
