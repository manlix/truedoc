"""Создание документа (успех).
Должен возвращать: 200 (OK)."""
import requests

from truedoc import constants

endpoint_document = 'http://truedoc-app.localhost/document/'
endpoint_profile = 'http://truedoc-app.localhost/profile/'

payload = dict(
    email='hello@example.com',
    password='password',
)

r = requests.post(endpoint_profile, json=payload)

assert r.status_code == 200, 'Cannot create profile'

# Upload file with size=1KB
payload = {
    'data': {
        'profile_id': r.json()['result']['profile_id'],
        'title': 'Document Simple Title: 1KB',
    },
    'files': [
        (
            'document',
            (
                'file_1KB.txt',
                1 * constants.SIZE.KILOBYTE * 'x',
            )
        ),
    ]
}

r = requests.post(endpoint_document, **payload)

assert r.status_code == 200, 'Cannot create document'  # OK
