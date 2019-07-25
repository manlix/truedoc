from http import HTTPStatus

from flask import jsonify
from .constants import STATUS


# TODO: add skipping 'http_code' key from 'kwargs' because HTTP code already has this code
def failure(**kwargs):
    return jsonify({'status': STATUS.ERROR, **kwargs}), \
           kwargs['http_code'] if 'http_code' in kwargs else HTTPStatus.BAD_REQUEST  # 400


# TODO: add skipping 'http_code' key from 'kwargs' because HTTP code already has this code
def success(**kwargs):
    return jsonify({'status': STATUS.SUCCESS, **kwargs}), \
           kwargs['http_code'] if 'http_code' in kwargs else HTTPStatus.OK  # 200
