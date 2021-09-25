#encoding: utf-8

from vm import VM

import sys

class Debugger(VM):
    def debug(self):
        r = False

        l = len(str(len(self.lines) + 1))
        while True:
            if r:
                if self.current_line_number < len(self.lines):
                    line = self.lines[self.current_line_number]
                    ok = self.eval_line(line)
                    if not ok:
                        self.error()
                else:
                    r = False
                    print()

            else:
                if self.current_line_number >= len(self.lines):
                    self.current_line_number = len(self.lines) - 1

                line = self.lines[self.current_line_number]
                inp = input(f"({str(self.current_line_number + 1).zfill(l)}/{len(self.lines)})> {line}:")
               
                cmd = inp.split()[0] if len(inp) != 0 else ""
                args = inp.split()[1:]

                if cmd in ["", "next", "n"]:
                     if self.current_line_number < len(self.lines):
                        line = self.lines[self.current_line_number]
                        ok = self.eval_line(line)
                        if not ok:
                            self.error()
     
                elif cmd in ["info", "i"]:
                    self.show_info(args)

                elif cmd in ["quit", "q"]: sys.exit(-1)

                elif cmd in ["run", "r"]: r = True

                elif cmd in ["set"]:
                    self.set_value(args)

                elif cmd in ["show", "s"]:
                    self.show_value(args)

                elif cmd in ["do", "d"]:
                    self.do(args)

                print()


    def show_info(self, args):
        #line number
        #stacks
        #registers
        #code
        #label

        if args == []:
            args = ["ln", "st", "rg", "cd", "lb"]

        if "ln" in args:
            print("LINE:", self.current_line_number + 1)

        if "st" in args:
            print("STACK")
            for n, stack in enumerate(self.stacks.stacks):
                print(str(n).ljust(len(str(len(self.stacks.stacks)))) + ": " + (" ".join(map(str, stack.stack)) if stack.stack else "EMPTY"))

        if "rg" in args:
            print("REGISTER")

            for name in self.REGISTER_LIST:
                print(name.ljust(2) + ":", self.eval_value("$"+name)[1])

        if "cd" in args:
            print("CODE: " + self.lines[self.current_line_number])

        if "lb" in args:
            for name, l in self.label.items():
                print(name.ljust(max([len(n) for n in self.label.keys()])) + ":", l)

    def set_value(self, args):
        if len(args) != 2: return

        name, value = args

        if name == "ln":
            if value.isdigit() and int(value) > 0 and int(value) <= len(self.lines):
                self.current_line_number = int(value) - 1

    def show_value(self, args):
        l = max([len(str(arg)) for arg in args])
        for arg in args:
            ok, value = self.eval_value(arg)

            if ok:
                print(arg.ljust(l) + ":", value)
            else:
                print(arg.ljust(l) + ":", arg)

    def do(self, args):
        l = " ".join(args)
        cln = self.current_line_number
        ok = self.eval_line(l)

        if not ok:
            print("An ERROR occurred")
        self.current_line_number = cln


