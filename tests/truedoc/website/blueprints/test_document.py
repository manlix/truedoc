import time

from http import HTTPStatus

import pytest
import requests

import truedoc.constants

res = {}


def authorization_header():
    return {
        'Authorization': f'Bearer {res["access_token"]}'
    }


def expected_result(expected_code: int, r, error_msg: str) -> str:
    """Show expected HTTP code and related message.

    :param expected_code: int — expected HTTP code
    :param r: Requests response
    :param error_msg: str — small detailed message of the error
    :return: str
    """

    return f'Status code ({r.status_code}) is NOT {expected_code}. {error_msg}: {r.text}'


@pytest.fixture(autouse=True)
def profile_lifecycle():
    """Create and delete profile during session."""

    payload = dict(
        email='test@example.com',
        password='password',
    )

    # Create profile
    r = requests.post('http://truedoc-app.localhost/profile/', json=payload)
    assert 200 == r.status_code, expected_result(200, r, 'cannot create profile')

    profile_id = r.json()['result']['profile_id']

    r = requests.post('http://truedoc-app.localhost/auth/', json=payload)
    assert 200 == r.status_code, expected_result(200, r, 'failed authorization')

    access_token = r.json()['result']['access_token']
    refresh_token = r.json()['result']['refresh_token']

    res.update({
        'profile_id': profile_id,
        'access_token': access_token,
        'refresh_token': refresh_token,
    })

    yield

    # Delete profile
    r = requests.delete(f'http://truedoc-app.localhost/profile/{profile_id}', headers=authorization_header())
    assert 200 == r.status_code, expected_result(200, r, 'cannot delete profile')


@pytest.fixture()
def endpoints():
    """Endpoints dict."""
    return {
        'auth': 'http://truedoc-app.localhost/auth/',
        'document': 'http://truedoc-app.localhost/document/',
        'profile': 'http://truedoc-app.localhost/profile/',
    }


@pytest.fixture()
def max_retries():
    """Max retries to get document."""
    return 5


@pytest.mark.parametrize('filesize', [
    0 * truedoc.constants.SIZE.BYTE,  # Invalid filesize. 0 — empty document is not allowed.
    512 * truedoc.constants.SIZE.BYTE,  # 512B
    1 * truedoc.constants.SIZE.KILOBYTE,  # 1KiB
    100 * truedoc.constants.SIZE.KILOBYTE,  # 100KiB
    250 * truedoc.constants.SIZE.KILOBYTE,  # 250KiB
    1 * truedoc.constants.SIZE.MEGABYTE,  # 1MiB
    4 * truedoc.constants.SIZE.MEGABYTE,  # 4MiB
])
def test_document_lifecycle(
        endpoints,
        max_retries,
        filesize,
):
    """Document lifecycle."""
    payload = {
        'data': {
            'profile_id': res['profile_id'],
            'title': f'Test document title with filesize {filesize}',
        },
        'files': [
            (
                'document',
                (
                    'file.txt',
                    'x' * filesize,
                )
            ),
        ]
    }

    # Upload document
    r = requests.post(endpoints['document'], headers=authorization_header(), **payload)

    # Empty document
    if not filesize:
        assert 406 == r.status_code, expected_result(406, r, 'has been send empty document but got OK')
        return

    assert 202 == r.status_code, expected_result(202, r, 'cannot create document')

    document_id = r.json()['result']['document_id']

    # Waiting that document task state == 'SUCCESS'
    for _ in range(max_retries):  # TODO: think about retries by 'requests'
        r = requests.get(f'http://truedoc-app.localhost/document/{document_id}/state', headers=authorization_header())
        assert 200 == r.status_code, expected_result(200, r, f'cannot get task for processing document ({document_id})')

        assert 'result' in r.json(), f'Not found "result" in response: {r.text}'
        assert 'state' in r.json()['result'], f'Not found "state" in response["result"]: {r.text}'

        assert r.json()['result']['state'] in truedoc.constants.JOB_STATE.ALL_STATES, f'Unknown task state: {r.text}'

        if r.json()['result']['state'] == truedoc.constants.JOB_STATE.SUCCESS:
            break

        time.sleep(1)
    else:
        raise Exception(f'{max_retries} attempts to get task state exceeded')

    # Get document
    r = requests.get(f'{endpoints["document"]}{document_id}', headers=authorization_header())

    assert 200 == r.status_code, expected_result(200, r, f'cannot load document ({document_id})')

    # Delete document
    r = requests.delete(f'{endpoints["document"]}{document_id}', headers=authorization_header())

    assert 200 == r.status_code, expected_result(200, r, f'cannot delete document ({document_id})')


def test_get_document_by_invalid_id(endpoints):
    document_id = 'INVALID_ID_DOCUMENT'
    r = requests.get(f'{endpoints["document"]}{document_id}', headers=authorization_header())

    expected_code = 404
    assert expected_code == r.status_code, expected_result(expected_code, r, f'Document is loaded but must got 404')


def test_get_not_existing_document(endpoints):
    document_id = '00000000-0000-0000-0000-000000000000'
    r = requests.get(f'{endpoints["document"]}{document_id}', headers=authorization_header())

    expected_code = 404
    assert expected_code == r.status_code, expected_result(expected_code, r, f'Document is loaded but must got 404')
