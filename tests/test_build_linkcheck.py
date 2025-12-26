"""
    test_build_linkcheck
    ~~~~~~~~~~~~~~~~~~~~

    Test the build process with manpage builder with the test root.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import json
import re
from unittest import mock
import pytest


@pytest.mark.sphinx('linkcheck', testroot='linkcheck', freshenv=True)
def test_defaults(app, status, warning):
    app.builder.build_all()

    assert (app.outdir / 'output.txt').exists()
    content = (app.outdir / 'output.txt').read_text()

    print(content)
    # looking for '#top' and '#does-not-exist' not found should fail
    assert "Anchor 'top' not found" in content
    assert "Anchor 'does-not-exist' not found" in content
    # looking for non-existent URL should fail
    assert " Max retries exceeded with url: /doesnotexist" in content
    # images should fail
    assert "Not Found for url: https://www.google.com/image.png" in content
    assert "Not Found for url: https://www.google.com/image2.png" in content
    assert len(content.splitlines()) == 5


@pytest.mark.sphinx('linkcheck', testroot='linkcheck', freshenv=True)
def test_defaults_json(app, status, warning):
    app.builder.build_all()

    assert (app.outdir / 'output.json').exists()
    content = (app.outdir / 'output.json').read_text()
    print(content)

    rows = [json.loads(x) for x in content.splitlines()]
    row = rows[0]
    for attr in ["filename", "lineno", "status", "code", "uri",
                 "info"]:
        assert attr in row

    assert len(content.splitlines()) == 8
    assert len(rows) == 8
    # the output order of the rows is not stable
    # due to possible variance in network latency
    rowsby = {row["uri"]:row for row in rows}
    assert rowsby["https://www.google.com#!bar"] == {
        'filename': 'links.txt',
        'lineno': 10,
        'status': 'working',
        'code': 0,
        'uri': 'https://www.google.com#!bar',
        'info': ''
    }
    # looking for non-existent URL should fail
    dnerow = rowsby['https://localhost:7777/doesnotexist']
    assert dnerow['filename'] == 'links.txt'
    assert dnerow['lineno'] == 13
    assert dnerow['status'] == 'broken'
    assert dnerow['code'] == 0
    assert dnerow['uri'] == 'https://localhost:7777/doesnotexist'
    assert rowsby['https://www.google.com/image2.png'] == {
        'filename': 'links.txt',
        'lineno': 16,
        'status': 'broken',
        'code': 0,
        'uri': 'https://www.google.com/image2.png',
        'info': '404 Client Error: Not Found for url: https://www.google.com/image2.png'
    }
    # looking for '#top' and '#does-not-exist' not found should fail
    assert "Anchor 'top' not found" == \
        rowsby["https://www.google.com/#top"]["info"]
    assert "Anchor 'does-not-exist' not found" == \
        rowsby["http://www.sphinx-doc.org/en/1.7/intro.html#does-not-exist"]["info"]
    # images should fail
    assert "Not Found for url: https://www.google.com/image.png" in \
        rowsby["https://www.google.com/image.png"]["info"]


@pytest.mark.sphinx(
    'linkcheck', testroot='linkcheck', freshenv=True,
    confoverrides={'linkcheck_anchors_ignore': ["^!", "^top$"],
                   'linkcheck_ignore': [
                       'https://localhost:7777/doesnotexist',
                       'http://www.sphinx-doc.org/en/1.7/intro.html#',
                       'https://www.google.com/image.png',
                       'https://www.google.com/image2.png']
                   })
def test_anchors_ignored(app, status, warning):
    app.builder.build_all()

    assert (app.outdir / 'output.txt').exists()
    content = (app.outdir / 'output.txt').read_text()

    # expect all ok when excluding #top
    assert not content


@pytest.mark.sphinx(
    'linkcheck', testroot='linkcheck', freshenv=True,
    confoverrides={'linkcheck_auth': [
                        (r'.+google\.com/image.+', 'authinfo1'),
                        (r'.+google\.com.+', 'authinfo2'),
                   ]
                  })
def test_auth(app, status, warning):
    mock_req = mock.MagicMock()
    mock_req.return_value = 'fake-response'

    with mock.patch.multiple('requests', get=mock_req, head=mock_req):
        app.builder.build_all()
        for c_args, c_kwargs in mock_req.call_args_list:
            if 'google.com/image' in c_args[0]:
                assert c_kwargs['auth'] == 'authinfo1'
            elif 'google.com' in c_args[0]:
                assert c_kwargs['auth'] == 'authinfo2'
            else:
                assert not c_kwargs['auth']


@pytest.mark.sphinx(
    'linkcheck', testroot='linkcheck', freshenv=True,
    confoverrides={'linkcheck_request_headers': {
        "https://localhost:7777/": {
            "Accept": "text/html",
        },
        "http://www.sphinx-doc.org": {  # no slash at the end
            "Accept": "application/json",
        },
        "*": {
            "X-Secret": "open sesami",
        }
    }})
def test_linkcheck_request_headers(app, status, warning):
    mock_req = mock.MagicMock()
    mock_req.return_value = 'fake-response'

    with mock.patch.multiple('requests', get=mock_req, head=mock_req):
        app.builder.build_all()
        for args, kwargs in mock_req.call_args_list:
            url = args[0]
            headers = kwargs.get('headers', {})
            if "https://localhost:7777" in url:
                assert headers["Accept"] == "text/html"
            elif 'http://www.sphinx-doc.org' in url:
                assert headers["Accept"] == "application/json"
            elif 'https://www.google.com' in url:
                assert headers["Accept"] == "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"
                assert headers["X-Secret"] == "open sesami"
            else:
                assert headers["Accept"] == "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"


@pytest.mark.sphinx(
    'linkcheck', testroot='linkcheck-local', freshenv=True,
    confoverrides={'linkcheck_check_local': True,
                   'linkcheck_ignore': [r'ignored\.html']})
def test_local_links_html(app, status, warning):
    app.builder.build_all()

    output = (app.outdir / 'output.json').read_text()
    rows = [json.loads(line) for line in output.splitlines() if line]
    rows_by_key = {(row['filename'], row['uri']): row for row in rows}

    def get(filename: str, uri: str) -> dict:
        try:
            return rows_by_key[(filename, uri)]
        except KeyError as exc:
            raise AssertionError(f"Missing row for {filename} -> {uri}") from exc

    index_file = 'index.rst'

    assert get(index_file, 'working.html')['status'] == 'working'
    assert get(index_file, 'working.html')['info'] == ''
    assert get(index_file, 'working/')['status'] == 'broken'
    assert get(index_file, 'missing.html')['status'] == 'broken'
    assert get(index_file, 'missing.html')['info'] == 'Local target not found'
    assert get(index_file, 'page.html')['status'] == 'working'
    assert get(index_file, 'page.html')['info'] == ''
    assert get(index_file, 'page.html#target-anchor')['status'] == 'working'
    assert get(index_file, 'page.html#missing-anchor')['status'] == 'broken'
    assert get(index_file, 'page.html#missing-anchor')['info'] == "Anchor 'missing-anchor' not found"
    assert get(index_file, 'page/#target-anchor')['status'] == 'broken'
    assert get(index_file, 'page/#target-anchor')['info'] == 'Local target not found'
    assert get(index_file, 'page/#missing-anchor')['status'] == 'broken'
    assert get(index_file, 'page/#missing-anchor')['info'] == 'Local target not found'
    assert get(index_file, 'ignored.html')['status'] == 'ignored'
    assert get('another.rst', '#home-anchor')['status'] == 'broken'
    assert get('another.rst', '#home-anchor')['info'] == "Anchor 'home-anchor' not found"
    assert get(index_file, '#home-anchor')['status'] == 'working'
    assert get(index_file, '#home-anchor')['info'] == ''
    assert get(index_file, '#missing-same-anchor')['status'] == 'broken'
    assert get(index_file, '#missing-same-anchor')['info'] == "Anchor 'missing-same-anchor' not found"
    assert get(index_file, 'dir/section.html')['status'] == 'working'
    assert get(index_file, 'dir/section.html#dir-anchor')['status'] == 'working'
    assert get(index_file, 'dir/section/')['status'] == 'broken'
    assert get(index_file, 'dir/section/')['info'] == 'Local target not found'
    assert get(index_file, 'dir/section/#dir-anchor')['status'] == 'broken'
    assert get(index_file, 'dir/section/#dir-anchor')['info'] == 'Local target not found'
    assert get(index_file, 'dir/section/#missing-dir-anchor')['status'] == 'broken'
    assert get(index_file, 'dir/section/#missing-dir-anchor')['info'] == 'Local target not found'
    assert get(index_file, 'dir/missing/')['status'] == 'broken'
    assert get(index_file, 'dir/missing/')['info'] == 'Local target not found'
    assert get(index_file, '/index.html')['status'] == 'ignored'
    assert get(index_file, '/index.html')['info'] == "Absolute local path requires 'linkcheck_local_root'"
    assert get(index_file, '/missing.html')['status'] == 'ignored'
    assert get(index_file, '/missing.html')['info'] == "Absolute local path requires 'linkcheck_local_root'"
    broken_page = get('dir/another.rst', 'page.html')
    assert broken_page['status'] == 'broken'
    assert broken_page['info'] == 'Local target not found'

    page_rows = [row for row in rows if row['uri'] == 'page.html']
    assert len(page_rows) == 2
    assert any(row['filename'] == 'index.rst' and row['status'] == 'working'
               for row in page_rows)
    assert any(row['filename'] == 'dir/another.rst' and row['status'] == 'broken'
               for row in page_rows)

    anchor_rows = [row for row in rows if row['uri'] == '#home-anchor']
    assert len(anchor_rows) == 2
    assert any(row['filename'] == 'index.rst' and row['status'] == 'working'
               for row in anchor_rows)
    assert any(row['filename'] == 'another.rst' and row['status'] == 'broken'
               for row in anchor_rows)

    broken_lines = (app.outdir / 'output.txt').read_text()
    assert 'missing.html' in broken_lines
    assert 'page.html#missing-anchor' in broken_lines


@pytest.mark.sphinx(
    'linkcheck', testroot='linkcheck-local', freshenv=True,
    confoverrides={'linkcheck_check_local': True,
                   'linkcheck_local_builder': 'dirhtml',
                   'linkcheck_ignore': [r'ignored\.html']})
def test_local_links_dirhtml(app, status, warning):
    app.builder.build_all()

    output = (app.outdir / 'output.json').read_text()
    rows = [json.loads(line) for line in output.splitlines() if line]
    rows_by_key = {(row['filename'], row['uri']): row for row in rows}

    def get(filename: str, uri: str) -> dict:
        try:
            return rows_by_key[(filename, uri)]
        except KeyError as exc:
            raise AssertionError(f"Missing row for {filename} -> {uri}") from exc

    index_file = 'index.rst'

    assert get(index_file, 'working.html')['status'] == 'broken'
    assert get(index_file, 'working.html')['info'] == 'Local target not found'
    assert get(index_file, 'working/')['status'] == 'working'
    assert get(index_file, 'page.html')['status'] == 'broken'
    assert get(index_file, 'page.html')['info'] == 'Local target not found'
    assert get(index_file, 'page.html#target-anchor')['status'] == 'broken'
    assert get(index_file, 'page.html#target-anchor')['info'] == 'Local target not found'
    assert get(index_file, 'page.html#missing-anchor')['status'] == 'broken'
    assert get(index_file, 'page.html#missing-anchor')['info'] == 'Local target not found'
    assert get(index_file, 'page/#target-anchor')['status'] == 'working'
    assert get(index_file, 'page/#missing-anchor')['status'] == 'broken'
    assert get(index_file, 'page/#missing-anchor')['info'] == "Anchor 'missing-anchor' not found"
    assert get(index_file, 'ignored.html')['status'] == 'ignored'
    assert get(index_file, 'dir/section.html')['status'] == 'broken'
    assert get(index_file, 'dir/section.html')['info'] == 'Local target not found'
    assert get(index_file, 'dir/section.html#dir-anchor')['status'] == 'broken'
    assert get(index_file, 'dir/section.html#dir-anchor')['info'] == 'Local target not found'
    assert get(index_file, 'dir/section/')['status'] == 'working'
    assert get(index_file, 'dir/section/#dir-anchor')['status'] == 'working'
    assert get(index_file, 'dir/section/#missing-dir-anchor')['status'] == 'broken'
    assert get(index_file, 'dir/section/#missing-dir-anchor')['info'] == "Anchor 'missing-dir-anchor' not found"
    assert get(index_file, 'dir/missing/')['status'] == 'broken'
    assert get(index_file, 'dir/missing/')['info'] == 'Local target not found'
    assert get(index_file, '/index.html')['status'] == 'ignored'
    assert get(index_file, '/missing.html')['status'] == 'ignored'
    assert get(index_file, '#home-anchor')['status'] == 'working'
    assert get('another.rst', '#home-anchor')['status'] == 'broken'
    broken_page = get('dir/another.rst', 'page.html')
    assert broken_page['status'] == 'broken'
    assert broken_page['info'] == 'Local target not found'

    page_rows = [row for row in rows if row['uri'] == 'page.html']
    assert len(page_rows) == 2
    assert all(row['status'] == 'broken' for row in page_rows)
    assert any(row['filename'] == 'index.rst' for row in page_rows)
    assert any(row['filename'] == 'dir/another.rst' for row in page_rows)

    anchor_rows = [row for row in rows if row['uri'] == '#home-anchor']
    assert len(anchor_rows) == 2
    assert any(row['filename'] == 'index.rst' and row['status'] == 'working'
               for row in anchor_rows)
    assert any(row['filename'] == 'another.rst' and row['status'] == 'broken'
               for row in anchor_rows)


@pytest.mark.sphinx(
    'linkcheck', testroot='linkcheck-local', freshenv=True,
    confoverrides={'linkcheck_check_local': True,
                   'linkcheck_local_root': '',
                   'linkcheck_ignore': [r'ignored\.html']})
def test_local_links_with_root(app, status, warning):
    app.builder.build_all()

    rows = [json.loads(line) for line in (app.outdir / 'output.json').read_text().splitlines() if line]
    rowsby = {row['uri']: row for row in rows}

    assert rowsby['/index.html']['status'] == 'working'
    assert rowsby['/index.html']['info'] == ''
    assert rowsby['/missing.html']['status'] == 'broken'
    assert rowsby['/missing.html']['info'] == 'Local target not found'


@pytest.mark.sphinx(
    'linkcheck', testroot='linkcheck-local', freshenv=True,
    confoverrides={'linkcheck_check_local': True,
                   'linkcheck_ignore': [r'ignored\.html'],
                   'linkcheck_anchors_ignore': [r'missing-anchor$']})
def test_local_links_anchor_ignore(app, status, warning):
    app.builder.build_all()

    rows = [json.loads(line) for line in (app.outdir / 'output.json').read_text().splitlines() if line]
    rowsby = {row['uri']: row for row in rows}

    assert rowsby['page.html#missing-anchor']['status'] == 'working'
    assert rowsby['page.html#missing-anchor']['info'] in ('', 'old')
    assert rowsby['page/#missing-anchor']['status'] == 'broken'
    assert rowsby['page/#missing-anchor']['info'] == 'Local target not found'
