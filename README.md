# Beauty City Bot
Реализация Telegram-бота для сети салонов красоты.

## О проекте
Проект реализован силами [amicuswat](https://github.com/amicuswat), [xakars](https://github.com/xakars) и [brabada](https://github.com/Brabada).

Backend: Django ORM 4.1.

## Как установить
Установить пакеты:
```shell
$ pip install -r requirements.txt
```

Создать файл окружения `.env` и прописать следующие поля (при необходимости):

- DEBUG (по умолч. `true`) - запуск сервера в режиме DEBUG;
- DATABASE (по умолч. `sqlite:///db.sqlite3`) - указание типа БД и название файла с БД. Подробности по ссылке: 
https://pypi.org/project/dj-database-url/;
- ALLOWED_HOSTS (по умолч. `localhost,127.0.0.1`) - список разрешенных хостов для запуска сервера.


## Как запустить
```shell
$ cd %рабочий_каталог%
$ python manage.py runserver
```

## REST API

Получить все салоны:
```text
api/v1/beauty_saloon_db/saloon/all/
```