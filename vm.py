#encoding: utf-8
import string

class VM:
    ZERO_REGISTER_NAME = "zr"
    ONE_REGISTER_NAME = "or"

    def __init__(self, code):
        self.code = code
        self.lines = self.code.split("\n")
        self.scan_labels()

        self.current_line_number = 0

        self.stack = []

        self.register_list = list(string.ascii_lowercase) + [ZERO_REGISTER_NAME, ONE_REGISTER_NAME]
        self.register_n = len(self.register_list)
        self.register_number = {name: rn for rn, name in enumerate(self.register_list)}
        self.register = [0 for i in range(len(self.register_list))]

        self.label = {}

    def set_register_value(self, rn, value):
        if rn < 0 or rn >= self.register_n:
            return False

        if not (isinstance(value, int) or isinstance(value, float)):
            return False

        if self.register_list[rn] in [ZERO_REGISTER_NAME, ONE_REGISTER_NAME]:
            return True

        self.register[rn] = value

        return True

    def set_label(self, name, number):
        self.label[name] = number

    def eval_value(self, value):
        #numerical value
        #integer
        if value.isdigit():
            return True, int(value)

        #float
        if value.replace(".", "", 1).isdigit():
            return True, float(value)

        #register name
        if value in self.register_list:
            return True, self.register_number[value]

        #register value
        if value[0] == "$" and value[1:] in self.register_list:
            return True, self.register[self.eval_value(value[1:])]

        #label name
        if value[0] == ":" and value[1:] in self.label:
            return True, self.label[value[1:]]

        else False, -1

    def scan_labels(self):
        for n, line in enumerate(self.lines):
            if len(line) == 1 and line[0][0] == ":":
                self.label[line[0][1:]] = n

    



