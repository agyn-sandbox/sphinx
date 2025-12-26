import pytest


@pytest.mark.sphinx('html', testroot='napoleon-numpy-comma',
                    confoverrides={'autodoc_default_options': {'members': True}})
def test_numpy_parameters_preserve_combined_names(app):
    app.build()
    content = (app.outdir / 'index.html').read_text()

    assert '<strong>x1</strong><strong>, </strong><strong>x2</strong> (' in content
    assert 'comma_parameters_no_space' in content
    assert '<strong>x1</strong><strong>,</strong><strong>x2</strong> (' in content
    assert 'array_like</span></code>, <em>optional</em>' in content
