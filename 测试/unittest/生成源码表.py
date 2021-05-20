import os

源码目录 = "测试/unittest/源码生成/"

原始木兰未过 = {
    "测试/unittest/源码生成/函数/变长指名参数": "TypeError: can only concatenate str (not \"arg\") to str",
    "测试/unittest/源码生成/类型/属性": "NameError: name 'decorator_list' is not defined",
}

python源码表 = {}
木兰源码表 = {}

for 路径, 目录名, 所有文件 in os.walk(源码目录):
    for 文件 in 所有文件:
        文件名 = os.path.splitext(os.path.join(路径, 文件))
        if 文件名[1] == '.py' and 文件名[0] not in 原始木兰未过:
            python文件名 = 文件名[0]
            python路径 = python文件名 + '.py'
            with open(python路径, 'r', encoding='utf-8') as f:
                python源码 = f.read()

            木兰路径 = python文件名 + ".ul"
            if os.path.isfile(木兰路径):
                with open(木兰路径, 'r', encoding='utf-8') as f:
                    木兰源码 = f.read()
            else:
                木兰源码 = python源码

            python源码表[python路径] = python源码
            木兰源码表[python路径] = 木兰源码