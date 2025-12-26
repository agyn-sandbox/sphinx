"""
    test_ext_autodoc_autoproperty
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the autodoc extension.  This tests mainly the Documenters; the auto
    directives are tested in a test source file translated by test_build.

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import sys

import pytest

from sphinx import addnodes
from sphinx.testing import restructuredtext
from sphinx.testing.util import assert_node

from .test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.Foo.prop1')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.prop1',
        '   :module: target.properties',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_class_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.Foo.prop2')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.prop2',
        '   :module: target.properties',
        '   :classmethod:',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]


@pytest.mark.skipif(sys.version_info < (3, 8), reason='python 3.8+ is required.')
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_cached_properties(app):
    actual = do_autodoc(app, 'property', 'target.cached_property.Foo.prop')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.prop',
        '   :module: target.cached_property',
        '   :type: target.cached_property.Point',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_property_type_annotation_links(app):
    actual = do_autodoc(app, 'property', 'target.properties.Segment.end')
    doctree = restructuredtext.parse(app, '\n'.join(actual))
    signature = doctree[1][0]
    annotation = signature[3]
    assert_node(annotation, addnodes.desc_annotation)
    assert annotation.astext().startswith(': ')
    assert_node(annotation[1], addnodes.pending_xref,
                refdomain='py', reftype='class', reftarget='target.properties.Point')
    assert annotation[1].astext() == 'target.properties.Point'


@pytest.mark.skipif(sys.version_info < (3, 8), reason='python 3.8+ is required.')
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_cached_property_type_annotation_links(app):
    actual = do_autodoc(app, 'property', 'target.cached_property.Foo.prop')
    doctree = restructuredtext.parse(app, '\n'.join(actual))
    signature = doctree[1][0]
    annotation = signature[3]
    assert_node(annotation, addnodes.desc_annotation)
    assert annotation.astext().startswith(': ')
    assert_node(annotation[1], addnodes.pending_xref,
                refdomain='py', reftype='class', reftarget='target.cached_property.Point')
    assert annotation[1].astext() == 'target.cached_property.Point'
