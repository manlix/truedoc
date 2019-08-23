"""Standard responses for API: success & failure."""
from http import HTTPStatus

from flask import jsonify
from .constants import STATUS


def failure(http_code=HTTPStatus.NOT_ACCEPTABLE, description=None, **kwargs):
    """Default return code is 406 if $http_code was not set."""
    response = {'status': STATUS.ERROR, **kwargs}

    if description is not None:
        response['description'] = description

    if http_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response['internal_error'] = True

    return jsonify(response), http_code


def success(http_code=HTTPStatus.OK, description=None, **kwargs):
    """Default return code is 200 if $http_code was not set."""
    response = {'status': STATUS.SUCCESS, **kwargs}

    if description is not None:
        response['description'] = description

    return jsonify(response), http_code
