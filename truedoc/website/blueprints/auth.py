"""Blueprint: auth by credentials pair.."""
from flask import Blueprint
from flask import request

import marshmallow.exceptions

import truedoc.exceptions

from truedoc import tokens
from truedoc.db import db
from truedoc.db import schemas
from truedoc.response import success

bp = Blueprint('auth', __name__)


@bp.route('/', methods=['POST'])
def authentication():
    """Authentication."""

    # Schemas
    profile_auth_schema = schemas.AuthenticationSchema()
    profile_tokens_schema = schemas.AuthorizationTokensSchema()

    profile_data = profile_auth_schema.load(request.get_json())

    try:
        profile = db.Profile.load(profile_data['email'])
        profile.check_password(profile_data['password'])
    except (
            truedoc.exceptions.ProfileDoesNotExist,
            truedoc.exceptions.ProfileInvalidPassword,
    ):
        raise truedoc.exceptions.ProfileUnauthorizedError

    tokens_data = profile_tokens_schema.load(tokens.create_tokens(profile_id=profile.profile_id))

    return success(result=tokens_data)


@bp.route('/check_token', methods=['GET'])
def check_token():
    """Process ${TOKEN} for validating from header: 'Authorization: ${auth_schema} ${TOKEN}'."""

    headers = dict(request.headers)  # TODO: think is it wrong to use 'dict()' here or not?
    authorization_header_schema = schemas.AuthorizationHeaderSchema()

    try:
        authorization_header_data = authorization_header_schema.load(headers)

    except marshmallow.exceptions.ValidationError:
        raise truedoc.exceptions.TokenNoValidTokenInHeaderError

    if tokens.is_token_valid(authorization_header_data['token']):
        return success()
