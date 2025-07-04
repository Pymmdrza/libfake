__version__ = "1.0.0"

from .core import FakeName
from .exceptions import NameError, DataFileError

# This makes the main class and exceptions directly importable
__all__ = ["FakeName", "NameError", "DataFileError"]
