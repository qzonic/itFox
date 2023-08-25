# CI/CD
![Workflow](https://github.com/qzonic/itFox/actions/workflows/main.yml/badge.svg)

# Стек
<img src="https://img.shields.io/badge/Python-4169E1?style=for-the-badge"/> <img src="https://img.shields.io/badge/Django-008000?style=for-the-badge"/> <img src="https://img.shields.io/badge/DRF-800000?style=for-the-badge"/> <img src="https://img.shields.io/badge/Docker-00BFFF?style=for-the-badge"/> <img src="https://img.shields.io/badge/PostgreSQL-87CEEB?style=for-the-badge"/> <img src="https://img.shields.io/badge/Nginx-67c273?style=for-the-badge"/> <img src="https://img.shields.io/badge/Gunicorn-06bd1e?style=for-the-badge"/>

# Описание проекта:

**Проект itFox**

Этот проект позволяет каждому пользователю создать новость. Все пользователи могут получать
списки всех новостей с пагинацией. Пользователи могут удалять и изменять свои
новости. Админ может удалять и изменять любую новость.

# Как запустить проект:

*Клонировать репозиторий и перейти в него в командной строке:*
```
https://github.com/qzonic/itFox.git
```
```
cd itFox/
```

В директории UrbanMedic нужно создать .env файл, в котором указывается 
SECRET_KEY, DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT.
Например:
```
SECRET_KEY='django-insecure-w2rvabrrx4_u=qfar0k*%zumx3l*d8@+v==%0o-i8k3(&9ut^='

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

*Теперь необходимо собрать Docker-контейнеры:*
```
docker-compose up -d
```

*После сборки контейнеров, нужно прописать следующие команды по очереди:*
```
docker-compose exec web python3 manage.py migrate
```

```
docker-compose exec web python3 manage.py createsuperuser
```

```
docker-compose exec web python3 manage.py collectstatic --no-input
```

*Теперь проект доступен по адресу:*
```
http://127.0.0.1/
```

*Эндпоинты для взаимодействия с API можно посмотреть в документации по адресу:*
```
http://127.0.0.1/api/v1/redoc/
```

### Автор
[![telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/qzonic)
