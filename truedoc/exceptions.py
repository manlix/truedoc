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
    http_code = HTTPStatus.NOT_ACCEPTABLE  # 406
    description = 'Profile is not available for deleting due to has documents'


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
