"""
Exceptions
"""
from colors import red


class InvalidDataType(Exception):
    """Exit code: 128
    This can happen when you try to pass a directory to `data` or when you
    try to pass a directory to `template`
    without '/', this can be interpreted as a file and throw this error.
    """

    def __init__(self,
                 message=f"{red('[ERROR]')} Invalid data type, try '-' for stdin, "
                 "valid URL or path on your file system."):
        self.message = message
        super().__init__(self.message)


class InvalidInput(Exception):
    """Exit code: 127"""

    def __init__(self, message=f"{red('[ERROR]')} Invalid input, "
                 "stdin can be used for data or template but not both."):
        self.message = message
        super().__init__(self.message)
