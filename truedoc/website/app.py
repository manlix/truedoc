from flask import Flask

from .blueprints import error
from .blueprints import profile

from ..db import db
from ..response import failure

app = Flask(__name__)
app.register_blueprint(error.bp)
app.register_blueprint(profile.bp, url_prefix='/profile')


# See Generic Exception Handlers:
# https://flask.palletsprojects.com/en/1.1.x/errorhandling/

# TODO: think about parse for 'e'
@app.errorhandler(Exception)
def handler_all_exceptions(e):
    """Catch all unhandled exception."""
    return failure(http_code=500)
