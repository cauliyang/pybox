"""Pybox."""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore
try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .__main__ import main
from .commands import gfile
from .commands import gfolder
from .commands import slack
from .commands import asyncdown
from . import utils

__all__ = ["__version__", "main", "gfile", "gfolder", "slack", "asyncdown", "utils"]
