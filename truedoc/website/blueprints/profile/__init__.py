from flask import Blueprint
from flask import request

from marshmallow import ValidationError

from ....response import failure, success

from ....db import db

from ....db import schemas

bp = Blueprint('profile', __name__)


# Create profile
@bp.route('/', methods=['POST'])
def create_profile():
    """Create profile."""

    profile_schema = schemas.ProfileSchema()
    try:
        data = profile_schema.load(request.get_json())
    except ValidationError as err:
        return failure(errors=err.messages)

    else:
        profile = db.models.Profile(email=data['email'])
        profile.set_password(data['password'])
        db.Profile.create(profile)

        return success()
