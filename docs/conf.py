"""Sphinx configuration."""
import datetime
import os
import sys

# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'glimpse'
author = 'Ethan Welty, Douglas Brinkerhoff'
copyright = f'{datetime.datetime.now().year}, {author}'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
    'matplotlib': ('https://matplotlib.org', None),
    'piexif': ('https://piexif.readthedocs.io/en/latest', None),
    'PIL': ('https://pillow.readthedocs.io/en/stable', None)
}

autosummary_generate = True
autodoc_typehints = 'description'

templates_path = ['templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# https://sphinx-rtd-theme.readthedocs.io/en/latest/configuring.html
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'style_external_links': False
}

