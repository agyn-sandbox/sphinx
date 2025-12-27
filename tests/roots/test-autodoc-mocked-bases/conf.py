import os
import sys

sys.path.insert(0, os.path.abspath('.'))

extensions = ['sphinx.ext.autodoc']

source_suffix = '.rst'

autodoc_mock_imports = ['torch']

nitpicky = True
