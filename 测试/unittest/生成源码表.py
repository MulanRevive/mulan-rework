from pathlib import Path

源码目录 = Path("测试/unittest/源码生成/")

# 待做：重现木兰的 `测试.unittest.Python到木兰` 应运行以下测试
原始木兰未过 = {
    Path("测试/unittest/源码生成/函数/变长指名参数.py"): "TypeError: can only concatenate str (not \"arg\") to str",
    Path("测试/unittest/源码生成/类型/属性.py"): "NameError: name 'decorator_list' is not defined",
    Path("测试/unittest/源码生成/流程控制/try.py"): "AttributeError: 'str' object has no attribute '_fields'",
    Path("测试/unittest/源码生成/算法/排序/冒泡.py"): "UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 6: illegal multibyte sequence",
    Path("测试/unittest/源码生成/综合/猜数字.py"):  "UnicodeDecodeError: 'gbk' codec can't decode byte 0xb0 in position 30: illegal multibyte sequence",
}

python源码表 = {}
木兰源码表 = {}

for 完整路径 in list(源码目录.glob('**/*.py')):
    if 完整路径 not in 原始木兰未过:
        python文件名 = str(完整路径)[:-len(完整路径.suffix)]
        python路径 = python文件名 + '.py'
        with open(python路径, 'r', encoding='utf-8') as f:
            python源码 = f.read()

        木兰路径 = python文件名 + ".ul"
        if Path(木兰路径).exists():
            with open(木兰路径, 'r', encoding='utf-8') as f:
                木兰源码 = f.read()
        else:
            木兰源码 = python源码

        python源码表[python路径] = python源码
        木兰源码表[python路径] = 木兰源码