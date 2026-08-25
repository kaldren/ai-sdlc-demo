# Architecture

## Overview

Task Tracker is a two-tier web app: a React SPA that talks exclusively over REST/JSON to a
FastAPI backend, which is the only component allowed to touch the database (per the project
constitution — see `specs/001-task-management/plan.md`).

```text
Browser ──HTTPS──▶ frontend Container App (nginx)
                        │  (config.js tells the SPA the backend's URL)
                        ▼
Browser ──HTTPS──▶ backend Container App (FastAPI/uvicorn) ──▶ Postgres Flexible Server
```

Both Container Apps sit in one Azure Container Apps Environment and pull their images from
one Azure Container Registry (ACR). Neither app talks to the other server-side; the browser
calls each independently.

## Components

| Component | Tech | Where it runs |
|---|---|---|
| Frontend | React 18 + Vite, built and served by nginx | `tasktracker-frontend` Container App |
| Backend | FastAPI + SQLAlchemy + Alembic, served by uvicorn | `tasktracker-backend` Container App |
| Database | PostgreSQL (Flexible Server, Burstable B1ms) | Azure Database for PostgreSQL |
| Images | Built from `src/backend/Dockerfile` / `src/frontend/Dockerfile` | Azure Container Registry |

## Request flow

1. Browser loads the frontend Container App, which serves the built SPA plus a
   runtime-generated `/config.js` (see below).
2. The SPA's `taskApi.ts` reads `window.__RUNTIME_CONFIG__.API_BASE_URL` from that file and
   makes `fetch` calls directly to the backend Container App's public HTTPS endpoint.
3. FastAPI (`app/api/tasks.py`) handles the request via `app/services/task_service.py` and
   `app/models/task.py`, using SQLAlchemy against Postgres. `CORS_ORIGINS` on the backend is
   set to the frontend's exact origin so only that SPA can call it from a browser.

## Why the frontend URL is injected at container *startup*, not build time

The frontend image is built once and can run against any backend URL — there's no
`VITE_API_BASE_URL` baked in at `npm run build` time. Instead:

- `src/frontend/docker-entrypoint.d/40-runtime-config.sh` runs when the nginx container
  starts, reading the `API_BASE_URL` env var (set by Bicep to the backend Container App's
  FQDN) and writing it into `/usr/share/nginx/html/config.js`.
- `index.html` loads `/config.js` before the app bundle.
- `taskApi.ts` reads `window.__RUNTIME_CONFIG__?.API_BASE_URL`, falling back to the
  build-time `VITE_API_BASE_URL` (used for local dev) and then `http://localhost:8000`.

This means the same built image is portable across environments (dev/staging/prod) without
a rebuild — only the Container App's env var changes.

## Secrets and identity

- **No registry passwords.** Both Container Apps pull from ACR using one shared
  user-assigned managed identity with the `AcrPull` role — ACR's admin user is disabled.
- **No stored Azure credentials in CI.** GitHub Actions authenticates to Azure via OIDC
  federated credentials (`azure/login@v2` with `client-id`/`tenant-id`/`subscription-id`
  secrets, no client secret).
- **Postgres password never touches a concatenated string in IaC.** The admin password
  flows into the backend Container App as its own secret (`PGPASSWORD`), unconcatenated
  with anything else. Host/port/user/database/sslmode are plain env vars, and
  `app/db.py._build_database_url()` assembles the connection string at runtime using
  SQLAlchemy's `URL.create()` (which percent-encodes each part, so special characters in the
  password can't corrupt the URL). This exists because Bicep variables/expressions can't
  carry a parameter's `@secure()` protection once you concatenate into them — see
  `infra/main.bicep` and `docs/deployment.md`.
- **Deployment parameters go through a file, not argv**, in `deploy.yml`, so the Postgres
  password never appears in the runner's process list.

## Infrastructure as code (`infra/`)

`infra/main.bicep` orchestrates modules under `infra/modules/`:

