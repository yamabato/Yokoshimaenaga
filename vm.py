#encoding: utf-8
from stack import Stack, Stacks

import string
import math
import sys

class VM:
    ZERO_REGISTER_NAME = "zr"
    ONE_REGISTER_NAME = "or"

    OPERATIONS = [
        "set",
        "add", "sub", "mul", "div", "pow", "mod",
        "and", "or", "xor",
        "equ", "neq", "gtr", "lss", "geq", "leq",
        "log",
        "int", "flt",
        "psh", "pop", "clr", "len", "cpy", "mks", "stn",
        "jmp", "gln",
        "chr", "prt", "gch", "gtx",
    ]

    OPERATORS = [
        "add", "sub", "mul", "div", "pow", "mod",
        "and", "or", "xor",
        "equ", "neq", "gtr", "lss", "geq", "leq",
    ]

    THREE_PARAMETERS = [
        "add", "sub", "mul", "div", "pow", "mod",
        "and", "or", "xor",
        "equ", "neq", "gtr", "lss", "geq", "leq",
        "log",
    ]

    TWO_PARAMETERS = [
        "set",
        "int", "flt",
        "psh", "pop", "len", "cpy",
        "jmp", 
        "prt", "gtx",
    ]

    ONE_PARAMETER = [
        "clr", "stn",
        "gln",
        "chr", "gch",
    ]
    
    NO_PARAMETERS = [
        "mks",  
    ]

    PARAM_NUMBER = {o: 3 for o in THREE_PARAMETERS}
    PARAM_NUMBER.update({o: 2 for o in TWO_PARAMETERS})
    PARAM_NUMBER.update({o: 1 for o in ONE_PARAMETER})
    PARAM_NUMBER.update({o: 0 for o in NO_PARAMETERS})

    REGISTER_LIST = list(string.ascii_lowercase) + [ZERO_REGISTER_NAME, ONE_REGISTER_NAME]
    REGISTER_N = len(REGISTER_LIST)
    REGISTER_NUMBER = {name: rn for rn, name in enumerate(REGISTER_LIST)}
 
    def __init__(self, code):
        self.code = code
        self.lines = self.code.split("\n")

        self.current_line_number = 0

        self.stacks = Stacks()

        self.register = [0 for i in range(len(self.REGISTER_LIST))]
        self.register[self.REGISTER_LIST.index("or")] = 1

        self.label = {}
        self.scan_labels()

    def set_register_value(self, register, value):
        ok, rn = self.eval_value(register)
        if not ok: return False

        return self.set_register_number_value(rn, value)

    def set_register_number_value(self, rn, value):
        if rn < 0 or rn >= self.REGISTER_N:
            return False

        if not (isinstance(value, int) or isinstance(value, float)):
            return False

        if self.REGISTER_LIST[rn] in [self.ZERO_REGISTER_NAME, self.ONE_REGISTER_NAME]:
            return True

        self.register[rn] = value

        return True

    def set_label(self, label, number):
        self.label[label[1:]] = number

    def label_to_line_number(self, label):
        if label[1:] not in self.label:
            return False, -1

        return True, self.label[label[1:]]

    def eval_value(self, value):
        #numerical value
        #integer
        if value.isdigit():
            return True, int(value)

        #float
        if value.replace(".", "", 1).isdigit():
            return True, float(value)

        #register name
        if value in self.REGISTER_LIST:
            return True, self.REGISTER_NUMBER[value]

        #register value
        if value[0] == "$" and value[1:] in self.REGISTER_LIST:
            ok, rn = self.eval_value(value[1:])
            if not ok: return False
            return True, self.register[rn]

        #label name
        if value[0] == ":" and value[1:] in self.label:
            return self.label_to_line_number(value)

        return False, -1

    def scan_labels(self):
        for n, line in enumerate(self.lines):
            line = line.split()
            if len(line) == 1 and line[0][0] == ":":
                self.set_label(line[0], n)

    def error(self):
        print(f"An ERROR occurred on line {self.current_line_number}.")

        return False

    def increment_line_number(self):
        self.current_line_number += 1

    def run(self):
        while self.current_line_number < len(self.lines):
            line = self.lines[self.current_line_number]
            ok = self.eval_line(line)
            if not ok:
                self.error()
                return False
        return True

    def eval_line(self, line):
        if len(line) == 0:
            self.increment_line_number()
            return True

        if line[0][0] in [":", ";"]:
            self.increment_line_number()
            return True
        
        line = line.split()
        operation = line[0]

        if operation not in self.OPERATIONS:
            return False

        params = line[1:]
        param_n = len(params)

        if param_n != self.PARAM_NUMBER[operation]:
            return False
        
        ok = self.execute_operation(operation, *params)
        self.increment_line_number()

        return ok
        
    def execute_operation(self, operation, p1=None, p2=None, p3=None):
        if operation in self.OPERATORS:
            ok1, v1 = self.eval_value(p1)
            ok2, v2 = self.eval_value(p2)

            if not (ok1 & ok2): return False

            r1 = p3
            v = -1

            if operation == "add":
                v = v1 + v2
            elif operation == "sub":
                v = v1 - v2
            elif operation == "mul":
                v = v1 * v2
            elif operation == "div":
                if v2 == 0: return False
                v = v1 / v2
            elif operation == "pow":
                v = v1 ** v2
            elif operation == "mod":
                if v2 == 0: return False
                v = v1 % v2

            elif operation == "and":
                v = v1 & v2
            elif operation == "or":
                v = v1 | v2
            elif operation == "xor":
                v = v1 ^ v2

            elif operation == "equ":
                v = int(v1 == v2)
            elif operation == "neq":
                v = int(v1 != v2)
            elif operation == "gtr":
                v = int(v1 > v2)
            elif operation == "lss":
                v = int(v1 < v2)
            elif operation == "geq":
                v = int(v1 >= v2)
            elif operation == "leq":
                v = int(v1 <= v2)
            
            return self.set_register_value(r1, v)
        
        elif operation == "set":
            ok, v1 = self.eval_value(p1)
            if not ok: return False

            r1 = p2

            return self.set_register_value(r1, v1)

        elif operation == "log":
            ok1, v1 = self.eval_value(p1)
            ok2, v2 = self.eval_value(p2)
            if not (ok1 & ok2): return False

            r1 = p3

            v = math.log(v2, v1)

            return self.set_register_value(r1, v)
        
        elif operation in ["int", "flt"]:
            ok, v1 = self.eval_value(p1)
            if not ok: return False
            
            r1 = p2

            if operation == "int":
                v = int(v1)

            elif operation == "flt":
                v = int(v1)

            return self.set_register_value(r1, v)

        elif operation == "jmp":
            ok1, v1 = self.eval_value(p1)
            ok2, l1 = self.eval_value(p2)

            if not (ok1 & ok2): return False

            if v1 == 1:
                self.current_line_number = l1
            else:
                pass

            return True

        elif operation == "gln":
            r1 = p1
            return self.set_register_value(r1, self.current_line_number)

        elif operation == "psh":
            ok1, s1 = self.eval_value(p1)
            ok2, v1 = self.eval_value(p2)
            
            if not (ok1 & ok2): return False
            
            return self.stacks.push_value(s1, v1)

        elif operation == "pop":
            ok, s1 = self.eval_value(p1)
            if not ok: return False

            r1 = p2

            ok, v = self.stacks.remove(s1)
            if not ok: return False

            return self.set_register_value(r1, v)

        elif operation == "len":
            ok, s1 = self.eval_value(p1)
            if not ok: return False

            ok, v = self.stacks.get_length(s1)
            if not ok: return False

            r1 = p2

            return self.set_register_value(r1, v)

        elif operation == "clr":
            ok, s1 = self.eval_value(p1)
            if not ok: return False

            return self.stacks.clear(s1)

        elif operation == "cpy":
            ok1, s1 = self.eval_value(p1)
            ok2, s2 = self.eval_value(p2)
            if not (ok1 & ok2): return False

            return self.stacks.copy(s1, s2)

        elif operation == "mks":
            self.stacks.make_new_stack()
            return True

        elif operation == "stn":
            r1 = p1
            v = self.stacks.get_stack_number()

            return self.set_register_value(r1, v)

        elif operation == "chr":
           ok, v1 = self.eval_value(p1)
           if not ok: return False

           print(chr(v1), end="")
           return True

        elif operation == "prt":
           ok1, s1 = self.eval_value(p1)
           ok2, v1 = self.eval_value(p2)

           if not (ok1 & ok2): return False
           if not isinstance(v1, int): return False

           for i in range(v1):
               ok, v = self.stacks.remove(s1)
               if not ok: return False

               print(chr(v), end="")

           return True

        elif operation == "gch":
           r1 = p1

           inp = input()

           if inp == "": v = -1
           else: v = ord(inp[0])

           self.set_register_value(r1, v)

        elif operation == "gtx":
           ok, s1 = self.eval_value(p1)
           if not ok: return False

           r1 = p2
           inp = input()

           if inp == "":
               txt = [-1]
               v = 0
           else:
               txt = [ord(c) for c in reversed(inp)]
               v = len(inp)
           
           for c in txt:
               ok = self.stacks.push_value(s1, v)
               if not ok: return False

           return self.set_register_value(r1, v)

