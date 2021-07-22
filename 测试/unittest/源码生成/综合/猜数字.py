import sys, cmd, random

class 猜数字(cmd.Cmd):
    intro, prompt = "我想了个 100 之内的数，猜猜是几？", '请猜吧: '
    想的 = random.randrange(100)

    def default(self, 行):
        数 = int(行)
        if 数 > self.想的:
            print("太大了!")
        elif 数 < self.想的:
            print("太小了!")
        else:
            print("中了!")
            sys.exit()

猜数字().cmdloop()