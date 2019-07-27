# Правила проекта

## Архитектура взаимодействия

* Используется [RESTful API](https://en.wikipedia.org/wiki/Representational_state_transfer#Applied_to_Web_services) ([CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete))

Действие | HTTP-метод | Контекст
-------- | ---------- | --------
Create   | POST       | Объект
Read     | GET        | Объект
Update   | PATCH      | Объект 
Delete   | DELETE     | Объект
  

* **JSON** является основным форматом для входных и выходных данных (включая ошибки).
* Каждый ответ содержит **status** со значением **success** (для успешных запросов) и **error** (для неудачный запросов) с уточняющей информацией в поле **description**:

* Ответ на удачный запрос:
```json
{
    "status": "success"
}
```
* Ответ на неудачный запрос:
```json
{
  "status": "error",
  "description": "Bad request.",
  "error_fields": {
    "email": [
      "Incorrect email."    
    ],
    "password": [
      "Missing data for required field."
    ]  
  } 
}
```


* **success** - для успешных запросов ([коды 2xx](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#2xx_Success))
* **error** - для неудачных запросов ([коды 4xx и 5xx](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_errors))

