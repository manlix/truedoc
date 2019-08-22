"""Создание профиля, без необходимых полей (пароль, поле 'password').
Должен возвращать ошибку: 406 (Not Acceptable).
"""
import requests

endpoint = 'http://truedoc-app.localhost/profile/'
payload = dict(
    email='hello@example.com',
)

r = requests.post(endpoint, json=payload)

assert r.status_code == 406  # 406 (Not Acceptable)
