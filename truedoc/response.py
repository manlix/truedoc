from http import HTTPStatus

from flask import jsonify
from .constants import STATUS


def failure(**kwargs):
    return jsonify({'status': STATUS.ERROR, **kwargs}), \
           kwargs['http_code'] if 'http_code' in kwargs else HTTPStatus.BAD_REQUEST  # 400


def success(**kwargs):
    return jsonify({'status': STATUS.SUCCESS}), \
           kwargs['http_code'] if 'http_code' in kwargs else HTTPStatus.OK  # 200
