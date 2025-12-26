"""Targets for napoleon decorator regression testing."""

from decorators import bare_init, decorate_class, wraps_init


class PlainInit:
    def __init__(self):
        """PlainInit.__init__"""
        pass


class WrapsDecoratedInit:
    @wraps_init
    def __init__(self):
        """WrapsDecoratedInit.__init__"""
        pass


class BareDecoratedInit:
    @bare_init
    def __init__(self):
        """BareDecoratedInit.__init__"""
        pass


@decorate_class
class DecoratedClassWithInit:
    @wraps_init
    def __init__(self):
        """DecoratedClassWithInit.__init__"""
        pass
