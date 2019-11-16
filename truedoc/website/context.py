"""Work with current request context."""
from typing import (
    Any,
    NoReturn,
    Union,
)

from flask import _request_ctx_stack


def add(key: str, value: Union[dict, str]) -> NoReturn:
    """Save 'key' with 'value' to current request context. Update 'key' value if already exists.

    :param key: key to save
    :param value: data to save with key 'key'
    :return: nothing
    """
    ctx = _request_ctx_stack.top

    if ctx is not None:
        setattr(ctx, key, value)


def get(key: str) -> Any:
    """Read 'key' from current request context.

    :param key: key name to get
    :return: None
    """
    ctx = _request_ctx_stack.top

    if ctx is not None:
        return getattr(ctx, key)
