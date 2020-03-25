import sys, cmd

class 木兰(cmd.Cmd):
    intro = "Welcome to ulang's REPL..\nType 'help' for more informations."
    prompt = '> '

    def do_quit(self, arg):
        sys.exit()

if __name__ == '__main__':
    木兰().cmdloop()
