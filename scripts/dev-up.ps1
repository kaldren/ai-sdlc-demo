<#
.SYNOPSIS
    Runs the frontend, backend, and PostgreSQL locally in Docker containers via Docker Desktop.

.DESCRIPTION
    Wraps `docker compose` for the stack defined in docker-compose.yml at the repo root:
      - postgres  -> localhost:5432 (taskuser/taskpass/tasktracker)
      - backend   -> http://localhost:8000 (runs alembic migrations on start)
      - frontend  -> http://localhost:5173

.PARAMETER Down
    Stop and remove the containers instead of starting them.

.PARAMETER Build
    Force a rebuild of the images before starting (default when starting).

.PARAMETER NoBuild
    Skip the image build step when starting.

.EXAMPLE
    ./scripts/dev-up.ps1
    ./scripts/dev-up.ps1 -Down
#>
param(
    [switch]$Down,
    [switch]$NoBuild
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

# `docker info` can print startup warnings (e.g. DOCKER_INSECURE_NO_IPTABLES_RAW) to
# stderr even when it succeeds; under ErrorActionPreference "Stop" those would otherwise
# be promoted to a terminating exception, so check $LASTEXITCODE instead of try/catch.
$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
docker info *> $null
$dockerRunning = ($LASTEXITCODE -eq 0)
$ErrorActionPreference = $prevEap

if (-not $dockerRunning) {
    Write-Error "Docker Desktop doesn't seem to be running. Start Docker Desktop and try again."
    exit 1
}

if ($Down) {
    Write-Host "Stopping containers..."
    docker compose down
    exit $LASTEXITCODE
}

Write-Host "Starting postgres, backend, and frontend containers..."
if ($NoBuild) {
    docker compose up
} else {
    docker compose up --build
}
