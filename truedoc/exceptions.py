"""Exception classes for truedoc-related errors."""
from http import HTTPStatus


class TruedocError(Exception):
    """General exception for Truedoc."""


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


class ProfileDoesNotExist(ProfileError):
    """Child profile exception: given profile_id doesn't exist."""
    http_code = HTTPStatus.NOT_ACCEPTABLE  # 406


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
