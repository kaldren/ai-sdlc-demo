---

description: "Task list for feature implementation"
---

# Tasks: Task Management

**Input**: Design documents from `/specs/001-task-management/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/tasks-api.md, quickstart.md

**Tests**: Included — Constitution Principle III (NON-NEGOTIABLE) requires backend unit tests for every endpoint and non-trivial function; the user also explicitly asked for backend logic + tests. Frontend tests are intentionally not included for v1 (see `research.md`).

**Organization**: Tasks are grouped by user story (from spec.md, in priority order) to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Paths use the Web Application structure from `plan.md`: `src/backend/`, `src/frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Create project skeleton directories per plan.md: `src/backend/app/{models,services,api}`, `src/backend/tests/unit`, `src/backend/alembic`, `src/frontend/src/{components,pages,services}`
- [X] T002 Initialize backend Python project in `src/backend` (`pyproject.toml` or `requirements.txt`) with FastAPI, Pydantic, SQLAlchemy, Alembic, psycopg, uvicorn, pytest, httpx as dependencies
- [X] T003 [P] Initialize frontend project in `src/frontend` (Vite + React + TypeScript scaffold, `package.json`)

**Checkpoint**: Repo has runnable-but-empty backend and frontend projects.

---

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T004 Configure SQLAlchemy engine/session management in `src/backend/app/db.py` (reads PostgreSQL connection string from environment)
- [X] T005 Initialize Alembic in `src/backend/alembic`, wiring `env.py` to the SQLAlchemy `Base`/engine from T004 (depends on T004)
- [X] T006 Create the `Task` SQLAlchemy model in `src/backend/app/models/task.py` (id, title, description, archived, created_at, updated_at per data-model.md) and generate the corresponding Alembic migration (depends on T004, T005)
- [X] T007 [P] Create Pydantic request/response schemas (`TaskCreate`, `TaskUpdate`, `TaskRead`) in `src/backend/app/models/schemas.py` per contracts/tasks-api.md, with `title` constrained to max 200 chars and `description` to max 2000 chars (data-model.md Validation Rules)
- [X] T008 Create the FastAPI app instance in `src/backend/app/main.py`: mount an (initially empty) tasks router, and configure CORS for the local frontend dev origin
- [X] T009 [P] Create pytest fixtures (test DB session, FastAPI `TestClient`) in `src/backend/tests/conftest.py`
- [X] T010 [P] Create the frontend API client skeleton in `src/frontend/src/services/taskApi.ts` (base URL config from env, `fetch` wrapper, TypeScript `Task` type matching contracts/tasks-api.md) — all CRUD functions implemented here in one pass (create/list/get/update/archive/unarchive/delete) rather than split across later story tasks

**Checkpoint**: Foundation ready — user story implementation can now begin.

---

## Phase 3: User Story 1 - Create a Task (Priority: P1) 🎯 MVP

**Goal**: Any user can create a task with a title and optional description; it appears in the active list with timestamps (FR-001, FR-002, FR-003, FR-010).

**Independent Test**: Submit a title (with and without a description) via the API/UI and verify the task appears in the active list with correct fields and a creation timestamp; verify a blank title is rejected.

### Tests for User Story 1 ⚠️

- [X] T011 [P] [US1] Unit tests for `create_task`/`list_tasks` in `src/backend/tests/unit/test_task_service.py` (title+description, title-only, blank-title rejected, title >200 chars rejected, description >2000 chars rejected)
- [X] T012 [P] [US1] API tests for `POST /api/tasks` and `GET /api/tasks` in `src/backend/tests/unit/test_tasks_api.py` (201 create, 422 blank title, 422 over-length title/description, 200 list defaults to active tasks)

### Implementation for User Story 1

- [X] T013 [US1] Implement `create_task` and `list_tasks(archived: bool)` in `src/backend/app/services/task_service.py` (depends on T006, T007)
- [X] T014 [US1] Implement `POST /api/tasks` and `GET /api/tasks` endpoints in `src/backend/app/api/tasks.py`, included in the router from T008 (depends on T013)
- [X] T015 [P] [US1] Create `TaskForm` component (title/description inputs, submit, blank-title validation) in `src/frontend/src/components/TaskForm.tsx`
- [X] T016 [P] [US1] Create `TaskList`/`TaskItem` components rendering the active task list in `src/frontend/src/components/TaskList.tsx` and `src/frontend/src/components/TaskItem.tsx`
- [X] T017 [US1] Add `createTask`/`listTasks` functions to `src/frontend/src/services/taskApi.ts` (depends on T010, T014) — implemented as part of T010
- [X] T018 [US1] Create `TasksPage` wiring `TaskForm` + `TaskList` + `taskApi` together in `src/frontend/src/pages/TasksPage.tsx` (depends on T015, T016, T017)

