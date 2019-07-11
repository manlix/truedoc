from http import HTTPStatus

from flask import Blueprint
from flask import jsonify
from flask import request

from ....constants import HTTP_METHOD
from ....constants import STATUS

from ....db import db

bp = Blueprint('profile', __name__)


# Create profile
@bp.route('/', methods=[HTTP_METHOD.POST])
def create_profile():
    """Create profile."""

    if not request.is_json:
        return jsonify(
            error_code=HTTPStatus.BAD_REQUEST,  # 400
            status=STATUS.ERROR,
        )

    else:

        profile = db.models.Profile(
            email=request.json['email'],
        )

        profile.set_password(request.json['password'])

        db.Profile.create_profile(profile)

        return jsonify(
            status=STATUS.SUCCESS,
        )


# List pr
@bp.route('/', methods=[HTTP_METHOD.GET])
def list_profiles():
    """List profiles."""
    return jsonify(
        status=STATUS.SUCCESS,
        users=db.Profile.list_all(),
    )
