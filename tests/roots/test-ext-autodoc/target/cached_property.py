from functools import cached_property


class Point:
    pass


class Foo:
    @cached_property
    def prop(self) -> Point:
        return Point()
