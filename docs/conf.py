"""Sphinx configuration."""
from datetime import datetime

project = "Pybox"
author = "yangli"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
source_suffix = [".rst", ".md"]
autodoc_typehints = "description"
html_theme = "furo"
html_logo = "_static/logo.png"
