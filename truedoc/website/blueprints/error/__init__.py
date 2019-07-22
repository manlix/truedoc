from http import HTTPStatus

from flask import Blueprint
from flask import jsonify

from ....constants import STATE

bp = Blueprint('error', __name__)


@bp.app_errorhandler(401)
def error_handler_401(e):
    return jsonify(
        error_code=HTTPStatus.UNAUTHORIZED,
        status=STATE.ERROR,
    )


@bp.app_errorhandler(404)
def error_handler_404(e):
    return jsonify(
        error_code=HTTPStatus.NOT_FOUND,
        status=STATE.ERROR,
    )


@bp.app_errorhandler(500)
def error_handler_401(e):
    return jsonify(
        error_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        status=STATE.ERROR,
    )
