# API Contract: Health Check

## `GET /health`

Reports basic process liveness of the FastAPI backend. Unauthenticated. Does not check any
downstream dependency (database, third-party services).

### Request

- Method: `GET`
- Path: `/health`
- Auth: none required
- Body: none
- Query params: none

### Success Response

- Status: `200 OK`
- Content-Type: `application/json`
- Body:
  ```json
  {
    "status": "ok"
  }
  ```

### Unsupported Method Response

- Any method other than `GET` (e.g. `POST`, `PUT`, `PATCH`, `DELETE`) on `/health`:
- Status: `405 Method Not Allowed`
- Content-Type: `application/json`
- Body (FastAPI/Starlette default):
  ```json
  {
    "detail": "Method Not Allowed"
  }
  ```

### Guarantees

- **No sensitive data**: the response body never includes configuration values, credentials,
  stack traces, or other internal implementation details (FR-004).
- **No dependency checks**: the handler performs no database query, network call, or other
  blocking I/O; a degraded or unreachable database does not affect this endpoint's response
  (FR-003, SC-002).
- **Performance**: the handler does no computation beyond returning a literal dict, so it
  responds well under the 200ms target (SC-001) and adds no measurable load under repeated
  calls (SC-003).

### Non-goals (explicitly out of scope)

- Readiness/dependency-health reporting (e.g. database connectivity) — a distinctly-named
  future endpoint (e.g. `/ready`) would be introduced separately if needed.
- Authentication or rate limiting.
- Historical logging, metrics export, or alerting integration beyond what the existing
  request-logging middleware in `main.py` already provides for all routes.

### Implementation reference

Already implemented in `src/backend/app/main.py`:

```python
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

No change to this handler is anticipated; this contract documents its existing, correct
behavior so it can be locked in with tests.
