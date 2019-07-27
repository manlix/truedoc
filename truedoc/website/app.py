from http import HTTPStatus

from flask import Flask

from truedoc.db import db

from truedoc.exceptions import TruedocError
from truedoc.response import failure
from truedoc.website.blueprints import error
from truedoc.website.blueprints import profile

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://f6de8903ce254aa89bfc41f021320f5d@sentry.io/1513696",
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
app.register_blueprint(error.bp)
app.register_blueprint(profile.bp, url_prefix='/profile')


# TODO: see error handling manual
# https://flask.palletsprojects.com/en/1.1.x/errorhandling/

@app.errorhandler(TruedocError)
def handle_exception(e):
    http_code = e.http_code if hasattr(e, 'http_code') else HTTPStatus.INTERNAL_SERVER_ERROR
    return failure(http_code=http_code, description=e.args)
