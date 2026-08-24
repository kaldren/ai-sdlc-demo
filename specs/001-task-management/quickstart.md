# Quickstart: Task Management

## Backend (`src/backend`)

1. Create/activate a Python 3.12 virtualenv.
2. Install dependencies (FastAPI, SQLAlchemy, Alembic, psycopg, pytest, httpx).
3. Point the app at a PostgreSQL instance (local Docker container or existing dev DB) via a connection string / env var.
4. Run Alembic migrations to create the `tasks` table.
5. Start the API: `uvicorn app.main:app --reload` (from `src/backend`).
6. Run tests: `pytest` (from `src/backend`) — covers `task_service` unit tests and `tasks` API tests.

## Frontend (`src/frontend`)

1. Install dependencies (`npm install`).
2. Configure the API base URL (e.g., `http://localhost:8000`) via an env var consumed by `src/frontend/src/services/taskApi.ts`.
3. Start the dev server: `npm run dev` (Vite).
4. Manually verify the golden path in a browser: create a task, edit it, archive it, view the archived list, unarchive it, delete it.

## Manual verification checklist (maps to spec Acceptance Scenarios)

- Create a task with title only, and with title + description — both appear in the active list with timestamps.
- Attempt to create/edit with a blank title — rejected, no task created/changed.
- Edit an active task's title/description — `updated_at` advances, `created_at` unchanged.
- Archive an active task — disappears from active list, appears in archived list.
- Archive an already-archived task — no-op, no error.
- Unarchive an archived task — reappears in active list.
- Edit an archived task — succeeds, task remains archived.
- Delete an active task and an archived task — both permanently gone from both views; re-fetching by id returns 404.
