def talk():
    # 若无 end，则带换行，与系统有关，win 下是\r\n：
    # 参考: https://stackoverflow.com/questions/8220108/how-do-i-check-the-operating-system-in-python
    # if platform == "win32"
    print(2, end='')

def listen():
    print(3, end='')