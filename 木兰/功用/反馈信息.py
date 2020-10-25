import re, sys, traceback

运行时木兰路径 = "site-packages/木兰/"
if sys.platform == 'win32':
    运行时木兰路径 = 运行时木兰路径.replace('/', '\\')

def 反馈信息(例外, 源码文件=None):
    提神符 = " 😰 "
    if sys.platform == 'win32':
        提神符 = "（>﹏<）"
    类型 = 例外.__class__.__name__
    原信息 = str(例外)
    exc_type, exc_value, 回溯信息 = sys.exc_info()
    各层 = traceback.extract_tb(回溯信息)
    # print(repr(各层))
    信息 = 提神符 + 提示(类型, 原信息)
    最高层号 = len(各层) - 1
    for 层号 in range(最高层号, -1, -1):
        层 = 各层[层号]
        文件名 = 层.filename
        if 文件名.find(运行时木兰路径) > 0:
            continue

        行信息 = f'见第{层.lineno}行'
        行内容 = 层.line
        if 源码文件 == None and 文件名 == "【标准输入】":
            return f"{信息}，{行信息}"
        else:
            # 在第二层前显示
            if 层号 == 最高层号 - 1:
                信息 += "\n调用层级如下"

            if 文件名 == 源码文件:
                信息 += "\n" + 行信息 + '：' + 行内容
            else:
                信息 += f"\n“{文件名}”第{层.lineno}行：{行内容}"
    return 信息

def 提示(类型, 原信息):
    if 类型 == 'NameError':
        return re.sub(r"name '(.*)' is not defined", r"请先定义‘\1’再使用", 原信息)
    elif 类型 == 'ZeroDivisionError':
        return "请勿除以零"
    elif 类型 == 'RecursionError':
        return "递归过深。请确认: 1、的确需要递归 2、递归的收敛正确"
    elif 类型 == 'UnboundLocalError':
        return re.sub(
            r"local variable '(.*)' referenced before assignment",
            r"请先对本地变量‘\1’赋值再引用",
            原信息)
    elif 类型 == 'KeyError':
        return "字典中不存在此键：" + 原信息
    elif 类型 == 'TypeError':
        模式 = 'can only concatenate str \(not "(.*)"\) to str'
        if re.match(模式, 原信息):
            return re.sub(模式, r'字符串只能拼接字符串，请将“\1”先用 str() 转换', 原信息)
    elif 类型 == 'IndexError' and 原信息 == "list index out of range":
        return "取列表内容时，索引超出范围"
    elif 类型 == 'AttributeError':
        return "需要添加此属性：" + 原信息 + "\n参考：https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit"
    elif 类型 == 'FileNotFoundError':
        return re.sub(r"\[Errno 2\] No such file or directory: '(.*)'",
            r"没找到文件或路径：‘\1’",
            原信息)
    return 类型 + "：" + 原信息
