from importlib import import_module
from types import SimpleNamespace

import pytest

from sphinx.errors import VersionRequirementError
from sphinx.extension import Extension, verify_needs_extensions


EXTENSION_NAME = 'dummy.ext'
EXTENSION_ROOT = 'tests.roots.test_needs_extensions'


def make_extension(module_basename: str) -> Extension:
    module = import_module(f'{EXTENSION_ROOT}.{module_basename}')
    kwargs = {}
    if hasattr(module, '__version__'):
        kwargs['version'] = module.__version__
    return Extension(EXTENSION_NAME, module, **kwargs)


def make_app_with_extension(module_basename: str) -> SimpleNamespace:
    extension = make_extension(module_basename)
    return SimpleNamespace(extensions={EXTENSION_NAME: extension})


def make_config(requirement: str) -> SimpleNamespace:
    return SimpleNamespace(needs_extensions={EXTENSION_NAME: requirement})


def test_needs_extensions_accepts_newer_version() -> None:
    app = make_app_with_extension('ext_newer')
    config = make_config('0.6.0')

    verify_needs_extensions(app, config)


def test_needs_extensions_rejects_prerelease_when_final_required() -> None:
    app = make_app_with_extension('ext_prerelease')
    config = make_config('0.6.0')

    with pytest.raises(VersionRequirementError) as exc:
        verify_needs_extensions(app, config)

    assert 'needs the extension dummy.ext at least in version 0.6.0' in str(exc.value)


def test_needs_extensions_rejects_unknown_version() -> None:
    app = make_app_with_extension('ext_unknown')
    config = make_config('0.6.0')

    with pytest.raises(VersionRequirementError) as exc:
        verify_needs_extensions(app, config)

    assert 'needs the extension dummy.ext at least in version 0.6.0' in str(exc.value)


def test_needs_extensions_accepts_exact_match() -> None:
    app = make_app_with_extension('ext_exact')
    config = make_config('0.6.0')

    verify_needs_extensions(app, config)


def test_needs_extensions_handles_dev_and_post_releases() -> None:
    config = make_config('0.6.0')

    app_with_dev = make_app_with_extension('ext_dev')
    with pytest.raises(VersionRequirementError):
        verify_needs_extensions(app_with_dev, config)

    app_with_post = make_app_with_extension('ext_post')
    verify_needs_extensions(app_with_post, config)
