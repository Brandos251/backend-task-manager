# Backend Task Manager

Backend-приложение на FastAPI для управления пользователями, проектами, задачами и комментариями

## Возможности

- CRUD для пользователей
- CRUD для проектов
- CRUD для задач
- CRUD для комментариев
- Связи User -> Project -> Task -> Comment
- Валидация входных данных через Pydantic
- Обработка HTTP-ошибок и ошибок базы данных
- Миграции схемы базы данных через Alembic
- Контейнеризация FastAPI и PostgreSQL через Docker Compose

## Технологии

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Psycopg
- Uvicorn
- Docker
- Docker Compose

## Структура проекта

```text
backend_task_manager/
├── alembic/
├── routers/
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── compose.yaml
├── database.py
├── Dockerfile
├── main.py
├── models.py
├── requirements.txt
├── schemas.py
└── README.md
```

## Локальный запуск

Установить зависимости:

```bash
pip install -r requirements.txt
```

Создать файл `.env` на основе `.env.example` и указать параметры подключения к PostgreSQL

Применить миграции:

```bash
alembic upgrade head
```

Запустить приложение:

```bash
uvicorn main:app --reload
```

После запуска документация API доступна через Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Запуск через Docker

Перед запуском необходимо создать `.env` на основе `.env.example` и указать параметры базы данных

### 1. Запустить PostgreSQL

```bash
docker compose up -d db
```

PostgreSQL запускается в отдельном контейнере. Данные базы сохраняются в именованном Docker volume

### 2. Применить Alembic-миграции

```bash
docker compose run --rm api alembic upgrade head
```

Alembic запускается во временном контейнере на основе сервиса `api` и применяет миграции к PostgreSQL

### 3. Запустить приложение

```bash
docker compose up --build
```

Docker Compose запустит:

- `api` - FastAPI-приложение
- `db` - PostgreSQL

FastAPI подключается к PostgreSQL внутри Docker-сети по имени сервиса `db`

Для PostgreSQL настроен `healthcheck`, а сервис `api` запускается после перехода `db` в состояние `healthy`

После запуска Swagger UI доступен по адресу:

```text
http://127.0.0.1:8000/docs
```

### 4. Остановить приложение

```bash
docker compose down
```

Команда удаляет контейнеры и сеть Docker Compose, но сохраняет volume с данными PostgreSQL

Для полного удаления контейнеров вместе с volume и данными базы:

```bash
docker compose down -v
```