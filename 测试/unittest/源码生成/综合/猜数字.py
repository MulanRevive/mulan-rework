import sys, cmd; from random import randrange

class 猜数字(cmd.Cmd):
    intro, prompt = "我想了个 100 之内的数，猜猜是几？", '请猜吧: '
    想的 = randrange(1000) // 10

    def default(self, 行):
        try:
            数 = int(行)
        except ValueError as 例外:
            print(行 + " 不是数，请再试")
            return
        self.比较(数)

    def 比较(self, 数):
        if 数 == self.想的:
            print("中了!")
            sys.exit()
        print("太大了!" if 数 > self.想的 else "太小了!")

猜数字().cmdloop()