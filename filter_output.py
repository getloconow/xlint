import click
import json


def filter_pylint(data: str, ranges: list) -> None:
    pass


def filter_mypy(data: str, ranges: list) -> None:
    pass


@click.command()
@click.option('--mypy/--no-mypy', default=False, help='Pylint enable')
@click.option('--pylint/--no-pylint', default=False, help='Pylint enable')
@click.option('--data', help='Pylint enable')
@click.option('--ranges', help='Pylint enable')
def main(data: str = '', ranges: str = '',
         pylint: bool=False, mypy: bool=False) -> None:
    ranges_list: list = json.loads(ranges)
    print(ranges)
    if pylint:
        filter_pylint(data, ranges_list)
    if mypy:
        filter_mypy(data, ranges_list)


if __name__ == '__main__':
    main()
