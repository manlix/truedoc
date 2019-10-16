import time

from http import HTTPStatus

import pytest
import requests

import truedoc.constants

res = {}


@pytest.fixture(autouse=True)
def profile_lifecycle():
    """Create and delete profile during session."""

    payload = dict(
        email='test@example.com',
        password='password',
    )

    # Create profile
    r = requests.post('http://truedoc-app.localhost/profile/', json=payload)
    assert 200 == r.status_code, f'Status code ({r.status_code}) is NOT 200. Cannot create profile: {r.text}'

    profile_id = r.json()['result']['profile_id']

    res.update({
        'profile_id': profile_id,
    })

    yield

    # Delete profile
    r = requests.delete(f'http://truedoc-app.localhost/profile/{profile_id}')
    assert 200 == r.status_code, f'Status code ({r.status_code}) is NOT 200. Cannot delete profile: {r.text}'


@pytest.fixture()
def endpoints():
    """Endpoints dict."""
    return {
        'document': 'http://truedoc-app.localhost/document/',
        'profile': 'http://truedoc-app.localhost/profile/',
    }


@pytest.fixture()
def max_retries():
    """Max retries to get document."""
    return 5


@pytest.mark.parametrize('filesize', [
    0 * truedoc.constants.SIZE.BYTE,
    512 * truedoc.constants.SIZE.BYTE,
    1 * truedoc.constants.SIZE.KILOBYTE,
    100 * truedoc.constants.SIZE.KILOBYTE,
    250 * truedoc.constants.SIZE.KILOBYTE,
    1 * truedoc.constants.SIZE.MEGABYTE,
    4 * truedoc.constants.SIZE.MEGABYTE,
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
    r = requests.post(endpoints['document'], **payload)

    # Empty document
    if not filesize:
        assert 406 == r.status_code, f'Status code ({r.status_code}) is NOT 406 due to empty document: {r.text}'
        return

    assert 202 == r.status_code, f'Status code ({r.status_code}) is NOT 202. Cannot create document: {r.text}'

    document_id = r.json()['result']['document_id']

    # Waiting that document task state == 'SUCCESS'
    for _ in range(max_retries):  # TODO: think about retries by 'requests'
        r = requests.get(f'http://truedoc-app.localhost/document/{document_id}/state')
        assert 200 == r.status_code, f'Status code ({r.status_code}) is NOT 200. Cannot get task ({document_id}) state: {r.text}'

        assert 'result' in r.json(), f'Not found "result" in response: {r.text}'
        assert 'state' in r.json()['result'], f'Not found "state" in response["result"]: {r.text}'

        assert r.json()['result']['state'] in truedoc.constants.JOB_STATE.ALL_STATES, f'Unknown task state: {r.text}'

        if r.json()['result']['state'] == truedoc.constants.JOB_STATE.SUCCESS:
            break

        time.sleep(1)
    else:
        raise Exception(f'{max_retries} attempts to get task state exceeded')

    # Get document
    r = requests.get(f'{endpoints["document"]}')

    assert 200 == r.status_code, f'Status code ({r.status_code}) is NOT 200. Cannot load document ({document_id}): {r.text}'

    # Delete document
    r = requests.delete(f'{endpoints["document"]}{document_id}')

    assert 200 == r.status_code, f'Status code ({r.status_code}) is NOT 200. Cannot delete document ({document_id}): {r.text}'
