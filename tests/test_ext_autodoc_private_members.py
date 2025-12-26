"""
    test_ext_autodoc_private_members
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the autodoc extension.  This tests mainly for private-members option.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_field(app):
    app.config.autoclass_content = 'class'
    options = {"members": None}
    actual = do_autodoc(app, 'module', 'target.private', options)
    assert list(actual) == [
        '',
        '.. py:module:: target.private',
        '',
        '',
        '.. py:function:: _public_function(name)',
        '   :module: target.private',
        '',
        '   public_function is a docstring().',
        '',
        '   :meta public:',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_field_and_private_members(app):
    app.config.autoclass_content = 'class'
    options = {"members": None,
               "private-members": None}
    actual = do_autodoc(app, 'module', 'target.private', options)
    assert list(actual) == [
        '',
        '.. py:module:: target.private',
        '',
        '',
        '.. py:function:: _public_function(name)',
        '   :module: target.private',
        '',
        '   public_function is a docstring().',
        '',
        '   :meta public:',
        '',
        '',
        '.. py:function:: private_function(name)',
        '   :module: target.private',
        '',
        '   private_function is a docstring().',
        '',
        '   :meta private:',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_list_module(app):
    options = {"members": None,
               "private-members": "_selected_function"}
    actual = do_autodoc(app, 'module', 'target.private_members_list', options)
    signatures = [line for line in actual if line.strip().startswith('.. py:function::')]
    assert len(signatures) == 2
    assert set(signatures) == {
        '.. py:function:: public_function()',
        '.. py:function:: _selected_function()',
    }
    assert '_other_private' not in '\n'.join(actual)
    assert '_undoc_private' not in '\n'.join(actual)


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_list_class_attribute(app):
    options = {"members": None,
               "private-members": "_documented_attr,_included_method"}
    actual = do_autodoc(app, 'class',
                        'target.private_members_list.PrivateListExample', options)
    signatures = [line for line in actual if '::' in line]
    assert signatures == [
        '.. py:class:: PrivateListExample()',
        '   .. py:attribute:: PrivateListExample._documented_attr',
        '   .. py:method:: PrivateListExample._included_method()',
        '   .. py:method:: PrivateListExample.public_method()',
    ]
    joined = '\n'.join(actual)
    assert '_other_method' not in joined
    assert '_undocumented_attr' not in joined
    assert '_instance_doc' not in joined


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_list_undoc(app):
    base_options = {"members": None,
                    "private-members": "_undoc_private"}
    actual = do_autodoc(app, 'module', 'target.private_members_list', base_options)
    assert '_undoc_private' not in '\n'.join(actual)

    options = dict(base_options)
    options['undoc-members'] = None
    actual = do_autodoc(app, 'module', 'target.private_members_list', options)
    assert any('.. py:function:: _undoc_private()' in line for line in actual)


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_list_missing_name_warning(app):
    options = {"members": None,
               "private-members": "_selected_function,_missing_member"}
    do_autodoc(app, 'module', 'target.private_members_list', options)
    message = app._warning.getvalue()
    assert 'missing private member _missing_member in object target.private_members_list' in message


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_list_respects_exclude(app):
    options = {"members": None,
               "private-members": "_selected_function",
               "exclude-members": "_selected_function"}
    actual = do_autodoc(app, 'module', 'target.private_members_list', options)
    assert '_selected_function' not in '\n'.join(actual)


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_list_inherited_members(app):
    options = {"members": None,
               "private-members": "_inherited_method"}
    actual = do_autodoc(app, 'class',
                        'target.private_members_list.PrivateListChild', options)
    assert '_inherited_method' not in '\n'.join(actual)

    options['inherited-members'] = None
    actual = do_autodoc(app, 'class',
                        'target.private_members_list.PrivateListChild', options)
    assert any('.. py:method:: PrivateListChild._inherited_method()' in line
               for line in actual)
