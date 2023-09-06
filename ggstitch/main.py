# GGStitch
# Takes a JavaScript file and uses comments written as "// !Require path/to/script.js" to insert required script
# It allows for splitting one big file into seperate files and joining them before runtime

import sys, os
from os import path
from time import time
from math import floor

def printUsage():
    print("Usage: ggstitch [mainfile=main.js|index.js|script.js] [outfile=out.js] [verbose=0]")
    exit(1)

try:
    sys.argv[1]
    if sys.argv[1] == "=":
        if path.exists("main.js"): sys.argv[1] = "main.js"
        elif path.exists("index.js"): sys.argv[1] = "index.js"
        elif path.exists("script.js"): sys.argv[1] = "script.js"
except IndexError:
    if path.exists("main.js"): sys.argv.append("main.js")
    elif path.exists("index.js"): sys.argv.append("index.js")
    elif path.exists("script.js"): sys.argv.append("script.js")
    else: printUsage()

try:
    sys.argv[2]
    if sys.argv[2] == "=":
        sys.argv[2] = "out.js"
except IndexError:
    sys.argv.append("out.js")

try:
    sys.argv[3] = int(sys.argv[3])
except IndexError:
    sys.argv.append(0)

sys.argv[3] = bool(sys.argv[3])

def getFile(loc):
    if not path.exists(loc):
        print(f"\033[91m\033[1mFile not found: {loc}")
        exit(1)
    res = ""
    with open(loc, 'r') as file:
        res = file.read()
        file.close()
    return res

milli = lambda: time() * 1000

stitchCount = 0

def assemble(code, dirl):
    global stitchCount
    code = code.replace('\r', '')
    assembled = ""
    for line in code.split('\n'):
        if line[:11] == "// !Require":
            loc = path.join(dirl, line[12:])
            if sys.argv[3]:
                assembled += "// "
                assembled += path.basename(loc)
            assembled += "\n"
            assembled += assemble(getFile(loc), path.dirname(loc))
            assembled = assembled.rstrip('\n')
        else:
            assembled += line
        assembled += '\n'
    stitchCount += 1
    return assembled

start = milli()
mainfile = assemble(getFile(sys.argv[1]), os.getcwd())
end = milli()

with open(sys.argv[2], 'w') as file:
    file.write(mainfile)
    file.close()

print(f"Stitched {stitchCount} files in {round(end - start, 2)}ms")
