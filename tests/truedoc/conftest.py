import pytest

import truedoc.common

MANY_UUID4_LEN = 1000


@pytest.fixture()
def one_uuid4():
    """1 uuid4 item."""
    return truedoc.common.uuid4()


@pytest.fixture()
def many_uuid4():
    """List of uuid4 items."""
    return [truedoc.common.uuid4() for _ in range(MANY_UUID4_LEN)]


@pytest.fixture()
def many_uuid4_len(many_uuid4):
    """Length of uuid4 items list."""
    return MANY_UUID4_LEN


@pytest.fixture()
def endpoints():
    """Endpoints dict."""
    return {
        'auth': 'http://truedoc-app.localhost/auth/',
        'document': 'http://truedoc-app.localhost/document/',
        'profile': 'http://truedoc-app.localhost/profile/',
    }
