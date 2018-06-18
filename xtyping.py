""" Syntax sugar """
from typing import Callable, Type


def throws(*args: Type[BaseException]) -> Callable:
    def wrapper(function: Callable) -> Callable:
        return function
    return wrapper
