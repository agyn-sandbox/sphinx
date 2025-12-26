from __future__ import annotations

from typing import TypeAlias


class AliasTarget:
    """Marker class used for type-alias testing."""


AliasName: TypeAlias = AliasTarget


def use_alias(value: AliasName) -> AliasName:
    """Return the provided value unchanged."""

    return value
