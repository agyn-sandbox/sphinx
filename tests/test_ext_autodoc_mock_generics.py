"""
    test_ext_autodoc_mock_generics
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Integration test for mocked generics in autodoc.
"""

import pytest


@pytest.mark.sphinx('html', testroot='autodoc-mock-generics')
def test_autodoc_mock_generics_build(app):
    app.builder.build_all()
