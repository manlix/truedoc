from typing import Tuple

import pytest
import requests


# TODO: do NOT duplicate this function in all modules
def expected_result(expected_code: int, r, error_msg: str) -> str:
    """Show expected HTTP code and related message.

    :param expected_code: int — expected HTTP code
    :param r: Requests response
    :param error_msg: str — small detailed message of the error
    :return: str
    """

    return f'Status code ({r.status_code}) is NOT {expected_code}. {error_msg[0].capitalize()}{error_msg[1:]}: {r.text}'


@pytest.fixture(autouse=True)
def profile_lifecycle():
    """Create and delete profile during session."""

    payload = dict(
        email='test@example.com',
        password='password',
    )

    # Create profile
    r = requests.post('http://truedoc-app.localhost/profile/', json=payload)
    excepted_code = 200
    assert r.status_code == excepted_code, expected_result(
        excepted_code,
        r,
        f'cannot create profile [{payload["email"]}]',
    )
    profile_id = r.json()['result']['profile_id']

    yield

    # Delete profile
    r = requests.delete(f'http://truedoc-app.localhost/profile/{profile_id}')
    excepted_code = 200
    assert r.status_code == excepted_code, expected_result(
        excepted_code,
        r,
        f'cannot delete profile [{payload["email"]}]',
    )


@pytest.fixture()
def endpoint():
    """Endpoint for 'auth'."""
    return 'http://truedoc-app.localhost/auth/'


def test_auth_success(endpoint):
    """Test success auth."""

    payload = dict(
        email='test@example.com',
        password='password',
    )

    r = requests.post(endpoint, json=payload)

    excepted_code = 200
    assert r.status_code == excepted_code, expected_result(
        excepted_code,
        r,
        'cannot make auth by login/password',
    )


def test_auth_invalid_password(endpoint):
    """Test failure auth."""

    payload = dict(
        email='test@example.com',
        password='INVALID_PASSWORD',
    )

    r = requests.post(endpoint, json=payload)

    excepted_code = 401
    assert r.status_code == excepted_code, expected_result(
        excepted_code,
        r,
        'should get failure instead successful',
    )
