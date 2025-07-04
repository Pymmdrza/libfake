class NameError(Exception):
    """Base exception class for all errors raised by NameForge."""
    pass

class DataFileError(NameError):
    """Raised when a required data file (e.g., NAMES.DIC) cannot be loaded."""
    def __init__(self, path: str):
        self.path = path
        message = f"Failed to load or read the data file at: {path}"
        super().__init__(message)
