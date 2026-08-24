# Implementation Plan: Task Management

**Branch**: `001-task-management` | **Date**: 2026-08-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-task-management/spec.md`

## Summary

Deliver full CRUD for a shared, unauthenticated task list: create a task (title + optional description), edit its title/description, archive/unarchive it (soft-hide from the default view without deleting), and permanently delete it. Backend is a FastAPI REST service backed by PostgreSQL with unit-tested business logic; frontend is a React UI that consumes that API exclusively. No real-time sync and no pagination are required for v1 (per clarifications).

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript 5.x + React 18 (frontend)

**Primary Dependencies**: FastAPI, Pydantic v2, SQLAlchemy 2.x (ORM), Alembic (migrations), psycopg (PostgreSQL driver), pytest + httpx (backend unit/API tests); React 18, Vite (dev/build tooling), native `fetch` for API calls

**Storage**: PostgreSQL (sole system of record, per constitution)

**Testing**: pytest with FastAPI's `TestClient`/httpx for backend unit tests, run against a disposable test database (or SQLite-compatible test doubles only where no Postgres-specific SQL is used); frontend covered by manual verification for v1 (no dedicated frontend test framework introduced — see Complexity Tracking / YAGNI)

**Target Platform**: Web — FastAPI service on Linux/container, React SPA served statically, both run locally via `uvicorn` and Vite dev server during development

**Project Type**: Web application (frontend + backend)

**Performance Goals**: Standard interactive web app responsiveness — list/detail requests complete well under 1s for the unpaginated list sizes expected at this stage; no specific throughput target

**Constraints**: REST/JSON only (Principle II); frontend MUST NOT access PostgreSQL directly (Principle IV); no real-time push/polling (per clarification); no pagination in v1 (per clarification); no auth/authorization

**Scale/Scope**: Single shared task list, no multi-tenancy; expected low-to-moderate task volume (hundreds to low thousands) — unpaginated list stays acceptable at this scale; 5 REST endpoints (create, list, get one, edit/archive/unarchive, delete)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Fixed Technology Stack | Uses React (frontend), FastAPI (backend), PostgreSQL (storage) exactly as specified in the Technology Stack table; no additional frontend/backend framework or datastore introduced | PASS |
| II. REST API Contract | All endpoints are resource-oriented (`/api/tasks`, `/api/tasks/{id}`), use standard HTTP methods (GET/POST/PATCH/DELETE) and status codes, and exchange JSON only | PASS |
| III. Backend Test Coverage (NON-NEGOTIABLE) | Every endpoint and the task service's business logic (validation, archive/unarchive no-op behavior, not-found handling) gets unit tests as part of `/speckit-tasks` → `/speckit-implement` | PASS (enforced at task-generation and implementation time) |
| IV. Frontend/Backend Separation | React frontend only calls the FastAPI REST API via `fetch`; no DB client, connection string, or credentials in frontend code | PASS |
| V. Simplicity First (YAGNI) | Single `Task` entity, no repository/service abstraction layers beyond one thin service module; archive/unarchive modeled as a `PATCH` field update rather than dedicated action endpoints; no frontend state-management library, no pagination, no real-time infrastructure | PASS |

No violations — Complexity Tracking table is not needed.

*Re-checked after Phase 1 design: no changes to the above — data model and contracts (below) stayed within the same single-entity, 5-endpoint scope.*

## Project Structure

### Documentation (this feature)

```text
specs/001-task-management/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   └── tasks-api.md
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
src/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app instance, router registration
│   │   ├── db.py              # SQLAlchemy engine/session setup
│   │   ├── models/
│   │   │   └── task.py        # SQLAlchemy Task model + Pydantic schemas
│   │   ├── services/
│   │   │   └── task_service.py # Create/edit/archive/unarchive/delete business logic
│   │   └── api/
│   │       └── tasks.py       # FastAPI router: /api/tasks endpoints
│   ├── alembic/                # DB migrations
│   └── tests/
│       └── unit/
│           ├── test_task_service.py
│           └── test_tasks_api.py
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── TaskForm.tsx, TaskList.tsx, TaskItem.tsx
    │   ├── pages/
    │   │   └── TasksPage.tsx
    │   └── services/
    │       └── taskApi.ts      # fetch wrapper for /api/tasks
    └── tests/                  # left empty for v1 (see Complexity Tracking)
```

**Structure Decision**: Web application split under the existing `src/` directory (per README), as `src/backend` (FastAPI) and `src/frontend` (React) — Option 2 from the plan template, nested under `src/` rather than at repo root, to match this repo's already-documented structure (`docs/`, `src/`, `specs/`).

## Complexity Tracking

*No Constitution Check violations — table intentionally left empty.*
