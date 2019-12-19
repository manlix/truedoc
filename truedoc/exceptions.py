"""Exception classes for truedoc-related errors."""
from http import HTTPStatus
from marshmallow.exceptions import MarshmallowError  # Used in 'truedoc.app'
from sqlalchemy.exc import SQLAlchemyError  # Used in 'truedoc.app'


class TruedocError(Exception):
    """General exception for Truedoc."""

    http_code = HTTPStatus.INTERNAL_SERVER_ERROR
    description = HTTPStatus.INTERNAL_SERVER_ERROR.description


#########################
#
# PROFILE
#
#########################

class ProfileError(TruedocError):
    """General exception for 'profile' routines."""


class ProfileAlreadyExistsError(ProfileError):
    """Child profile exception: profile already exists."""
    http_code = HTTPStatus.CONFLICT  # 409
    description = 'Profile with given email already exists'


class ProfileDoesNotExist(ProfileError):
    """Child profile exception: given profile_id doesn't exist."""
    http_code = HTTPStatus.NOT_ACCEPTABLE  # 406
    description = 'Profile with given profile_id does not exist'


class ProfileIsNotAvailableForDeleting(ProfileError):
    """Child profile exception: given profile is not available for deleting."""
    http_code = HTTPStatus.NOT_ACCEPTABLE  # 406
    description = 'Profile is not available for deleting due to has documents'


class ProfileUnauthorizedError(ProfileError):
    """Child profile exception: either 'profile_id or email' or password is invalid."""
    http_code = HTTPStatus.UNAUTHORIZED  # 401
    description = 'Unauthorized by invalid credentials for profile'


class ProfileInvalidPassword(ProfileError):
    """Child profile exception: invalid password."""
    http_code = HTTPStatus.UNAUTHORIZED  # 401
    description = 'Invalid password for given profile'


#########################
#
# DOCUMENT
#
#########################

class DocumentError(TruedocError):
    """General exception for 'document' entities."""


class DocumentNoFileInRequest(DocumentError):
    """Child exception for 'document': there isn't file data in request."""
    http_code = HTTPStatus.NOT_ACCEPTABLE  # 406
    description = 'No file data in request'


class DocumentDoesNotExist(DocumentError):
    """Child document exception: given document does not exist."""

    http_code = HTTPStatus.NOT_FOUND  # 404
    description = 'Document does not exist'


#########################
#
# JWT
#
#########################

class TokenError(TruedocError):
    """General exception for JWT."""
    http_code = HTTPStatus.UNAUTHORIZED  # 401
    description = 'Invalid token'


class TokenNoValidTokenInHeaderError(TokenError):
    """Child exception for 'token'."""
    description = 'No valid token in header'


#########################
#
# BOOKMYTIME
#
#########################

class BookmytimeError(TruedocError):
    """General exception for 'Bookmytime' routines."""


class BookmytimeDateAlreadyExistsError(BookmytimeError):
    """Child exception: date already exists for this profile."""
    http_code = HTTPStatus.CONFLICT  # 409
    description = 'Given date already exists'


class BookmytimeDateDoesNotExist(BookmytimeError):
    """Child exception: given date does not exist for this profile."""

    http_code = HTTPStatus.NOT_FOUND  # 404
    description = 'Date does not exist'


class BookmytimeTimeAlreadyExistsError(BookmytimeError):
    """Child exception: time already exists for this profile."""
    http_code = HTTPStatus.CONFLICT  # 409
    description = 'Given time already exists'


class BookmytimeViolationError(BookmytimeError):
    """Child exception: access violation."""
    http_code = HTTPStatus.FORBIDDEN  # 403
    description = 'Given date does not belong to this profile'
