import os
import sys
import click
from subprocess import getoutput
import imp
import json


try:
    imp.find_module('pylint')
    imp.find_module('pylint_django')
except ModuleNotFoundError as e:
    print('Requires pylint and pylint-django,\
    run : pip install pylint pylint-django')


COMMAND = ['pylint', "--load-plugins=pylint_django"]

LEVELS = {
    1: ['wrong-import-order',
        'ungrouped-imports',
        'invalid-name',
        'wrong-import-position',
        'missing-docstring',
        'bad-continuation',
        'bad-whitespace',
        'trailing-whitespace']
}
EDITORS = {'vscode'}


def write_vscode(commad: list, python: str=None) -> None:
    print('Make sure that you have installed pylint plugin for VSCODE.')
    try:
        os.makedirs('./.vscode/')
        file = open('./.vscode/settings.json', 'a')
        file.close()
    except FileExistsError:
        pass
    file = open('./.vscode/settings.json')
    try:
        content = file.read()
        file.close()
    except BaseException:
        content = "{}"
    config = json.loads(content)
    config['python.linting.pylintArgs'] = commad[1:]
    if python:
        config['python.pythonPath'] = str(os.path.join(python, 'python'))
    file = open('./.vscode/settings.json', 'w')
    file.write(json.dumps(config, indent=4))
    file.close()
    print('Changes written to ./.vscode/settings.json')


def write_config(command: list, editor: str, python: str=None) -> None:
    global EDITORS
    if editor not in EDITORS:
        raise NotImplementedError('No support for editor : ' + editor)
    if editor == 'vscode':
        write_vscode(command, python)


def run_cmd(python_command: list, command: list, name: str='') -> None:
    # print('Running test : {}'.format(name), end='\r')
    # print(' '.join(python_command + command))
    res = getoutput(' '.join(python_command + command))
    # message = '{} test out : '.format(name)
    # print(message)
    # print('='*len(message))
    print(res)


def run_checks(python_command: list, command: list, cmds: dict) -> None:
    if cmds['pylint']:
        run_cmd(python_command, command, 'Pylint')
    s = command[2]
    if cmds['mypy']:
        # s = s.replace("\\", "\\\\")
        # s = s.replace(" ", "\\ ")
        command = ['mypy', "--ignore-missing-imports",
                   "--follow-imports=silent", '--check-untyped-defs',
                   '--disallow-untyped-defs', '--quick-and-dirty', s]
        run_cmd(python_command, command, 'Mypi')


def run_or_exec(command: list, write: str, python: str, cmds: dict) -> None:
    if python:
        python_command = ["source "] + \
            [str(os.path.join(python, 'activate'))] + [" && "]
    else:
        python_command = []
    if not write:
        run_checks(python_command, command, cmds=cmds)
    else:
        write_config(command, write, python)


@click.command()
@click.option('-v', '--level', default=1, help='Strictness level', count=True)
@click.option('--write-config', default=False, help='Strictness level')
@click.option('--pylint/--no-pylint', default=False, help='Pylint enable')
@click.option('--mypy/--no-mypy', default=False, help='Pylint enable')
@click.argument('module', default=False)
@click.option('--python', default=False, help='Strictness level')
def exec(level: int=0, write_config: str='', module: str='', python: str='',
         pylint: bool=False, mypy: bool=False) -> None:
    global COMMAND
    cmds = {'pylint': pylint, 'mypy': mypy}
    if not module and not write_config:
        raise ModuleNotFoundError(
            'Specify module name. i.e. : ' + ' '.join(sys.argv) + ' {module}')
    if not write_config:
        s = module.replace("\\", "\\\\")
        s = s.replace(" ", "\\ ")
        COMMAND.append( s)
    if level in LEVELS:
        COMMAND += list(map(lambda x: '--disable ' + x, LEVELS[level]))
        run_or_exec(COMMAND, write_config, python, cmds=cmds)
    elif level == 'strict':
        run_or_exec(COMMAND, write_config, python, cmds=cmds)


if __name__ == '__main__':
    exec()
