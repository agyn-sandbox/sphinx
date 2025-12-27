from typing import List, TypeAlias, Union


SimpleInt = int
"""Docstring for SimpleInt."""


MyInt: TypeAlias = int
"""Docstring for MyInt."""


IntListOrUnion: TypeAlias = Union[List[int], int]
"""Docstring for IntListOrUnion."""


class _Aliased:
    pass


AliasWithoutDoc = _Aliased
