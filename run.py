#encoding: utf-8

import sys
import os

from vm import VM

help_text == """\
python3 run.py [Yokoshimaenaga_File.yse]
"""

args = sys.argv()
if len(args) == 1:
    print(help_text)
    sys.exit(-1)

file_name = args[1]

if not os.path.isfile(file_name):
    print(f"File {file_name} not found.")
    sys.exit(-1)

with open(file_name, mode="r", encoding="utf-8") as f:
    code = f.read()

vm = VM(code)
vm.run()
