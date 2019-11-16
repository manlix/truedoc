"""Decorators."""

import functools

from flask import request

import marshmallow.exceptions

from truedoc import tokens
import truedoc.exceptions
from truedoc.db import schemas


def require_valid_token(func):
    """Decorator for sections required valid 'access_token'."""

    @functools.wraps(func)
    def wrapper(*arg, **kwargs):

        headers = dict(request.headers)  # TODO: think is it wrong to use 'dict()' here or not?
        authorization_header_schema = schemas.AuthorizationHeaderSchema()

        try:
            authorization_header_data = authorization_header_schema.load(headers)

        except marshmallow.exceptions.ValidationError:
            raise truedoc.exceptions.TokenNoValidTokenInHeaderError

        tokens.is_valid_token(authorization_header_data['token'])

        return func(*arg, **kwargs)

    return wrapper
