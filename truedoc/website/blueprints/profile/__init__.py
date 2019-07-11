from http import HTTPStatus

from flask import Blueprint
from flask import jsonify
from flask import request

from ...constants import HTTP_METHOD
from ...constants import STATUS

bp = Blueprint('profile', __name__)


@bp.route('/', methods=[HTTP_METHOD.POST])
def create_profile():

    if not request.is_json:
        return jsonify(
            error_code=HTTPStatus.BAD_REQUEST,  # 400
            status=STATUS.ERROR,
        )

    else:
        return jsonify(

            status=STATUS.SUCCESS
        )


