"""Decorators mimicking external wrappers for napoleon tests."""

import functools


def wraps_init(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def bare_init(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    return wrapper


def decorate_class(cls):
    base_init = cls.__init__

    @functools.wraps(base_init)
    def replacement(self, *args, **kwargs):  # type: ignore[override]
        base_init(self, *args, **kwargs)

    cls.__init__ = replacement  # type: ignore[assignment]
    return cls
