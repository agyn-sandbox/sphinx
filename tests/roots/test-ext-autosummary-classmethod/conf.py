import os
import sys


sys.path.insert(0, os.path.abspath('.'))


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]

autosummary_generate = True
autosummary_generate_overwrite = True

master_doc = 'index'
source_suffix = '.rst'
