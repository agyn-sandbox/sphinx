"""Tests for locale precedence when project catalogs override Sphinx domain."""

import gettext
from os import path

import pytest

from sphinx import locale as sphinx_locale
from sphinx import package_dir


@pytest.fixture(autouse=True)
def clear_locale_translators():
    sphinx_locale.translators.clear()
    try:
        yield
    finally:
        sphinx_locale.translators.clear()


def _bundled_translation(message: str) -> str:
    mo_path = path.join(package_dir, 'locale', 'da', 'LC_MESSAGES', 'sphinx.mo')
    with open(mo_path, 'rb') as stream:
        bundled = gettext.GNUTranslations(stream)
    return bundled.gettext(message)


@pytest.mark.sphinx('html', testroot='locale-override')
def test_project_catalog_overrides_sphinx_domain(app):
    translator = app.translator

    assert translator.gettext('Fig. %s') == 'LOKAL FIGUR %s'
    assert translator.gettext('Listing %s') == 'LOKAL LISTE %s'

    # When the local catalog does not define a message, fall back to bundled strings.
    assert translator.gettext('Table %s') == _bundled_translation('Table %s')


@pytest.mark.sphinx(
    'html',
    testroot='locale-override',
    confoverrides={'locale_dirs': ['locales/project_secondary', 'locales/project_primary']},
)
def test_multiple_locale_dirs_respect_declaration_order(app):
    translator = app.translator

    assert translator.gettext('Fig. %s') == 'SEKUNDÆR FIGUR %s'
    assert translator.gettext('Listing %s') == 'SEKUNDÆR LISTE %s'
