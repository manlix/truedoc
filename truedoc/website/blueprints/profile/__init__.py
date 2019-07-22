from flask import Blueprint
from flask import request

from flask import jsonify

from ....constants import STATE
from ....db import db
from ....messages import Error

bp = Blueprint('profile', __name__)


# Create profile
@bp.route('/', methods=['POST'])
def create_profile():
    """Create profile."""

    if not request.is_json:
        return jsonify(
            error=Error.IS_NOT_JSON,
            state=STATE.ERROR,
        )

    else:

        profile = db.models.Profile(
            email=request.json['email'],
        )

        profile.set_password(request.json['password'])

        db.Profile.create_profile(profile)

        return jsonify(
            state=STATE.SUCCESS,
        )
