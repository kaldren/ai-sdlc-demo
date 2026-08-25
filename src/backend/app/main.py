import logging
import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.tasks import router as tasks_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
request_logger = logging.getLogger("app.requests")

app = FastAPI(title="Task Tracker API")

cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registered after CORSMiddleware so it wraps CORSMiddleware in the ASGI stack
# (Starlette runs middleware in reverse registration order) and therefore logs
# every request, including ones CORSMiddleware itself rejects or short-circuits
# (e.g. a preflight from a disallowed origin) — those would otherwise produce
# no server-side log line at all, making origin-mismatch failures invisible.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    client = request.client.host if request.client else "-"
    origin = request.headers.get("origin", "-")
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (time.perf_counter() - start) * 1000
        request_logger.exception(
            "method=%s path=%s status=ERROR duration_ms=%.1f client=%s origin=%s",
            request.method, request.url.path, duration_ms, client, origin,
        )
        raise
    duration_ms = (time.perf_counter() - start) * 1000
    request_logger.info(
        "method=%s path=%s status=%s duration_ms=%.1f client=%s origin=%s",
        request.method, request.url.path, response.status_code, duration_ms, client, origin,
    )
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(tasks_router)
