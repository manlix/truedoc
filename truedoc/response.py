from flask import jsonify
from .constants import STATUS


def failure(http_code=400, description=None, **kwargs):
    """Default return code is 400 if $http_code was not set."""
    response = {'status': STATUS.ERROR, **kwargs}

    if description is not None:
        response['description'] = description if isinstance(description, str) else description[0]

    return jsonify(response), http_code


def success(http_code=200, description=None, **kwargs):
    """Default return code is 200 if $http_code was not set."""
    response = {'status': STATUS.SUCCESS, **kwargs}

    if description is not None:
        response['description'] = description if isinstance(description, str) else description[0]

    return jsonify(response), http_code
