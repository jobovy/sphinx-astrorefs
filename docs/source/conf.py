# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import datetime


# -- Project information -----------------------------------------------------

project = 'sphinx-astrorefs'
if datetime.datetime.now().year > 2020:
    copyright = u'2020 - {}, Jo Bovy'.format(datetime.datetime.now().year)
else:
    copyright = u'2020, Jo Bovy'.format(datetime.datetime.now().year)
author = 'Jo Bovy'

# The full version, including alpha/beta/rc tags
release = '0.11'


# -- General configuration ---------------------------------------------------

master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx_rtd_theme',
              'nbsphinx',
              'sphinxcontrib.bibtex',
              'sphinx_astrorefs'
]

# sphinxcontrib.bib
bibtex_bibfiles= ['references.bib']
bibtex_encoding= 'latin'

# sphinx_astrorefs
astrorefs_resolve_aas_macros= True
astrorefs_resolve_aas_macros_infile= 'refs.bib'
astrorefs_resolve_aas_macros_outfile= 'references.bib'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['.ipynb_checkpoints/*']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

# no prompts in nbsphinx
nbsphinx_prolog = """
.. raw:: html

    <style>
        .nbinput .prompt,
        .nboutput .prompt {
            display: none;
        }
    </style>
"""
