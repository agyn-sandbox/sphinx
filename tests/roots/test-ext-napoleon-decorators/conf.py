import os
import sys


project = 'napoleon-decorators'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
source_suffix = '.rst'
master_doc = 'index'
napoleon_include_init_with_doc = True
autodoc_default_options = {'members': True}

sys.path.insert(0, os.path.abspath('.'))
