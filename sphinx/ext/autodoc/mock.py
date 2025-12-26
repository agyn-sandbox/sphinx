"""
    sphinx.ext.autodoc.mock
    ~~~~~~~~~~~~~~~~~~~~~~~

    mock for autodoc

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import contextlib
import os
import re
import sys
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
from types import FunctionType, MethodType, ModuleType
from typing import Any, Generator, Iterator, List, Sequence, Tuple, Union

try:  # Python 3.8+
    from typing import get_args, get_origin
except ImportError:  # Python 3.7
    get_args = get_origin = None

from sphinx.util import logging

logger = logging.getLogger(__name__)


class _MockObject:
    """Used by autodoc_mock_imports."""

    __display_name__ = '_MockObject'
    __sphinx_mock__ = True

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if len(args) == 3 and isinstance(args[1], tuple):
            superclass = args[1][-1].__class__
            if superclass is cls:
                # subclassing MockObject
                return _make_subclass(args[0], superclass.__display_name__,
                                      superclass=superclass, attributes=args[2])

        return super().__new__(cls)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.__qualname__ = ''

    def __len__(self) -> int:
        return 0

    def __contains__(self, key: str) -> bool:
        return False

    def __iter__(self) -> Iterator:
        return iter([])

    def __mro_entries__(self, bases: Tuple) -> Tuple:
        return (self.__class__,)

    def __getitem__(self, key: Any) -> "_MockObject":
        return _make_subclass(key, self.__display_name__, self.__class__)()

    def __getattr__(self, key: str) -> "_MockObject":
        return _make_subclass(key, self.__display_name__, self.__class__)()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if args and type(args[0]) in [type, FunctionType, MethodType]:
            # Appears to be a decorator, pass through unchanged
            return args[0]
        return self

    def __repr__(self) -> str:
        return self.__display_name__


def _get_origin_and_args(tp: Any) -> Tuple[Any, Tuple[Any, ...]]:
    if get_origin:
        origin = get_origin(tp)
        if origin is not None:
            args = get_args(tp) if get_args else ()
            return origin, tuple(args)

    origin = getattr(tp, '__origin__', None)
    args = getattr(tp, '__args__', ())
    if args is None:
        args = ()

    return origin, tuple(args)


def _stringify(value: Any) -> str:
    if isinstance(value, tuple):
        return ', '.join(_stringify(item) for item in value)

    display_name = getattr(value, '__display_name__', None)
    if display_name:
        return display_name

    value_type = type(value).__name__
    if value_type == 'TypeVar':
        return getattr(value, '__name__', str(value).lstrip('~'))

    origin, args = _get_origin_and_args(value)
    if origin is not None:
        base_name = getattr(value, '__qualname__', None)
        if base_name is None:
            base_name = getattr(value, '_name', None)
        module = getattr(value, '__module__', None)

        if base_name is None:
            base_name = (getattr(origin, '__qualname__', None) or
                         getattr(origin, '__name__', None) or
                         str(origin))
            module = getattr(origin, '__module__', module)

        if module and module not in ('builtins',):
            base = '%s.%s' % (module, base_name)
        else:
            base = base_name

        if args:
            rendered_args = ', '.join(_stringify(arg) for arg in args)
            return '%s[%s]' % (base, rendered_args)
        else:
            return base

    if hasattr(value, '__module__') and hasattr(value, '__qualname__'):
        module = value.__module__
        qualname = value.__qualname__
        if module and module not in ('builtins',):
            return '%s.%s' % (module, qualname)
        return qualname

    text = str(value)
    if text.startswith('~'):
        return text[1:]
    return text


def _sanitize_identifier(text: str) -> str:
    sanitized = ''.join(ch if (ch.isalnum() or ch == '_') else '_' for ch in text)
    sanitized = re.sub('_+', '_', sanitized).strip('_')
    if not sanitized:
        sanitized = 'Mock'
    if sanitized[0].isdigit():
        sanitized = '_' + sanitized
    return sanitized


def _coerce_type_and_display(name: Any, module: str, superclass: Any) -> Tuple[str, str]:
    if isinstance(name, str):
        display_name = module + '.' + name if module else name
        return name, display_name

    rendered = _stringify(name)
    display_suffix = '[%s]' % rendered if rendered else '[]'

    type_base = getattr(superclass, '__name__', '_MockObject')
    identifier = _sanitize_identifier('%s_%s' % (type_base, rendered))
    display_name = (module or type_base) + display_suffix

    return identifier, display_name


def _make_subclass(name: Any, module: str, superclass: Any = _MockObject,
                   attributes: Any = None) -> Any:
    type_name, display_name = _coerce_type_and_display(name, module, superclass)
    attrs = {'__module__': module, '__display_name__': display_name}
    attrs.update(attributes or {})

    return type(type_name, (superclass,), attrs)


class _MockModule(ModuleType):
    """Used by autodoc_mock_imports."""
    __file__ = os.devnull
    __sphinx_mock__ = True

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.__all__ = []  # type: List[str]
        self.__path__ = []  # type: List[str]

    def __getattr__(self, name: str) -> _MockObject:
        return _make_subclass(name, self.__name__)()

    def __repr__(self) -> str:
        return self.__name__


class MockLoader(Loader):
    """A loader for mocking."""
    def __init__(self, finder: "MockFinder") -> None:
        super().__init__()
        self.finder = finder

    def create_module(self, spec: ModuleSpec) -> ModuleType:
        logger.debug('[autodoc] adding a mock module as %s!', spec.name)
        self.finder.mocked_modules.append(spec.name)
        return _MockModule(spec.name)

    def exec_module(self, module: ModuleType) -> None:
        pass  # nothing to do


class MockFinder(MetaPathFinder):
    """A finder for mocking."""

    def __init__(self, modnames: List[str]) -> None:
        super().__init__()
        self.modnames = modnames
        self.loader = MockLoader(self)
        self.mocked_modules = []  # type: List[str]

    def find_spec(self, fullname: str, path: Sequence[Union[bytes, str]],
                  target: ModuleType = None) -> ModuleSpec:
        for modname in self.modnames:
            # check if fullname is (or is a descendant of) one of our targets
            if modname == fullname or fullname.startswith(modname + '.'):
                return ModuleSpec(fullname, self.loader)

        return None

    def invalidate_caches(self) -> None:
        """Invalidate mocked modules on sys.modules."""
        for modname in self.mocked_modules:
            sys.modules.pop(modname, None)


@contextlib.contextmanager
def mock(modnames: List[str]) -> Generator[None, None, None]:
    """Insert mock modules during context::

        with mock(['target.module.name']):
            # mock modules are enabled here
            ...
    """
    try:
        finder = MockFinder(modnames)
        sys.meta_path.insert(0, finder)
        yield
    finally:
        sys.meta_path.remove(finder)
        finder.invalidate_caches()
