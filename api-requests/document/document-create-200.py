"""Создание документа (успех).
Должен возвращать: 200 (OK)."""
import requests

from truedoc import constants

endpoint = 'http://truedoc-app.localhost/document/'

# Upload file with size=1KB
payload = {
    'data': {
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

r = requests.post(endpoint, **payload)

assert r.status_code == 200  # OK
