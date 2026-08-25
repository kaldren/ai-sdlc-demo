# Deployment: Azure Container Apps

`.github/workflows/deploy.yml` deploys this app to Azure Container Apps on every push to
`main` (or manually via `workflow_dispatch`). It provisions infrastructure from
`infra/main.bicep`, builds/pushes both container images to Azure Container Registry, then
updates the two Container Apps to the new images.

## Architecture

- **Backend**: FastAPI app (`src/backend`), containerized, runs `alembic upgrade head` on
  startup, exposed on port 8000.
- **Frontend**: React/Vite SPA (`src/frontend`), built and served by nginx on port 80. The
  backend's URL is injected at container *startup* (not build time) via
  `docker-entrypoint.d/40-runtime-config.sh`, which writes `/config.js` from the
  `API_BASE_URL` env var — so the same image works in any environment without rebuilding.
- **Database**: Azure Database for PostgreSQL Flexible Server (Burstable B1ms).
- Both apps run in one Container Apps Environment, pull images from one Azure Container
  Registry using a shared user-assigned managed identity (no registry passwords), and the
  Postgres connection string is stored as a Container Apps secret, never in plain env vars.

## One-time setup (do this once, before the first push)

These steps require `Owner` (or `Contributor` + `User Access Administrator`) on the target
subscription, since the pipeline's identity needs to create role assignments (for ACR pull).

### 1. Create the resource group (or let the pipeline create it)

The workflow runs `az group create` itself, so this is optional:

```bash
az group create --name rg-tasktracker --location eastus
```

If you use a different name/location, update the `AZURE_RESOURCE_GROUP` / `AZURE_LOCATION`
values at the top of `.github/workflows/deploy.yml`.

### 2. Create an app registration with federated credentials (OIDC — no stored secrets)

```bash
az ad app create --display-name "tasktracker-github-deploy" \
  --query appId -o tsv
# save this as APP_ID

az ad sp create --id "$APP_ID"

az ad app federated-credential create --id "$APP_ID" --parameters '{
  "name": "github-main-branch",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:<GITHUB_ORG>/<GITHUB_REPO>:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'
```

Add a second federated credential if you also want manual `workflow_dispatch` runs from
other branches, or one scoped to `pull_request` if you later gate on PR environments.

### 3. Grant the app registration access to the subscription

```bash
az role assignment create \
  --assignee "$APP_ID" \
  --role "Owner" \
  --scope "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/rg-tasktracker"
```

`Owner` (scoped to just this resource group) is simplest since the Bicep template creates
role assignments (ACR pull) as part of provisioning. If you'd rather avoid `Owner`, use
`Contributor` + `User Access Administrator` instead.

### 4. Add GitHub repository secrets

Under **Settings → Secrets and variables → Actions**, add:

| Secret | Value |
|---|---|
| `AZURE_CLIENT_ID` | the app registration's `appId` |
| `AZURE_TENANT_ID` | `az account show --query tenantId -o tsv` |
| `AZURE_SUBSCRIPTION_ID` | `az account show --query id -o tsv` |
| `POSTGRES_ADMIN_PASSWORD` | a strong password for the Postgres admin login |

No client secret is needed — OIDC federation replaces it.

## How the pipeline works

1. **provision-infra** — logs in via OIDC, ensures the resource group exists, then runs
   `az deployment group create` against `infra/main.bicep`. To avoid resetting a live
   deployment back to its placeholder image, it first looks up the currently-running
   backend/frontend image (if any) and passes it back in as the image parameter.
2. **build-and-push** — logs into the newly-provisioned ACR and builds/pushes both images,
   tagged with the commit SHA (and `latest`).
3. **deploy** — runs `az containerapp update --image ...` for both apps with the SHA tag,
   which creates a new revision that pulls the freshly-pushed image.

Re-running the workflow (including the very first run) is safe: infrastructure provisioning
is idempotent, and images are always content-addressed by commit SHA.

## Customizing

Names, region, and app naming all live as `env:` values at the top of
`.github/workflows/deploy.yml` and as parameters in `infra/main.bicep` — no other files need
to change to point this at a different subscription, region, or app name.
