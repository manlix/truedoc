"""Application: Truedoc."""
from http import HTTPStatus
import logging

from flask import Flask

import sentry_sdk

from truedoc.exceptions import MarshmallowError
from truedoc.exceptions import SQLAlchemyError
from truedoc.exceptions import TruedocError

from truedoc.response import failure
from truedoc.website.blueprints import document
from truedoc.website.blueprints import error
from truedoc.website.blueprints import profile

logging.basicConfig(
    level=logging.WARNING,
    format='[%(levelname)s] - [%(name)s] - [%(asctime)s] - %(message)s',
)

logger = logging.getLogger(__name__)

sentry_sdk.init("https://f6de8903ce254aa89bfc41f021320f5d@sentry.io/1513696")

app = Flask(__name__)

app.register_blueprint(error.bp)
app.register_blueprint(profile.bp, url_prefix='/profile')
app.register_blueprint(document.bp, url_prefix='/document')


# TODO: see error handling manual
# https://flask.palletsprojects.com/en/1.1.x/errorhandling/

@app.errorhandler(TruedocError)
def handle_exception_truedocerror(exc):
    """Common handler for exceptions TruedocError type."""
    http_code = exc.http_code
    description = exc.description

    logger.exception('[ErrorHandler:TruedocError]')
    return failure(http_code=http_code, description=description)


@app.errorhandler(SQLAlchemyError)
def handle_exception_sqlalchemyerror(exc):
    """Error handler for any errors by SQLAlchemy."""

    http_code = HTTPStatus.INTERNAL_SERVER_ERROR
    description = HTTPStatus.INTERNAL_SERVER_ERROR.description

    logger.exception('[ErrorHandler:SQLAlchemyError]')
    return failure(http_code=http_code, description=description)


@app.errorhandler(MarshmallowError)
def handle_exception_validationerror(exc):
    """Error handler for any errors by Marshmallow."""

    http_code = HTTPStatus.NOT_ACCEPTABLE

    logger.exception('[ErrorHandler:MarshmallowError]')
    return failure(http_code=http_code, error_fields=exc.messages)


@app.errorhandler(Exception)
def handle_exception_unknown(exc):
    """Error handler for any unknown exceptions."""

    http_code = HTTPStatus.INTERNAL_SERVER_ERROR

    logger.exception('[ErrorHandler:Exception]')
    return failure(http_code=http_code)
