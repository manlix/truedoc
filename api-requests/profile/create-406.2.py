"""Создание профиля, с некорректным email адресом.
Должен возвращать ошибку: 406 (Not Acceptable).
"""
import requests

endpoint = 'http://truedoc-app.localhost/profile/'

payload = dict(
    email='invalid_email',
    password='password',
)

r = requests.post(endpoint, json=payload)

assert r.status_code == 406  # 406 (Not Acceptable)
