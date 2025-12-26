from __future__ import annotations

from abc import ABCMeta, abstractmethod


class Basic:
    """Container for basic class level descriptor."""

    @classmethod
    @property
    def value(cls) -> int:
        """Class-level counter."""
        return 1


class Inherited(Basic):
    """Subclass used to verify inherited descriptors."""


class AbstractBase(metaclass=ABCMeta):
    @classmethod
    @property
    @abstractmethod
    def token(cls) -> str:
        """Abstract identifier."""
        return NotImplemented


class AbstractImpl(AbstractBase):
    @classmethod
    @property
    def token(cls) -> str:
        """Real identifier."""
        return "impl"


class PropertyMeta(type):
    @classmethod
    @property
    def label(mcls) -> str:
        """Metaclass provided label."""
        return "meta"


class WithMeta(metaclass=PropertyMeta):
    """Target class exposing metaclass property."""
