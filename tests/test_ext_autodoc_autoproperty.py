"""
    test_ext_autodoc_autoproperty
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the autodoc extension.  This tests mainly the Documenters; the auto
    directives are tested in a test source file translated by test_build.

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from .test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.Foo.prop')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.prop',
        '   :module: target.properties',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property(app):
    actual = do_autodoc(app, 'property', 'target.classmethod_properties.Basic.value')
    assert list(actual) == [
        '',
        '.. py:property:: Basic.value',
        '   :module: target.classmethod_properties',
        '   :type: int',
        '',
        '   Class-level counter.',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property_inherited(app):
    actual = do_autodoc(app, 'property', 'target.classmethod_properties.Inherited.value')
    assert list(actual) == [
        '',
        '.. py:property:: Inherited.value',
        '   :module: target.classmethod_properties',
        '   :type: int',
        '',
        '   Class-level counter.',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property_abstract(app):
    actual = do_autodoc(app, 'property', 'target.classmethod_properties.AbstractBase.token')
    assert list(actual) == [
        '',
        '.. py:property:: AbstractBase.token',
        '   :module: target.classmethod_properties',
        '   :abstractmethod:',
        '   :type: str',
        '',
        '   Abstract identifier.',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property_concrete(app):
    actual = do_autodoc(app, 'property', 'target.classmethod_properties.AbstractImpl.token')
    assert list(actual) == [
        '',
        '.. py:property:: AbstractImpl.token',
        '   :module: target.classmethod_properties',
        '   :type: str',
        '',
        '   Real identifier.',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property_metaclass(app):
    actual = do_autodoc(app, 'property', 'target.classmethod_properties.WithMeta.label')
    assert list(actual) == [
        '',
        '.. py:property:: WithMeta.label',
        '   :module: target.classmethod_properties',
        '   :type: str',
        '',
        '   Metaclass provided label.',
        '',
    ]
