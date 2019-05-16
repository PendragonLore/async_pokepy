# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "async_pokepy"
copyright = "2019, Lorenzo"  # pylint: disable=redefined-builtin
author = "Lorenzo"

# The full version, including alpha/beta/rc tags
with open("../async_pokepy/__init__.py") as f:
    version = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE).group(1)

# The full version, including alpha/beta/rc tags.
release = version

pygments_style = "friendly"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.napoleon",
    "sphinxcontrib.asyncio",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

gettext_compact = False

# -- Options for HTML output -------------------------------------------------

html_experimental_html5_writer = True

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme_path = [sphinx_readable_theme.get_html_theme_path()]
html_theme = "basic"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiohttp": ("https://aiohttp.readthedocs.io/en/stable/", None)
}


def setup(app):
    app.add_javascript("custom.js")
    app.add_stylesheet("style.css")
