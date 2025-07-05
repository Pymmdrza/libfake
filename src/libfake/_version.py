"""
Version information for LibFake package.
This is the single source of truth for version numbers.

Requires Python 3.8+
"""

__author__ = "Mmdrza"
__author_email__ = "pymmdrza@gmail.com"
__description__ = (
    "A professional library for generating realistic fake names and emails"
)
__url__ = "https://github.com/Pymmdrza/libfake"

# Version components for programmatic access
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 3
VERSION_SUFFIX = ""  # e.g., "a1", "b1", "rc1", "" for stable

# Build the version string
if VERSION_SUFFIX:
    __version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}{VERSION_SUFFIX}"
else:
    __version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

# Additional metadata
__license__ = "MIT"
__copyright__ = "2025 Mmdrza"
