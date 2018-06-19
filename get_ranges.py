from collections import defaultdict
from typing import Generator
from xtyping import throws


@throws(BaseException, IndentationError)
def getScope(line: str, previous_depth: int,
             number: int, stack: list) -> tuple:
    spaces = 0
    line = line.rstrip()
    if line == '':
        return (previous_depth, False, False, stack[-1])
    for char in line:
        if char is ' ':
            spaces += 1
            continue
        break

    if spaces % 4 != 0:
        return (previous_depth, False, False, stack[-1])
    isFunction = False
    depth = spaces // 4
    ended: list = []
    if previous_depth > depth:
        ended = []

        try:
            for _ in range(previous_depth - depth):
                ended += [stack.pop()[2]]
        except IndexError:
            print(ended)
            print(line)
            pass
    if line.lstrip().startswith('def '):
        stack.append((depth, number, line))
        isFunction = True
    return (depth, True, isFunction, stack[-1] + tuple(ended))


def scopes(lines: list) -> Generator:
    depth = 0
    stack = [(0, 0, 'module')]
    for number, line in enumerate(lines):
        res = getScope('    ' + line, depth, number, stack)
        depth = res[0]
        yield res[3]


def get_ranges(data: str) -> dict:
    lines = data.splitlines()
    loc = list(scopes(lines))
    group: defaultdict = defaultdict(set)
    for no, line in enumerate(loc):
        group[line[2]].add(no)
        for i in line[3:]:
            group[i].add(no - 1)
    final = {}
    for vals in group.values():
        start = min(vals) + 1
        end = max(vals) + 1
        if end == start:
            end = None
        for i in vals:
            final[i + 1] = (start, end)
    return final
