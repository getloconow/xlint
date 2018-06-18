import sys
from check_changes import get_functions

diff = sys.argv[1]
_file = sys.argv[2]

# print(_file)
if diff == '':
    print([])
    exit(0)
lines = diff.splitlines()

meta = lines[:3]
lines = lines[2:]

if lines[-1][0] == '\\':
    lines = lines[:-1]
ln = 0
lastline_startedwith = ''
selected: list = []
final: list = []
for line in lines:
    startingwith: str = line[0]
    if startingwith == '@':
        delinfo, addinfo = line.strip('@').strip().split(' ')
        try:
            start1, count1 = list(map(int, addinfo.split(',')))
        except IndexError as e:
            start1 = list(map(int, addinfo.split(',')))[0]
        ln = start1
        continue
    elif startingwith == '+' and lastline_startedwith == '-':
        selected += [ ln]
        final[-1] = (line, ln)
    elif startingwith == '+':
        if line[1:].strip() != '':

            selected += [ ln]
            final += [ (line, ln)]
    elif startingwith == '-':
        ln -= 1
        final += [(line, '*', ln)]
    else:
        final += [ (line, ln)]

    lastline_startedwith = startingwith
    ln += 1


with open(_file) as file:
    content: str = file.read()
    get_functions(content, selected)
