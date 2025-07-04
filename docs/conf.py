# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

"""
Sphinx configuration file
=========================

isort:skip_file
"""

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import re
import sys


# appending ../src/auxjad to path
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.getcwd()),
        'src',
    )
)
import auxjad  # noqa: E402

# -- Project information -----------------------------------------------------

project = 'Auxjad'
copyright = '2024, Gilberto Agostinho'
author = 'Gilberto Agostinho'
email = 'gilbertohasnofb@gmail.com'

# The short X.Y version
version = re.search(r'(\d+\.\d+).*', auxjad.__version__).group(1)
# The full version, including alpha/beta/rc tags
release = auxjad.__version__


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = True

# Add mappings
intersphinx_mapping = {
    'python': ('http://docs.python.org/3', None),
    'abjad': ('https://abjad.github.io/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Custom syntax highlighting syle ------------------------------------------

from pygments.style import Style
from pygments.token import (
     Comment, Error, Generic, Literal, Name, Number, Operator, Other, 
     Punctuation, String, Text, Keyword,
)


class PandaStyle(Style):
    r"""Panda Syntax Theme.

    Custom ``pygments_style`` theme based on:
    https://github.com/tinkertrain/panda-syntax-vscode
    """
    background_color = '#292a2b'
    default_style = ''
    # Token documentation: https://pygments.org/docs/tokens/
    styles = {  
        Comment: 'italic #676b79',
        Error: '#dee2e2',
        Generic: '#676b79',
        Generic.Prompt: '#ff75b5',
        Generic.Error: 'bold #ff4f4f',
        Literal: '#dee2e2',
        Name: '#dee2e2',
        Name.Builtin: '#dee2e2',
        Name.Function: '#4cb3ec',
        Name.Decorator: '#4cb3ec',
        Name.Variable: '#dee2e2',
        Name.Tag: '#4cb3ec',
        Name.Constant: '#ffba70',
        Name.Entity: 'italic #4cb3ec',
        Name.Attribute: '#dee2e2',
        Name.Label: '#dee2e2',
        Name.Exception: '#ffba70',
        Number: '#ffba70',
        Operator: '#dee2e2',
        Operator.Word: '#ffba70',
        Other: '#dee2e2',
        Punctuation: '#dee2e2',
        String: '#19f9d8',
        Text: '#dee2e2',
        Keyword: '#ff75b5',
        Keyword.Constant: '#ffba70',
        Keyword.Declaration: '#ffba70',
        Keyword.Type: '#ffba70',
    }


def pygments_monkeypatch_style(mod_name, cls):
    r"""Monkeypatch custom theme."""
    import sys
    import pygments.styles
    cls_name = cls.__name__
    mod = type(__import__("os"))(mod_name)
    setattr(mod, cls_name, cls)
    setattr(pygments.styles, mod_name, mod)
    sys.modules["pygments.styles." + mod_name] = mod
    from pygments.styles import STYLE_MAP
    STYLE_MAP[mod_name] = mod_name + "::" + cls_name


pygments_monkeypatch_style("panda", PandaStyle)
pygments_style = "panda"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': 'https://gilbertohasnofb.github.io/auxjad-docs/',
    'logo_only': False,
    # 'display_version': True,  # deprecated
    # 'style_nav_header_background': '#4cb3ec',
}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_logo = '_static/auxjad-logo.png'

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'auxjaddoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    'figure_align': 'H',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'auxjad.tex', 'Auxjad Documentation',
     'Gilberto Agostinho', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'auxjad', 'Auxjad Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'auxjad', 'Auxjad Documentation',
     author, 'auxjad', 'Auxiliary classes and functions for Abjad.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------


# -- Adding Abjad's custom 'docs' directive ----------------------------------

import typing
from docutils.parsers.rst import Directive, directives


class HiddenDoctestDirective(Directive):
    r"""An hidden doctest directive.
    Contributes no formatting to documents built by Sphinx.
    """

    ### CLASS VARIABLES ###

    __documentation_ignore_inherited__ = True

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: typing.Dict[str, str] = {}

    ### PUBLIC METHODS ###

    def run(self):
        r"""Execute the directive."""
        self.assert_has_content()
        return []


def setup(app):
    r"""Setup directives."""
    app.add_directive('docs', HiddenDoctestDirective)
    # replacing abjad's todo custom directive with a regular warning
    app.add_directive('todo', directives.admonitions.Warning)
