#encoding: utf-8

import sys
import os

from vm import VM
from debugger import Debugger

help_text = """\
python3 run.py [Yokoshimaenaga_File.yse] [args]
"""

args = sys.argv
if len(args) == 1:
    print(help_text)
    sys.exit(-1)

file_name = args[1]
params = args[2:]

if not os.path.isfile(file_name):
    print(f"File {file_name} not found.")
    sys.exit(-1)

elif file_name[-4:] != ".yse":
    print("The file extension for Yokoshimaenaga File is .yse")
    sys.exit(-1)

with open(file_name, mode="r", encoding="utf-8") as f:
    code = f.read()

d = False
if "-d" in params: d = True

if d:
    debugger = Debugger(code)
    debugger.debug()
else:
    vm = VM(code)
    vm.run()
