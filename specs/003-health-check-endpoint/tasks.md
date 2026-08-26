---

description: "Task list for Backend Health-Check Endpoint"
---

# Tasks: Backend Health-Check Endpoint

**Input**: Design documents from `/specs/003-health-check-endpoint/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, contracts/health-api.md, quickstart.md
(`data-model.md` is explicitly N/A — this feature introduces no entities)

**Tests**: Tests are the primary deliverable of this feature. `GET /health` already exists in
`src/backend/app/main.py` and already satisfies FR-001–FR-006, but it has **zero** test
coverage — a direct violation of Constitution Principle III (Backend Test Coverage,
NON-NEGOTIABLE). No new endpoint is being built; the work below is entirely test-first
verification that locks in the existing, correct behavior.

**Organization**: This feature has a single user story (P1), so all substantive work lives in
Phase 3.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

Backend-only change under the existing `src/backend` layout (Web application structure from
`001-task-management`):
- Production code (no changes anticipated): `src/backend/app/main.py`
- Tests (all new work): `src/backend/tests/unit/test_health.py`
- Shared test fixtures (reused, not modified): `src/backend/tests/conftest.py`

---

## Phase 1: Setup

**Not applicable.** No new project, dependency, or scaffolding is needed. The FastAPI app,
pytest/`TestClient` stack, and `client` fixture (`src/backend/tests/conftest.py`) already exist
and are reused as-is (see plan.md Technical Context and Project Structure).

---

## Phase 2: Foundational

**Not applicable.** There is no shared infrastructure to build before the single user story
can proceed — the endpoint under test already exists in `src/backend/app/main.py` and requires
no code changes. Work can start directly at Phase 3.

---

## Phase 3: User Story 1 - Automated uptime and load-balancer probing (Priority: P1) 🎯 MVP

**Goal**: Close the Constitution Principle III test-coverage gap on the existing `GET /health`
endpoint by adding unit tests that lock in its documented contract (contracts/health-api.md):
a 200 success response with the exact `{"status": "ok"}` body, independence from the database,
and a standard 405 rejection of unsupported methods that leaks no internal details.

**Independent Test**: Run `pytest tests/unit/test_health.py -v` from `src/backend`; all tests
pass, confirming the behavior a load balancer / uptime monitor depends on (spec.md Acceptance
Scenarios 1–3 and Edge Cases) without needing any other feature or fixture beyond what already
exists.

### Tests for User Story 1 ⚠️

> **NOTE**: These tests exercise the existing `GET /health` handler in
> `src/backend/app/main.py`. No production code change is expected; if a test fails, fix the
> test's expectations against contracts/health-api.md first, and only change `main.py` if the
> contract itself is confirmed wrong.

- [X] T001 [US1] In `src/backend/tests/unit/test_health.py`, write `test_health_returns_200_with_status_ok` using the existing `client` fixture (`src/backend/tests/conftest.py`): `GET /health` returns status code 200, `Content-Type: application/json`, and a JSON body that is exactly `{"status": "ok"}` with no extra keys (FR-002, FR-004, contracts/health-api.md Success Response).
- [X] T002 [US1] In `src/backend/tests/unit/test_health.py`, write `test_health_does_not_require_database` using a plain `fastapi.testclient.TestClient(app)` from `app.main` (deliberately bypassing the `client`/`db_session` fixtures and their DB override) to prove `GET /health` returns 200 with no database dependency configured or reachable (FR-003, SC-002, contracts/health-api.md Guarantees — "No dependency checks"). Depends on T001 (same file).
- [X] T003 [US1] In `src/backend/tests/unit/test_health.py`, write `test_health_rejects_unsupported_method` using the `client` fixture: `POST /health` returns status code 405 with a JSON body exactly `{"detail": "Method Not Allowed"}`, confirming FastAPI's default 405 body leaks no sensitive/internal details (FR-004, FR-005, contracts/health-api.md Unsupported Method Response). Depends on T002 (same file).
- [X] T004 [US1] Run `pytest tests/unit/test_health.py -v` from `src/backend` and confirm all three tests pass without any modification to `src/backend/app/main.py`, closing the Constitution Principle III gap identified in plan.md. Depends on T001–T003.

**Checkpoint**: `GET /health` now has full unit test coverage of its success path, its
DB-independence guarantee, and its unsupported-method rejection — the feature is complete and
independently verifiable.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Confirm the documented contract matches observed runtime behavior and that no
regressions were introduced elsewhere in the backend test suite.

- [X] T005 [P] Follow `specs/003-health-check-endpoint/quickstart.md`: start the backend locally and run `curl -i http://localhost:8000/health` (expect `200` / `{"status":"ok"}`) and `curl -i -X POST http://localhost:8000/health` (expect `405` / `{"detail":"Method Not Allowed"}`) to manually confirm the contract.
- [X] T006 Run the full backend suite (`pytest` from `src/backend`) to confirm the new `tests/unit/test_health.py` introduces no regressions alongside `test_tasks_api.py` and `test_task_service.py`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: N/A — nothing to build.
- **Foundational (Phase 2)**: N/A — nothing blocks User Story 1.
- **User Story 1 (Phase 3)**: Can start immediately. All tasks (T001–T004) touch the same new
  file (`test_health.py`), so within the story they are sequential rather than parallel.
- **Polish (Phase 4)**: Depends on Phase 3 completion (T001–T004).

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories (there are no other stories in this
  feature).

### Within User Story 1

- T001 → T002 → T003 (all edit `src/backend/tests/unit/test_health.py`; sequential to avoid
  edit conflicts even though the test cases themselves are logically independent).
- T004 depends on T001–T003 (runs the tests just written).

### Parallel Opportunities

- None within Phase 3 (single target file, see above).
- T005 and T006 in Phase 4 are independent of each other and can run in parallel — T005 is a
  manual curl-based check against a running server, T006 is the automated pytest suite — but
  both depend on Phase 3 being complete.

---

## Parallel Example: Polish Phase

```bash
# After Phase 3 (T001-T004) is complete, these two can run at the same time:
Task: "Manually verify GET/POST /health against a locally running backend per quickstart.md"
Task: "Run full backend pytest suite from src/backend to confirm no regressions"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Skip Phase 1 and Phase 2 (not applicable — no setup or foundational work exists).
2. Complete Phase 3: write and pass `test_health.py` (T001–T004).
3. **STOP and VALIDATE**: `pytest tests/unit/test_health.py -v` is green and `main.py` is
   untouched.
4. This closes the feature — User Story 1 is the entire scope (spec.md: "This is the entire
   scope of the feature").

### Incremental Delivery

Not applicable beyond the MVP — there is only one user story, and Phase 4 is a lightweight
confirmation pass, not a separate increment.

---

## Notes

- [P] tasks = different files, no dependencies. This feature has almost none, since all new
  test code lands in a single file.
- Verify each test fails for the *right reason* before it's written correctly, then passes once
  correct — even though `main.py` is not expected to change, writing the assertions against the
  actual running app (not just the contract doc) is what proves the contract.
- Do not modify `src/backend/app/main.py` unless a test reveals the existing handler actually
  violates a functional requirement (none are expected per plan.md's analysis).
- Commit after Phase 3 is green; Phase 4 is confirmation, not new functional work.
