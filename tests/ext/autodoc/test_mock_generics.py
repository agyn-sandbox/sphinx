"""
    tests.ext.autodoc.test_mock_generics
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for mocked generics handling.
"""

from typing import List, Mapping, TypeVar

from sphinx.ext.autodoc.mock import _MockModule


T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


def _make_mock() -> _MockModule:
    return _MockModule('mylib')


def test_mock_generic_typevar_repr() -> None:
    module = _make_mock()
    thing = module.Thing

    specialized = thing[T]

    assert repr(specialized) == 'mylib.Thing[T]'


def test_mock_generic_nested_typing_repr() -> None:
    module = _make_mock()
    thing = module.Thing

    specialized = thing[List[T]]

    assert repr(specialized) == 'mylib.Thing[typing.List[T]]'


def test_mock_generic_mapping_repr() -> None:
    module = _make_mock()
    thing = module.Thing

    specialized = thing[Mapping[K, V]]

    assert repr(specialized) == 'mylib.Thing[typing.Mapping[K, V]]'


def test_mock_generic_multiple_typevars_repr() -> None:
    module = _make_mock()
    thing = module.Thing

    specialized = thing[K, V]

    assert repr(specialized) == 'mylib.Thing[K, V]'


def test_mock_generic_nested_mock_repr() -> None:
    module = _make_mock()
    thing = module.Thing

    inner = thing[T]
    specialized = thing[inner]

    assert repr(inner) == 'mylib.Thing[T]'
    assert repr(specialized) == 'mylib.Thing[mylib.Thing[T]]'