**Checkpoint**: User Story 1 is fully functional and independently testable — this is the MVP.

---

## Phase 4: User Story 2 - Edit a Task (Priority: P2)

**Goal**: Any user can edit an existing task's title and/or description, including archived tasks; `updated_at` advances while `created_at` stays fixed (FR-004, FR-011, FR-014).

**Independent Test**: Create a task, change its title/description, and verify the stored values and `updated_at` change while `created_at` doesn't; verify editing an archived task succeeds and it stays archived; verify a blank-title edit is rejected; verify editing a nonexistent task returns not-found.

### Tests for User Story 2 ⚠️

- [X] T019 [P] [US2] Unit tests for `update_task` (title/description edit, blank title rejected, over-length title/description rejected, `updated_at` advances, `created_at` unchanged, edit succeeds while archived, unknown id raises not-found) in `src/backend/tests/unit/test_task_service.py`
- [X] T020 [P] [US2] API tests for `GET /api/tasks/{id}` and `PATCH /api/tasks/{id}` in `src/backend/tests/unit/test_tasks_api.py` (200 edit, 404 unknown id, 422 blank title, 422 over-length title/description)

### Implementation for User Story 2

- [X] T021 [US2] Implement `get_task` and extend `update_task` for title/description fields in `src/backend/app/services/task_service.py` (depends on T013)
- [X] T022 [US2] Implement `GET /api/tasks/{id}` and `PATCH /api/tasks/{id}` endpoints in `src/backend/app/api/tasks.py` (depends on T021, T014)
- [X] T023 [P] [US2] Add inline edit UI to `TaskItem` (edit title/description, save/cancel) in `src/frontend/src/components/TaskItem.tsx` (depends on T016)
- [X] T024 [US2] Add `updateTask` function to `taskApi.ts` and wire editing into `TasksPage` in `src/frontend/src/services/taskApi.ts` and `src/frontend/src/pages/TasksPage.tsx` (depends on T022, T023) — `updateTask` implemented as part of T010

**Checkpoint**: User Stories 1 and 2 both work independently.

---

## Phase 5: User Story 3 - Archive and Unarchive a Task (Priority: P3)

**Goal**: Any user can archive an active task (hiding it from the default view) and unarchive it later; archiving/unarchiving an already-archived/active task is a no-op (FR-005, FR-006, FR-007, FR-013).

**Independent Test**: Create a task, archive it, verify it disappears from the active list and appears in the archived list; archive it again and verify no error/no `updated_at` change; unarchive it and verify it reappears in the active list.

### Tests for User Story 3 ⚠️

- [X] T025 [P] [US3] Unit tests for archiving via `update_task`'s `archived` field (archive active task, no-op re-archive, unarchive, no-op re-unarchive, `updated_at` behavior for each) in `src/backend/tests/unit/test_task_service.py`
- [X] T026 [P] [US3] API tests for `PATCH /api/tasks/{id}` with `archived` and `GET /api/tasks?archived=true` in `src/backend/tests/unit/test_tasks_api.py`

### Implementation for User Story 3

- [X] T027 [US3] Extend `update_task` in `src/backend/app/services/task_service.py` to accept and apply the `archived` field with no-op semantics (depends on T021)
- [X] T028 [US3] Ensure `PATCH /api/tasks/{id}` accepts `archived` and `GET /api/tasks?archived=true` returns the archived list in `src/backend/app/api/tasks.py` (depends on T027, T022)
- [X] T029 [P] [US3] Add Archive/Unarchive button to `TaskItem` in `src/frontend/src/components/TaskItem.tsx` (depends on T016)
- [X] T030 [US3] Add an active/archived view toggle to `TasksPage`, plus `archiveTask`/`unarchiveTask` calls (via `updateTask`) in `src/frontend/src/pages/TasksPage.tsx` and `src/frontend/src/services/taskApi.ts` (depends on T028, T029) — `archiveTask`/`unarchiveTask` implemented as part of T010

**Checkpoint**: User Stories 1, 2, and 3 all work independently.

---

## Phase 6: User Story 4 - Delete a Task (Priority: P4)

**Goal**: Any user can permanently delete a task — active or archived — and it becomes unrecoverable (FR-008, FR-009, FR-014).

