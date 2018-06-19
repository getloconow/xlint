import click
import json
from typing import List


def filter_pylint(data: str, ranges: list) -> None:
    lines: List[str] = data.splitlines()
    required: List[str] = lines[1:-2]
    required = list(filter(lambda x: not x.startswith('***'), required))
    required = list(filter(lambda x: not x.rstrip() == '', required))
    selected_lines: list = []
    for i, j in ranges:
        selected_lines += list(range(i, j + 1))
    selected_lines_set: set = set(selected_lines)
    linenumber: int
    for line in required:
        try:
            linenumber, _ = list(map(int, line.split(':')[-2].split(',')))
        except IndexError:
            continue
        if linenumber in selected_lines_set:
            print("\t", line)


def filter_mypy(data: str, ranges: list, file: str) -> None:
    lines: List[str] = data.splitlines()

    # required: List[str] = lines[1:-2]
    required = list(filter(lambda x: not x.startswith('***'), lines))
    required = list(filter(lambda x: not x.rstrip() == '', required))
    selected_lines: list = []
    for i, j in ranges:
        selected_lines += list(range(i, j + 1))
    selected_lines_set: set = set(selected_lines)
    linenumber: int
    for line in required:
        try:
            splitted = line.split(':')
            # print(splitted[0].strip() == file.strip(), splitted[0].strip(), file.strip())
            linenumber = int(splitted[-3])
            if splitted[0].strip() != file.strip():
                # print(line, linenumber)
                continue
            
        except BaseException:
            continue
        # print(splitted[0], file)
        if linenumber in selected_lines_set:
            print("\t", line)
    pass


@click.command()
@click.option('--mypy/--no-mypy', default=False, help='Pylint enable')
@click.option('--pylint/--no-pylint', default=False, help='Pylint enable')
@click.option('--file', default=False, help='Pylint enable')
@click.option('--data', help='Pylint enable')
@click.option('--ranges', help='Pylint enable')
def main(data: str='', ranges: str='', file: str = '',
         pylint: bool=False, mypy: bool=False) -> None:
    print(ranges)
    ranges_list: list = json.loads(ranges)
    # print(ranges)
    if pylint:
        filter_pylint(data, ranges_list)
    if mypy:
        filter_mypy(data, ranges_list, file)


if __name__ == '__main__':
    main()
