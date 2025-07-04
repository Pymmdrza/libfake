from ._version import __version__, __author__, __description__, __license__

from .core import FakeName
from .exceptions import NameError, DataFileError

# This makes the main class and exceptions directly importable
__all__ = ["FakeName", "NameError", "DataFileError", "__version__"]


# CLI entry point
def main():
    """Entry point for CLI when installed via pip."""
    from .cli import main as cli_main

    cli_main()
