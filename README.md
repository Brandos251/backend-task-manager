# Backend Task Manager

Backend-приложение на FastAPI для управления пользователями, проектами, задачами и комментариями

## Возможности

- CRUD для пользователей
- CRUD для проектов
- CRUD для задач
- CRUD для комментариев
- Связи User -> Project -> Task -> Comment
- Валидация входных данных через Pydantic
- Обработка ошибок HTTP и ошибок базы данных
- Миграции схемы базы данных через Alembic

## Технологии

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Psycopg
- Uvicorn

## Структура проекта

```text
backend_task_manager/
├── alembic/
├── routers/
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
├── alembic.ini
└── .gitignore
```

## Запуск

Установить зависимости:

```bash
pip install -r requirements.txt
```

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