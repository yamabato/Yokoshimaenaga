#encoding: utf-8

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if len(self.stack) == 0: return False, -1

        return True, self.stack.pop()
    
    def get(self):
        if len(self.stack) == 0: return False, -1

        return True, self.stack[-1]

    def clear(self):
        self.stack = []

    def length(self):
        return len(self.stack)

class Stacks:
    def __init__(self):
        self.stacks = [Stack()]

    def make_new_stack(self):
        self.stacks.append(Stack())

    def push_value(self, sn, value):
        if sn < 0 or sn >= len(self.stacks) or (not isinstance(sn, int)): return False
        
        self.stacks[sn].push(value)
        return True

    def remove(self, sn):
        if sn < 0 or sn >= len(self.stacks) or (not isinstance(sn, int)): return False, -1

        stack = self.stacks[sn]
        return stack.pop()

    def copy(self, sn1, sn2):
        if sn1 < 0 or sn1 >= len(self.stacks) or (not isinstance(sn1, int)): return False
        if sn2 < 0 or sn2 >= len(self.stacks) or (not isinstance(sn2, int)): return False

        stack1 = self.stacks[sn1]
        stack2 = self.stacks[sn2]
        
        ok, value = stack1.get()
        if not ok: return False

        stack2.push(value)

        return True

    def get_length(self, sn):
        if sn < 0 or sn >= len(self.stacks) or (not isinstance(sn, int)): return False, -1

        stack = self.stacks[sn]
        return True, stack.length()

    def get_stack_number(self):
        return len(self.stacks)

    def clear(self, sn):
        if sn < 0 or sn >= len(self.stacks) or (not isinstance(sn, int)): return False

        self.stacks[sn].clear()
        return True
