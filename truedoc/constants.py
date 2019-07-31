"""Project constants."""


class STATUS:
    """Possible status result of operation in response."""
    ERROR = 'error'
    SUCCESS = 'success'


class SIZE:
    """Standard sizes."""
    BYTE = 1
    KILOBYTE = 1024 * BYTE
    MEGABYTE = 1024 * KILOBYTE
