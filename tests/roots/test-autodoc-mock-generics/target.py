from typing import List, Mapping, TypeVar

from mylib import Thing


T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class Foo(Thing[T]):
    """Simple generic subclass."""


class Bar(Thing[List[T]]):
    """Nested typing alias."""


class Baz(Thing[Mapping[K, V]]):
    """Mapping-based generic subclass."""


class Qux(Thing[K, V]):
    """Multiple type variables."""
