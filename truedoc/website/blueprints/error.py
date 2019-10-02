from http import HTTPStatus

from flask import Blueprint

from truedoc.response import failure

bp = Blueprint('error', __name__)


@bp.app_errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler_400(e):
    """Catch incorrect JSON in requests with Content-Type = application/json"""
    return failure(http_code=HTTPStatus.BAD_REQUEST, description=HTTPStatus.BAD_REQUEST.description)


@bp.app_errorhandler(HTTPStatus.UNAUTHORIZED)
def error_handler_401(e):
    return failure(http_code=HTTPStatus.UNAUTHORIZED, description=HTTPStatus.UNAUTHORIZED.description)


@bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def error_handler_404(e):
    return failure(http_code=HTTPStatus.NOT_FOUND, description=HTTPStatus.NOT_FOUND.description)


@bp.app_errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def error_handler_405(e):
    return failure(http_code=HTTPStatus.METHOD_NOT_ALLOWED, description=HTTPStatus.METHOD_NOT_ALLOWED.description)
