"""Создание документа (успех).
Должен возвращать: 200 (OK)."""
import requests

endpoint = 'http://truedoc-app.localhost/document/'
payload = dict(
    title='Document Simple Title',
    document='password',
)

r = requests.post(endpoint, json=payload)

assert r.status_code in (
    200,  # 200 (OK)
    409,  # 409 (Conflict)
)



# Test request: http -v -f POST truedoc-app.localhost/document/  title="document_title" document@~/checm.docx