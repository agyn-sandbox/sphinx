from __future__ import annotations

import pytest

from tests.test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_autodoc_inherited_attribute_docs(app):
    options = {
        "members": None,
        "undoc-members": True,
        "inherited-members": True,
    }
    actual = do_autodoc(app, 'class', 'target.inherited_attrs.Child', options)
    output = "\n".join(actual)

    assert '.. py:attribute:: Child.base_attr' in output
    assert 'Docstring for the base class attribute.' in output
    assert '.. py:attribute:: Child.override_attr' in output
    assert 'Subclass-specific documentation that overrides the base docstring.' in output
    assert 'Docstring defined on the base class but overridden in the subclass.' not in output
    assert '.. py:attribute:: Child.annotated_only' in output
    assert 'Docstring for an annotation-only ClassVar.' in output
    assert 'instance_attr' not in output


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_autodoc_inherited_attribute_docs_control(app):
    options = {
        "members": None,
        "undoc-members": True,
    }
    actual = do_autodoc(app, 'class', 'target.inherited_attrs.Child', options)
    output = "\n".join(actual)

    assert '.. py:attribute:: Child.base_attr' not in output
    assert 'Docstring for the base class attribute.' not in output
