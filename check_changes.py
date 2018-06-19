# from get_ranges import get_ranges
import json
from io import BytesIO
import tokenize


def get_ranges(data: str) -> list:
    x = tokenize.tokenize(BytesIO(data.encode('utf-8')).readline)
    stack = []
    indentable = { 'def', 'class', 'with', 'if',
                   'while', 'for', 'try', 'except', 'elif', 'else'}
    found_indentable: bool = False
    expecting_newline: bool = False
    allowed_blocks: list = []
    ranges = []
    for token in x:
        #     print(token)?
        #     print(token)
        if found_indentable:
            if stack and stack[-1].string == 'if' and token.string == 'else':
                expecting_newline = False
                found_indentable = False
            if expecting_newline:

                if token.type == 4:
                    expecting_newline = False
                continue
            if token.type == 4:
                continue

            if token.type == 5:
                found_indentable = False
            continue

        if token.string in indentable:
            if token.string in {'def', 'class'}:
                allowed_blocks += [token]
            stack.append(token)
            found_indentable = True
            expecting_newline = True
        if token.type == 6:
            top = stack.pop()
    #         print(list(map(lambda x:x.string, allowedBlocks)))
            if top.string in {'def', 'class'}:
                allowed_blocks.pop()
    #             print('from {} to {}\n'.format(top.start[0], token.start[0]))
                ranges.append((top.start[0], token.start[0]))
            elif allowed_blocks and allowed_blocks[-1].string == 'class':
                raise SyntaxError
            elif allowed_blocks and allowed_blocks[-1].string != 'def':
                ranges.append((top.start[0], token.start[0]))

    lines = { i: (i, i) for i in range(1, ranges[-1][-1] + 1)}
    for i in reversed(ranges):
        for j in range(i[0], i[1]):
            lines[j] = i[0], i[1]-1
    return lines


def get_functions(data: str, required: list) -> None:
    ranges = get_ranges(data)
    # print(ranges)
    # print(required)

    final_ranges = set([ ranges[i] for i in required])
    print(json.dumps(list(final_ranges)))
