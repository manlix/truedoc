"""Создание профиля (неудача).
Должен возвращать: 400 (Bad request).
"""
import requests

endpoint = 'http://truedoc-app.localhost/profile/'
headers = {
    'Content-type': 'application/json'
}

r = requests.post(endpoint, headers=headers)

assert r.status_code == 400  # 400 (Bad request)
