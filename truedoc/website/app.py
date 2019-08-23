"""Application: Truedoc."""
from http import HTTPStatus

from flask import Flask

import sentry_sdk

from truedoc.exceptions import SQLAlchemyError
from truedoc.exceptions import TruedocError

from truedoc.response import failure
from truedoc.website.blueprints import document
from truedoc.website.blueprints import error
from truedoc.website.blueprints import profile

sentry_sdk.init("https://f6de8903ce254aa89bfc41f021320f5d@sentry.io/1513696")

app = Flask(__name__)

app.register_blueprint(error.bp)
app.register_blueprint(profile.bp, url_prefix='/profile')
app.register_blueprint(document.bp, url_prefix='/document')


# TODO: see error handling manual
# https://flask.palletsprojects.com/en/1.1.x/errorhandling/

@app.errorhandler(TruedocError)
def handle_exception(e):
    """Common handler for exceptions TruedocError type."""
    http_code = e.http_code if hasattr(e, 'http_code') else HTTPStatus.INTERNAL_SERVER_ERROR

    # TODO: log exception here by logging.exception(...)
    return failure(http_code=http_code, description=e.args)


@app.errorhandler(SQLAlchemyError)
def handle_exception(exc):
    """Error handler for any errors by SQLAlchemy."""

    http_code = HTTPStatus.INTERNAL_SERVER_ERROR

    # TODO: log exception here by logging.exception(...)
    return failure(http_code=http_code, description=HTTPStatus.INTERNAL_SERVER_ERROR.description)
