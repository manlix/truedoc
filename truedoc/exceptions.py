"""Exception classes for truedoc-related errors."""
from http import HTTPStatus


class TruedocError(Exception):
    pass


#########################
#
# PROFILE
#
#########################

class ProfileError(TruedocError):
    pass


class ProfileAlreadyExistsError(ProfileError):
    http_code = HTTPStatus.CONFLICT  # 409


class ProfileDoesNotExist(ProfileError):
    http_code = HTTPStatus.NOT_ACCEPTABLE  # 406


#########################
#
# DOCUMENT
#
#########################

class DocumentError(TruedocError):
    pass


class DocumentNoFileInRequest(DocumentError):
    http_code = HTTPStatus.NOT_ACCEPTABLE  # 406
