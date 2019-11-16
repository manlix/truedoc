from flask import Blueprint
from flask import request

from truedoc.db import db
from truedoc.db import schemas
from truedoc.response import success

bp = Blueprint('profile', __name__)


@bp.route('/', methods=['POST'])
def create_profile():
    """Create profile."""

    profile_schema = schemas.ProfileSchema()
    data = profile_schema.load(request.get_json())

    profile = db.models.Profile(email=data['email'])
    profile.set_password(data['password'])
    db.Profile.create(profile)

    return success(result=profile_schema.dump(profile))


# TODO: drop or move to admin scope
@bp.route('/', methods=['GET'])
def list_profiles():
    """List profiles."""

    profiles_schema = schemas.ProfileSchema(many=True)
    profiles = profiles_schema.dump(db.Profile.list_all())

    return success(result=profiles)


# TODO: drop or move to admin scope
@bp.route('/<uuid:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Delete given profile_id."""

    profile_id = str(profile_id)

    profile = db.Profile.load(profile_id)
    db.Profile.delete(profile)

    return success()
