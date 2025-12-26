"""Fixtures for testing :private-members: argument handling."""


def public_function():
    """Public function that is always documented."""


def _selected_function():
    """Private function that should be included when requested."""


def _other_private():
    """Private function that should stay hidden unless all are included."""


def _undoc_private():
    # intentionally undocumented to exercise :undoc-members:
    pass


class PrivateListBase:
    """Base class providing an inherited private member."""

    def _inherited_method(self):
        """Private method defined on the base class."""


class PrivateListExample(PrivateListBase):
    """Class used by private-members selection tests."""

    #: Documented private attribute.
    _documented_attr = 1
    _undocumented_attr = 2

    def __init__(self) -> None:
        #: Documented private instance attribute.
        self._instance_doc = 3
        self._instance_nodoc = 4

    def _included_method(self):
        """Private method that should be included when requested."""

    def _other_method(self):
        """Private method that should remain hidden."""

    def public_method(self):
        """Public method that is documented regardless of options."""


class PrivateListChild(PrivateListBase):
    """Child class for inherited private member tests."""

    def _child_private(self):
        """Private method defined on the child class."""
