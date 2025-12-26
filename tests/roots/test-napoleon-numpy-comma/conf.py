import os
import sys


sys.path.insert(0, os.path.abspath('.'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

source_suffix = '.rst'
master_doc = 'index'

napoleon_google_docstring = False
napoleon_numpy_docstring = True
