# Task Tracker — Backend

FastAPI + SQLAlchemy + PostgreSQL. See `/specs/001-task-management/quickstart.md` for full context.

## Setup

```
py -m venv .venv
.venv/Scripts/pip install -r requirements.txt
cp .env.example .env   # then set DATABASE_URL to a real PostgreSQL instance
```

## Run

```
.venv/Scripts/uvicorn app.main:app --reload
```

Applies migrations first with `.venv/Scripts/alembic upgrade head`.

## Test

```
.venv/Scripts/pytest
```

Tests run against an in-memory SQLite database (see `tests/conftest.py`) — no external database required.
