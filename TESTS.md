Testing Sphinx locally

This document explains how to set up and run the Sphinx test suites (Python and JavaScript) locally, and how to troubleshoot common issues.

Prerequisites
- Python 3.11+ with pip
- Node.js and npm (for JS tests)
- Recommended Python test tools: pytest, pytest-cov

Setup
1) Python environment
   - Create/activate a virtual environment (recommended)
   - Install Sphinx in editable mode:
     - pip install -e .
   - Install test dependencies (aligns with the repository’s test group):
     - pip install "pytest>=8.0" "pytest-xdist[psutil]>=3.4" \
       "cython>=3.0" "defusedxml>=0.7.1" "setuptools>=70.0" \
       "typing_extensions>=4.9"

2) JavaScript environment
   - Install JS dev dependencies:
     - npm ci
   - Firefox + geckodriver (required for JS tests)
     - The JS test runner uses headless Firefox via geckodriver. Install both
       and ensure they are on your PATH.
     - macOS (Homebrew):
       - brew install --cask firefox
       - brew install geckodriver
     - Debian/Ubuntu:
       - sudo apt-get update
       - sudo apt-get install firefox geckodriver
         - If firefox is not available via apt, use firefox-esr:
           - sudo apt-get install firefox-esr geckodriver
     - Fedora/RHEL:
       - sudo dnf install firefox geckodriver
     - Windows:
       - Install Firefox from mozilla.org (MSI/installer).
       - Install geckodriver from GitHub releases:
         - https://github.com/mozilla/geckodriver/releases
         - Place geckodriver.exe in a directory on PATH (e.g., C:\\Tools) and
           add that directory to the PATH environment variable.
     - Verify installation:
       - firefox --version
       - geckodriver --version

Run tests
- Python tests:
  - python -m pytest -vv
  - Tip: to leverage multiple CPUs: python -m pytest -vv -n auto

- JavaScript tests:
  - npm test

Troubleshooting
- Python
  - ModuleNotFoundError: defusedxml: ensure you installed the Python test dependencies listed above.
  - Slow runs: use parallelization via pytest-xdist: -n auto (Linux/macOS). On Windows, avoid -n auto unless configured appropriately.
  - Python 3.12 vs 3.11 (Enum/autodoc): CPython 3.12 introduced changes in enum.Enum internals and representation that result in different autodoc output compared to Python 3.11. As a consequence, running the Python test suite on 3.12 may produce a small number of expected failures in Enum-related autodoc tests (around 11 failures). If you need a fully green local run:
    - Prefer Python 3.11 for local testing.
    - Or skip Enum/autodoc-focused tests using pytest's -k filtering. Examples:
      - python -m pytest -vv -k 'not enum'
      - python -m pytest -vv -k 'not test_ext_autodoc and not util_inspect'
    These examples are approximate and intended to exclude Enum-heavy autodoc tests; adjust the -k expressions to match your local needs.

- JavaScript
  - The JS tests run via jasmine-browser-runner in a headless Firefox browser.
  - Runner cannot find Firefox/geckodriver:
    - Ensure both firefox and geckodriver are installed and on PATH.
    - Check versions: firefox --version, geckodriver --version.
    - On Linux, prefer distro packages (apt/dnf) over Snap for Firefox if
      geckodriver cannot locate the binary. Using firefox-esr is fine.
    - On Windows, after adding geckodriver.exe to PATH, restart your shell.
  - WebDriver or connection errors:
    - Kill stray geckodriver processes and retry:
      - Linux/macOS: pkill -f geckodriver
      - Windows (PowerShell): Stop-Process -Name geckodriver -Force
    - Ensure headless mode works: MOZ_HEADLESS=1 firefox -headless -v
  - Port binding issues (runner HTTP server):
    - The runner binds to 127.0.0.1. Close programs using the same port, or
      adjust tests/js/jasmine-browser.mjs if you need different settings.
  - Configure a different browser (optional):
    - Edit tests/js/jasmine-browser.mjs and change browser.name, e.g., to
      "chromeHeadless" if you have Chrome and the appropriate driver installed.
  - Re-install JS deps if needed: npm ci
  - Still failing?
    - Clear npm cache and reinstall: npm cache verify && npm ci
    - Use a clean virtualenv for Python and re-install.

Notes
- Requires Python >= 3.11 (see pyproject.toml).
- Some tests may depend on external tools (e.g., LaTeX toolchain) that are not strictly required for most development workflows.
