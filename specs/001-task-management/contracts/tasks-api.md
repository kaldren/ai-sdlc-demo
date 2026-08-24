# API Contract: Task Management

Base path: `/api/tasks`. All request/response bodies are JSON (Principle II). No authentication.

## Task representation (response body)

```json
{
  "id": 1,
  "title": "Buy milk",
  "description": "2% milk, one gallon",
  "archived": false,
  "created_at": "2026-08-24T12:00:00Z",
  "updated_at": "2026-08-24T12:00:00Z"
}
```

## `POST /api/tasks` — Create a task (User Story 1, FR-001, FR-002)

- **Request body**: `{ "title": string (required, non-blank, max 200 chars), "description": string (optional, max 2000 chars) }`
- **201 Created**: full Task representation
- **422 Unprocessable Entity**: `title` missing/blank, or `title` > 200 chars / `description` > 2000 chars

## `GET /api/tasks?archived={true|false}` — List tasks (User Story 1 & 3, FR-003, FR-006)

- **Query param**: `archived` — `false` (default) returns the active list; `true` returns the archived list
- **200 OK**: `{ "tasks": [Task, ...] }` — full, unpaginated list (per clarification)

## `GET /api/tasks/{id}` — Get a single task

- **200 OK**: Task representation
- **404 Not Found**: no task with that `id` (FR-014)

## `PATCH /api/tasks/{id}` — Edit / archive / unarchive a task (User Story 2 & 3, FR-004, FR-005, FR-007, FR-013)

- **Request body**: any subset of `{ "title": string (max 200 chars), "description": string (max 2000 chars), "archived": boolean }`
- **200 OK**: updated Task representation. `updated_at` advances only if a field actually changed; setting `archived` to its current value is a no-op (FR-013) and does not advance `updated_at`.
- **404 Not Found**: no task with that `id` (FR-014)
- **422 Unprocessable Entity**: `title` present but blank, or `title`/`description` exceeds its max length

## `DELETE /api/tasks/{id}` — Permanently delete a task (User Story 4, FR-008, FR-009)

- **204 No Content**: task removed; irreversible
- **404 Not Found**: no task with that `id` (FR-014) — including a task already deleted
