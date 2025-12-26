"""Helper decorators for napoleon tests.

These decorators live in a separate module so wrapped callables have a
different global namespace from the classes they decorate.  This mirrors the
real-world scenario where decorators are imported from third-party modules.
"""

import functools
from typing import Callable, TypeVar

F = TypeVar('F', bound=Callable[..., object])
T = TypeVar('T', bound=type)


def wraps_init(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


def bare_init(func: F) -> F:
    def wrapper(*args: object, **kwargs: object) -> object:
        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    return wrapper  # type: ignore[return-value]


def decorate_class(cls: T) -> T:
    base_init = cls.__init__

    @functools.wraps(base_init)
    def replacement(self, *args: object, **kwargs: object) -> None:  # type: ignore[override]
        base_init(self, *args, **kwargs)

    cls.__init__ = replacement  # type: ignore[assignment]
    return cls
