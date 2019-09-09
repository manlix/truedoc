"""Project constants."""


class STATUS:  # pylint: disable=too-few-public-methods
    """Possible status result of operation in response."""
    ERROR = 'error'
    SUCCESS = 'success'


class SIZE:  # pylint: disable=too-few-public-methods
    """Standard sizes."""
    BYTE = 1
    KILOBYTE = 1024 * BYTE
    MEGABYTE = 1024 * KILOBYTE


class TIME:
    """Time."""
    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
