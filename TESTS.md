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

- JavaScript
  - The JS tests run via jasmine-browser-runner in a headless Firefox browser.
  - If the runner cannot find a browser, install Firefox and geckodriver, or configure jasmine-browser-runner to use an available headless browser.
  - Re-install JS deps if needed: npm ci

Notes
- Requires Python >= 3.11 (see pyproject.toml).
- Some tests may depend on external tools (e.g., LaTeX toolchain) that are not strictly required for most development workflows.
