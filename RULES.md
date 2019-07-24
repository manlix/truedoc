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
* Каждый ответ содержит **status** со значением:
    * **success** - для успешных запросов ([коды 2xx](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#2xx_Success))
    * **error** - для неудачных запросов ([коды 4xx и 5xx](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_errors))

