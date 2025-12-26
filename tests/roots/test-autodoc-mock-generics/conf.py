import os
import sys

sys.path.insert(0, os.path.abspath('.'))

extensions = ['sphinx.ext.autodoc']

autodoc_mock_imports = ['mylib']

master_doc = 'index'
