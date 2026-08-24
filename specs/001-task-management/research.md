# Phase 0 Research: Task Management

No `NEEDS CLARIFICATION` markers remain in the Technical Context (the stack is fixed by the constitution, and behavioral ambiguities were resolved in `/speckit-clarify`). This document records the smaller implementation-pattern decisions needed before design.

## Decision: ORM — SQLAlchemy 2.x

- **Rationale**: Standard, well-supported ORM for FastAPI + PostgreSQL; async-capable if needed later; the constitution names PostgreSQL as the datastore but leaves the access library open as a "supporting library" (Principle I).
- **Alternatives considered**: Raw SQL via psycopg (more boilerplate for a CRUD-shaped feature; rejected for this feature's simplicity needs); Tortoise ORM/Django ORM (less common in FastAPI ecosystem, no added benefit here).

## Decision: Migrations — Alembic

- **Rationale**: Standard companion to SQLAlchemy; a single `tasks` table needs one migration, keeping schema changes reviewable and repeatable.
- **Alternatives considered**: Hand-written SQL migration scripts (works, but Alembic's autogeneration reduces error risk for a one-table schema); no migrations at all / `create_all()` on startup (rejected — not repeatable/reviewable, poor fit even for a small schema).

## Decision: Archive/unarchive modeled as a `PATCH` field update, not dedicated endpoints

- **Rationale**: `archived` is just another mutable field on the `Task` resource (alongside `title`/`description`); a single `PATCH /api/tasks/{id}` accepting any subset of `{title, description, archived}` satisfies FR-004 through FR-007 and FR-013 (idempotent no-op) without adding two extra routes. Matches Principle V (Simplicity First) and Principle II (resource-oriented REST).
- **Alternatives considered**: Dedicated `POST /api/tasks/{id}/archive` and `/unarchive` action endpoints (more explicit intent in the URL, but doubles the route count for behavior a single `PATCH` already covers cleanly; rejected as unnecessary for this scope).

## Decision: Backend test approach — pytest + FastAPI `TestClient` (httpx) against a real/disposable PostgreSQL test database

- **Rationale**: Constitution Principle III requires unit tests that exercise business logic directly, not just end-to-end. Splitting tests into (a) `task_service` unit tests calling the service functions directly with a test DB session, and (b) `tasks` API tests via `TestClient` for request/response/status-code contracts, satisfies both "fast, localized" and "endpoint contract" coverage.
- **Alternatives considered**: SQLite in-memory for tests (faster, but risks masking PostgreSQL-specific behavior; acceptable only if no Postgres-specific SQL/types are used — since this schema is simple (text/bool/timestamp columns), SQLite is an acceptable *fallback* if a local test Postgres isn't available, but a disposable Postgres instance is preferred for parity).

## Decision: Frontend data fetching — native `fetch`, component-local state, no state-management library

- **Rationale**: A single-resource CRUD UI (one list, one form) doesn't need Redux/Zustand/React Query; `fetch` + component state keeps the frontend simple (Principle V) while still going exclusively through the REST API (Principle IV).
- **Alternatives considered**: React Query/SWR (nice caching/refetch ergonomics, but an added dependency not justified by this feature's scope — refresh-based sync was explicitly chosen over real-time, so there's no cache-invalidation complexity to manage yet); Redux/Zustand (no cross-page shared state exists to justify a global store).

## Decision: No dedicated frontend test framework introduced for v1

- **Rationale**: The constitution's NON-NEGOTIABLE testing requirement (Principle III) applies to backend behavior. Introducing a frontend test framework (Vitest/RTL) is reasonable long-term but not required to satisfy this feature's explicit requirements; adding it now without a concrete current need would conflict with Principle V. Flagged here so the decision is visible, not silently skipped.
- **Alternatives considered**: Add Vitest + React Testing Library now (deferred — can be introduced in a future feature once frontend logic grows beyond simple form/list rendering).
