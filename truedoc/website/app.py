from flask import Flask

from .blueprints import error
from .blueprints import profile

app = Flask(__name__)

app.register_blueprint(error.bp)
app.register_blueprint(profile.bp, url_prefix='/profile')
