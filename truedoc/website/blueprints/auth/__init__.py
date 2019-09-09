"""Blueprint: auth by credentials pair.."""
from flask import Blueprint
from flask import request

import truedoc.exceptions

from truedoc import token
from truedoc.db import db
from truedoc.db import schemas
from truedoc.response import success

bp = Blueprint('auth', __name__)


@bp.route('/', methods=['POST'])
def authentication():
    """Authentication."""

    # Schemas
    profile_auth_schema = schemas.ProfileAuthSchema()
    profile_tokens_schema = schemas.ProfileTokensSchema()

    profile_data = profile_auth_schema.load(request.get_json())

    try:
        profile = db.Profile.load(profile_data['email'])
        profile.check_password(profile_data['password'])
    except (
            truedoc.exceptions.ProfileDoesNotExist,
            truedoc.exceptions.ProfileInvalidPassword,
    ):
        raise truedoc.exceptions.ProfileUnauthorized

    tokens_data = profile_tokens_schema.load(token.create_tokens(profile_id=profile.profile_id))

    return success(result=tokens_data)