| Module | Provisions |
|---|---|
| `container-registry.bicep` | ACR (Basic, admin disabled) + the shared pull identity + its `AcrPull` role assignment |
| `container-apps-environment.bicep` | Log Analytics workspace + the Container Apps managed environment |
| `postgres.bicep` | Postgres Flexible Server, database, and an "allow Azure services" firewall rule |
| `container-app.bicep` | Generic Container App (used once each for backend and frontend) — ingress, registry pull identity, plain + secret env vars |

**Postgres runs in a different Azure region than everything else.** ACR, the Container Apps
Environment, and both Container Apps are in `eastus`; Postgres is in `centralus` via its own
`postgresLocation` parameter. This isn't a design preference — new Postgres Flexible Server
provisioning turned out to be restricted in `eastus` for the subscription this was deployed
to (confirmed with `az postgres flexible-server list-skus --location eastus`, which returned
an empty supported-version list and an explicit restriction reason). A resource group can
span regions, so only the Postgres module needed to move. If you deploy to a different
subscription, re-check region availability rather than assuming this split is required.

## CI/CD pipeline (`.github/workflows/deploy.yml`)

Three jobs, in order, on every push to `main` (or manual `workflow_dispatch`):

1. **provision-infra** — `az login` via OIDC, ensures the resource group exists, then runs
   `az deployment group create` against `infra/main.bicep`. Before deploying, it looks up
   each Container App's *currently running* image and re-passes it as the Bicep parameter,
   so re-running this job can never silently reset a live app back to the placeholder image
   — including distinguishing "the app doesn't exist yet" from a real Azure CLI failure
   (auth/network/throttling), which must fail the step loudly rather than being treated as
   "no image."
2. **build-and-push** — logs into ACR, builds both Dockerfiles, and pushes each image tagged
   with the commit SHA (and `latest`).
3. **deploy** — `az containerapp update --image ...` for both apps with the SHA tag, which
   creates a new revision that pulls the freshly-pushed image.

Re-running the workflow, including the very first run, is idempotent: infra provisioning
only changes what's different, and images are content-addressed by commit SHA.

## Branch protection

`main` requires the `claude-review` status check (an agentic Claude Code review triggered on
PR open or an `@claude review` comment — see `.github/workflows/claude-pr-review.yml`) to
pass before merging. It does not require a separate human approval.

## Local development

`docker-compose.yml` (repo root) runs all three components locally — postgres, backend,
frontend — via `scripts/dev-up.ps1`. **Always use `127.0.0.1`, never `localhost`, for any
port this stack publishes** (5173, 8000, 5432, 9999) — on this machine, Windows resolves
`localhost` to `::1` first, and on at least one of these ports something other than the
Docker container ends up owning that specific loopback address (observed causes so far:
Docker Desktop's own IPv6 loopback forwarder accepting-but-not-forwarding on `::1`, and once,
a stray `vite --port 5173` dev server run directly on the host outside Docker, whose loopback
listener silently took priority over the container's). Either way the request hangs or hits
the wrong server with no obvious error, so don't assume `localhost` is safe here even when it
looks like it's working — verify with `docker compose ps` / `curl` against `127.0.0.1` instead.
Because of this, backend `CORS_ORIGINS` also lists both `127.0.0.1:5173` and `localhost:5173`,
since the browser's Origin header reflects whichever one was actually typed and CORS checks it
by exact match.

**Monitoring the local stack:**
- `docker compose ps` — per-container healthchecks (postgres, backend `/health`, frontend `/`).
- Dozzle (`http://127.0.0.1:9999` — not `localhost`, see above) — live, searchable log viewer
  across all three containers.
- Backend requests are logged with method/path/status/duration/client/origin for *every*
  request, including ones `CORSMiddleware` rejects or short-circuits — those otherwise
  produce no server-side log line, which made a real origin-mismatch bug invisible from the
  container logs alone.

## Known tradeoffs (see `docs/deployment.md` for detail)

- Postgres's firewall allows all Azure-hosted resources (`AllowAllAzureServicesAndResourcesWithinAzureIps`), not just this app's Container Apps, since tightening that requires VNet integration + a private endpoint. Reasonable follow-up if this moves beyond a demo.
- No pagination, real-time sync, or auth — out of scope per the feature spec (`specs/001-task-management/spec.md`).
