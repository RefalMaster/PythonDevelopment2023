import cmd

class CommandLine(cmd.Cmd):
    def do_something(self, arg):
        print('Just doing something...')

    def do_exit(self, arg):
        return 1

cmdline = CommandLine()
cmdline.cmdloop()