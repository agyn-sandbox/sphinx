import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath('.'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': (
        'https://docs.python.org/3',
        str(Path(__file__).resolve().parent / 'inventory' / 'python.inv'),
    ),
}
