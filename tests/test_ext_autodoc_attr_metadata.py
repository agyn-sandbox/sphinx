"""
    test_ext_autodoc_attr_metadata
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for autodoc behavior around metadata in attribute doc comments.
"""

import pytest

from .test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_meta_public_doc_comment(app):
    options = {"members": None}
    actual = do_autodoc(app, 'module', 'target.meta_doc_comments', options)
    assert '.. py:data:: _foo' in list(actual)
