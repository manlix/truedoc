from flask import Blueprint
from ....response import failure

bp = Blueprint('error', __name__)


@bp.app_errorhandler(401)
def error_handler_401(e):
    return failure(http_code=401)


@bp.app_errorhandler(404)
def error_handler_404(e):
    return failure(http_code=404)
