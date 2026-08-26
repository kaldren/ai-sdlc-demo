# Quickstart: Backend Health-Check Endpoint

## Try it locally

1. From `src/backend`, install dependencies and start the API (see repo README / existing
   `001-task-management` docs for full local setup, e.g. via the Docker Compose stack or a
   local virtualenv + `uvicorn`).
2. With the backend running (default `http://localhost:8000`), request the health check:

   ```bash
   curl -i http://localhost:8000/health
   ```

   Expected response:

   ```http
   HTTP/1.1 200 OK
   content-type: application/json

   {"status":"ok"}
   ```

3. Confirm unsupported methods are rejected:

   ```bash
   curl -i -X POST http://localhost:8000/health
   ```

   Expected response: `405 Method Not Allowed` with a JSON `{"detail": "Method Not Allowed"}`
   body.

## Run the tests

From `src/backend`:

```bash
pytest tests/unit/test_health.py -v
```

This exercises:
- `GET /health` returns `200` with `{"status": "ok"}`.
- The response contains no fields beyond the documented contract (no leaked internals).
- A disallowed method (e.g. `POST /health`) returns `405`.

## Notes for load balancers / uptime monitors

- No authentication header or credentials are required or accepted.
- The endpoint reflects process liveness only — it will return `200` even if the database is
  unreachable. Do not use it to infer full application readiness; a separate, distinctly
  named readiness check would be needed for that (out of scope for this feature).
