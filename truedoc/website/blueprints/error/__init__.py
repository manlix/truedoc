from http import HTTPStatus

from flask import Blueprint

import werkzeug.exceptions

from truedoc.response import failure

bp = Blueprint('error', __name__)


@bp.app_errorhandler(HTTPStatus.UNAUTHORIZED)
def error_handler_401(e):
    return failure(http_code=HTTPStatus.UNAUTHORIZED)


@bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def error_handler_404(e):
    return failure(http_code=HTTPStatus.NOT_FOUND)


@bp.app_errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def error_handler_405(e):
    return failure(http_code=HTTPStatus.METHOD_NOT_ALLOWED)


@bp.app_errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    """Catch incorrect JSON in requests with Content-Type = application/json"""
    return failure(
        http_code=werkzeug.exceptions.BadRequest.code,
        description=werkzeug.exceptions.BadRequest.description,
    )
