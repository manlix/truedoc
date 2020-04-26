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


def test_create_and_delete_profile(endpoints):
    """Create and delete profile."""
    payload = dict(
        email='test@example.com',
        password='password',
    )

    r = requests.post(f'{endpoints["profile"]}', json=payload)

    expected_code = 200
    assert expected_code == r.status_code, expected_result(
        expected_code,
        r,
        f'cannot create new profile [{payload["email"]}]',
    )

    profile_id = r.json()['result']['profile_id']

    r = requests.delete(f'{endpoints["profile"]}{profile_id}')

    expected_code = 200
    assert expected_code == r.status_code, expected_result(
        expected_code,
        r,
        f'cannot create new profile [{profile_id}]',
    )


def test_create_profile_bad_request(endpoints):
    """Create profile: 400 — Bad request."""
    headers = {
        'Content-type': 'application/json'
    }

    r = requests.post(f'{endpoints["profile"]}', headers=headers)

    expected_code = 400
    assert expected_code == r.status_code, expected_result(
        expected_code,
        r,
        'Should get failure (Bad request) instead',
    )


def test_create_profile_not_acceptable(endpoints):
    """Create profile: 406 — Not Acceptable."""
    payload = dict(
        email='test@example.com',
    )

    r = requests.post(f'{endpoints["profile"]}', json=payload)

    expected_code = 406
    assert expected_code == r.status_code, expected_result(
        expected_code,
        r,
        'should get failure (Not acceptable) instead',
    )


def test_create_profile_invalid_email(endpoints):
    """Create profile: 406 — Not Acceptable."""
    payload = dict(
        email='invalid_email',
        password='password',
    )

    r = requests.post(f'{endpoints["profile"]}', json=payload)

    expected_code = 406
    assert expected_code == r.status_code, expected_result(
        expected_code,
        r,
        'should get failure (Not acceptable) instead',
    )
