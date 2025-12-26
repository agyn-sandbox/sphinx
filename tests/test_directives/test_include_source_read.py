from collections import Counter

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


@pytest.mark.sphinx(testroot='include-source-read-nested')
def test_nested_include_emits_source_read_once(app):
    counts: Counter[str] = Counter()

    def append_marker(_app, docname, source):
        counts[docname] += 1
        for token, replacement in (('&A_TOKEN;', 'handled-a'),
                                   ('&B_TOKEN;', 'handled-b')):
            if token in source[0]:
                source[0] = source[0].replace(token, replacement)

    app.connect('source-read', append_marker)

    app.build()

    def count_for(suffix: str) -> int:
        return sum(value for name, value in counts.items() if name.endswith(suffix))

    assert count_for('a') == 1, counts
    assert count_for('b') == 1, counts

    doctree = app.env.get_doctree('index')
    text = doctree.astext()
    assert text.count('handled-a') == 1
    assert text.count('handled-b') == 1
