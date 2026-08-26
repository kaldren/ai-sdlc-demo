# Phase 0 Research: Backend Health-Check Endpoint

## Context

The spec's Technical Context left no `NEEDS CLARIFICATION` markers to resolve (see spec.md
Assumptions: response format and exact path naming were deferred to planning). This research
resolves that one open point and documents the discovery that shaped the plan.

## Finding: An endpoint already exists

**Decision**: Treat `GET /health` (already present in `src/backend/app/main.py`, added in
commit `bf02783` "Add local Docker Compose stack with monitoring, fix task-create bug") as the
health-check endpoint this feature specifies, rather than adding a second, competing endpoint.

**Rationale**:
- The existing handler already matches the spec's own example verbatim:
  ```python
  @app.get("/health")
  def health() -> dict[str, str]:
      return {"status": "ok"}
  ```
- It already satisfies FR-001 (no auth), FR-002 (immediate success), FR-003 (no dependency
  check — the handler is a pure literal return, no DB/service calls), FR-004 (no sensitive
  data in the response), and FR-006 (no I/O or computation, trivially lightweight).
- Introducing a second, differently-named endpoint (e.g. `/api/health` or `/healthz`) would
  violate Principle V (Simplicity First / YAGNI) by duplicating working functionality and
  would fragment monitoring configuration that might already reference `/health` (e.g. the
  Docker Compose stack it was added alongside).

**Alternatives considered**:
- *Add a new `/api/health` endpoint under the `app/api/` router package, matching the
  `/api/tasks` convention.* Rejected: the spec has no requirement that this endpoint follow
  the `/api/*` resource-namespacing used for business-domain resources: health/liveness
  probes conventionally live at a top-level, unversioned, unnamespaced path (`/health`,
  `/healthz`, `/livez`) precisely so load balancer and orchestrator configuration doesn't need
  to track API versioning. Moving it would also require updating any existing infra config
  that already points at `/health`, for no behavioral benefit.
- *Add a `/ready` or dependency-aware readiness endpoint alongside it.* Rejected: explicitly
  out of scope per spec Assumptions ("Deeper 'readiness' checks... are out of scope for this
  feature").

## Finding: FastAPI's default 405 response is safe to rely on

**Decision**: Rely on FastAPI/Starlette's built-in automatic `405 Method Not Allowed` response
for unsupported methods on `/health` (e.g. `POST`, `DELETE`) rather than adding custom
exception handling.

**Rationale**: FastAPI's default behavior for a route registered only with `@app.get(...)` is
to return HTTP 405 with a JSON body of `{"detail": "Method Not Allowed"}` for any other verb.
This satisfies FR-005 ("reject requests using unsupported HTTP methods with a standard error
response") without any additional code, and the body contains only a generic, non-sensitive
string — consistent with FR-004. No custom `exception_handler` or method-routing logic is
needed (Principle V).

**Alternatives considered**:
- *Custom 405 handler with a bespoke JSON shape.* Rejected: adds code and a bespoke response
  contract for no requirement gain; the spec only asks for "a standard error response."

## Finding: No new dependency or test tooling needed

**Decision**: Use the existing `pytest` + FastAPI `TestClient` stack and the existing shared
`client` fixture (`src/backend/tests/conftest.py`), the same pattern already used by
`test_tasks_api.py`.

**Rationale**: Consistent with Principle I (Fixed Technology Stack) and Principle V
(Simplicity First) — no new test framework or fixture scaffolding is justified for one
endpoint.

**Alternatives considered**: None seriously considered; this is a direct application of
existing, working conventions.

## Summary of resolved unknowns

| Unknown | Resolution |
|---|---|
| Exact endpoint path | `GET /health` (already implemented; reused as-is) |
| Response body shape | `{"status": "ok"}` (already implemented; matches spec's own example) |
| Method-not-allowed handling | FastAPI's default automatic 405 JSON response (no custom code) |
| Test approach | pytest + existing `TestClient`/`client` fixture, new file `tests/unit/test_health.py` |

No `NEEDS CLARIFICATION` items remain.
