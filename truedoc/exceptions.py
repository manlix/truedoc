"""Exception classes for truedoc-related errors."""
from http import HTTPStatus


class TruedocError(Exception):
    pass


class ProfileError(TruedocError):
    pass


class ProfileAlreadyExistsError(ProfileError):
    http_code = HTTPStatus.CONFLICT  # 409
