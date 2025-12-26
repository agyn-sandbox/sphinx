from __future__ import annotations

from typing import ClassVar


class Base:
    #: Docstring for the base class attribute.
    base_attr = 1

    #: Docstring defined on the base class but overridden in the subclass.
    override_attr = 2

    #: Docstring for an annotation-only ClassVar.
    annotated_only: ClassVar[int]


class Child(Base):
    #: Subclass-specific documentation that overrides the base docstring.
    override_attr = 3

    #: Subclass attribute documented in the subclass.
    child_only = 4

    def __init__(self) -> None:
        self.instance_attr = "runtime"
