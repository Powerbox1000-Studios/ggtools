# GGPatcher Takes a Sourcefile and Editedfile and outputs a Patchfile

import sys, json
from os import path
from difflib import Differ

def printUsage():
    print("Usage: ggpatch [srcfile] [editfile] [outfile?]")
    exit(1)

try:
    sys.argv[1]
    sys.argv[2]
except IndexError:
    printUsage()

try:
    sys.argv[3]
except IndexError:
    sys.argv.append("patch.json")

if not path.exists(sys.argv[1]):
    print("\033[91m\033[1msrcfile not found\033[0m")
elif not path.exists(sys.argv[2]):
    print("\033[91m\033[1meditfile not found\033[0m")

srcfile=""
editfile=""

with open(sys.argv[1], 'r') as file:
    srcfile = file.read()
    file.close()

with open(sys.argv[2], 'r') as file:
    editfile = file.read()
    file.close()

srcfile = srcfile.replace('\r', '')
srcfile = srcfile.split('\n')
editfile = editfile.replace('\r', '')
editfile = editfile.split('\n')

d = Differ()
diff = d.compare(srcfile, editfile)
ndiff = []
for item in diff:
    if item[0] == "+" or item[0] == " ": ndiff.append(item)

# Assemble patchfile
patchfile = []
for i, line in enumerate(ndiff):
    if line[0] == "+": patchfile.append([i + 1, line[2:]])

with open(sys.argv[3], 'w') as file:
    file.write(json.dumps(patchfile, sort_keys=True, indent=None, separators=(',', ':')))
    file.close()

print("Wrote patchfile!")
