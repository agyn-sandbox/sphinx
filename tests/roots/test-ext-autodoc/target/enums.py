import enum


class EnumCls(enum.Enum):
    """
    this is enum class
    """

    #: doc for val1
    val1 = 12
    val2 = 23  #: doc for val2
    val3 = 34
    """doc for val3"""
    val4 = 34

    def say_hello(self):
        """a method says hello to you."""
        pass

    @classmethod
    def say_goodbye(cls):
        """a classmethod says good-bye to you."""
        pass


class IntEnumCls(enum.IntEnum):
    """An IntEnum for autodoc enum default tests."""

    level1 = 1
    level2 = 2


def enum_function(color: EnumCls = EnumCls.val1):
    """Function with an Enum default value."""
    return color


def int_enum_function(level: IntEnumCls = IntEnumCls.level1):
    """Function with an IntEnum default value."""
    return level


def mixed_defaults(color: EnumCls = EnumCls.val2, label: str = 'enum'):
    """Function combining Enum and non-Enum defaults."""
    return color, label
