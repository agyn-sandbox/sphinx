from __future__ import annotations

from pathlib import Path

import pytest


@pytest.mark.parametrize(
    'prolog',
    [
        '.. prolog-comment\n',
        '.. prolog-comment\n.. second-line\n',
        '.. prolog-comment\n\n',
        '',
    ],
    ids=['comment_single', 'multi_line', 'trailing_blank', 'empty'],
)
@pytest.mark.sphinx('html', testroot='rst-prolog-heading')
def test_inline_role_heading_recognized(app, status, warning, prolog):
    app.config.rst_prolog = prolog

    app.build()

    assert 'WARNING' not in warning.getvalue()

    index_html = Path(app.outdir, 'index.html').read_text(encoding='utf-8')
    module_html = Path(app.outdir, 'module.html').read_text(encoding='utf-8')
    module_docinfo_html = Path(app.outdir, 'module_docinfo.html').read_text(encoding='utf-8')

    assert 'mypackage2' in index_html
    assert 'mypackage3' in index_html
    assert '&lt;no title&gt;' not in index_html

    assert 'mypackage2' in module_html
    assert 'mypackage3' in module_docinfo_html

    assert app.env.titles['module'].astext() == 'mypackage2'
    assert app.env.titles['module_docinfo'].astext() == 'mypackage3'