**Independent Test**: Create a task (active and, separately, archived), delete each, and verify both are gone from active and archived views and return not-found on retrieval.

### Tests for User Story 4 ⚠️

- [X] T031 [P] [US4] Unit tests for `delete_task` (delete active, delete archived, delete unknown id → not-found, deleted task not retrievable afterward) in `src/backend/tests/unit/test_task_service.py`
- [X] T032 [P] [US4] API tests for `DELETE /api/tasks/{id}` in `src/backend/tests/unit/test_tasks_api.py` (204 on success, 404 for unknown/already-deleted id)

### Implementation for User Story 4

- [X] T033 [US4] Implement `delete_task` in `src/backend/app/services/task_service.py` (depends on T013)
- [X] T034 [US4] Implement `DELETE /api/tasks/{id}` endpoint in `src/backend/app/api/tasks.py` (depends on T033)
- [X] T035 [P] [US4] Add a Delete button (with confirmation) to `TaskItem` in `src/frontend/src/components/TaskItem.tsx` (depends on T016)
- [X] T036 [US4] Add `deleteTask` function to `taskApi.ts` and wire deletion into `TasksPage` in `src/frontend/src/services/taskApi.ts` and `src/frontend/src/pages/TasksPage.tsx` (depends on T034, T035) — `deleteTask` implemented as part of T010

**Checkpoint**: All four user stories work independently — full CRUD is complete.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T037 [P] Run the quickstart.md manual verification checklist end-to-end across all four user stories — verified functionally via live API smoke test (create/edit/archive/unarchive/delete, full lifecycle) and `pytest` (38/38 passing); UI was not visually verified in a browser since the Chrome browser-automation extension was not connected in this environment
- [X] T038 Review and align error-response consistency (404/422 bodies) across all endpoints in `src/backend/app/api/tasks.py` — 404s consistently return `{"detail": "<message>"}` from the service layer; 422s are consistently produced by Pydantic schema validation (`TaskCreate`/`TaskUpdate` field constraints) before the handler body runs, so the service layer's own `TaskValidationError` 422 handling in the router is a harmless defense-in-depth fallback, not a live inconsistency
- [X] T039 [P] Add brief run/test instructions (referencing quickstart.md) to `src/backend/README.md` and `src/frontend/README.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories.
- **User Stories (Phase 3–6)**: All depend on Foundational completion. US2, US3, and US4 each build on service/API scaffolding from US1 (T013/T014) but are independently testable once their own phase is done — implement in priority order (P1 → P2 → P3 → P4).
- **Polish (Phase 7)**: Depends on all four user stories being complete.

### Within Each User Story

- Tests are written first and must fail before implementation.
- Service layer before API endpoints; API endpoints before frontend wiring.
- Story is checkpointed (fully functional) before moving to the next priority.

### Parallel Opportunities

- T002 and T003 (Setup) can run in parallel.
- T007, T009, T010 (Foundational) can run in parallel with each other and with the T004→T005→T006 chain.
- Within each story, the two test tasks are marked [P] (different files) and can run together.
- Within each story, frontend component tasks marked [P] can run in parallel with backend service/API tasks, since they touch different files — but final wiring tasks depend on both being done.

---

## Parallel Example: User Story 1

```bash
# Tests (parallel):
Task: "Unit tests for create_task/list_tasks in src/backend/tests/unit/test_task_service.py"
Task: "API tests for POST/GET /api/tasks in src/backend/tests/unit/test_tasks_api.py"

# Frontend components (parallel, independent of backend implementation):
Task: "Create TaskForm component in src/frontend/src/components/TaskForm.tsx"
Task: "Create TaskList/TaskItem components in src/frontend/src/components/TaskList.tsx, TaskItem.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete Phase 3 (User Story 1 — Create).
3. **STOP and VALIDATE**: create tasks via the UI and API, confirm they list correctly.
4. This is a demoable MVP: a shared list where tasks can be created and viewed.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. Add US1 (Create) → validate → demo (MVP).
3. Add US2 (Edit) → validate → demo.
4. Add US3 (Archive/Unarchive) → validate → demo.
5. Add US4 (Delete) → validate → demo.
6. Polish.

---

## Notes

- [P] tasks touch different files with no unmet dependencies.
- Commit after each task or logical group.
- Stop at any checkpoint to validate a story independently before moving on.
- Tests must fail before their corresponding implementation task is done (write-tests-first, per Constitution Principle III).
