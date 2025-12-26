import pytest


@pytest.mark.sphinx(testroot='include-source-read')
def test_include_emits_source_read(app):
    def replace_token(_app, docname, source):
        if docname == 'index':
            return

        source[0] = source[0].replace('&REPLACE_ME;', 'REPLACED')

    app.connect('source-read', replace_token)

    app.build()

    doctree = app.env.get_doctree('index')
    text = doctree.astext()
    assert 'REPLACED' in text
    assert '&REPLACE_ME;' not in text
