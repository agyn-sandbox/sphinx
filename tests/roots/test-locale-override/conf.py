# -- Test configuration for locale override precedence --------------------

extensions = []
master_doc = 'index'
language = 'da'
locale_dirs = [
    'locales/project_primary',
    'locales/project_secondary',
]
gettext_compact = False
