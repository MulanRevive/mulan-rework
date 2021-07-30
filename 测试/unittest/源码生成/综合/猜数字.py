import sys, cmd; from 随机数 import 随机范围数

class 猜数字(cmd.Cmd):
    intro, prompt = "我想了个 100 之内的数，猜猜是几？", '请猜吧: '
    想的 = 随机范围数(1000) / 10

    def default(self, 行):
        数 = int(行)
        if 数 == self.想的:
            print("中了!")
            sys.exit()
        print("太大了!" if 数 > self.想的 else "太小了!")

猜数字().cmdloop()