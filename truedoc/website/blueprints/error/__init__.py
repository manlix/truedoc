from flask import Blueprint
from truedoc.response import failure

bp = Blueprint('error', __name__)


@bp.app_errorhandler(401)  # UNAUTHORIZED
def error_handler_401(e):
    return failure(http_code=401)


@bp.app_errorhandler(404)  # NOT_FOUND
def error_handler_404(e):
    return failure(http_code=404)


@bp.app_errorhandler(405)  # METHOD_NOT_ALLOWED
def error_handler_405(e):
    return failure(http_code=405)
