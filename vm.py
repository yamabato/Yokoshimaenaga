#encoding: utf-8
import string

class VM:
    ZERO_REGISTER_NAME = "zr"
    ONE_REGISTER_NAME = "or"
    def __init__(self):
        self.stack = []

        self.register_list = list(string.ascii_lowercase) + [ZERO_REGISTER_NAME, ONE_REGISTER_NAME]
        self.register_n = len(self.register_list)
        self.register_number = {name: rn for rn, name in enumerate(self.register_list)}
        self.register = [0 for i in range(len(self.register_list))]

    def set_register_value(self, rn, value):
        if rn < 0 or rn >= self.register_n:
            return False

        if not (isinstance(value, int) or isinstance(value, float)):
            return False

        if self.register_list[rn] in [ZERO_REGISTER_NAME, ONE_REGISTER_NAME]:
            return True

        self.register[rn] = value

        return True

