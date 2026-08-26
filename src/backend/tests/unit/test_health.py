from fastapi.testclient import TestClient

from app.main import app

# --- User Story 1: Automated uptime and load-balancer probing ---


def test_health_returns_200_with_status_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


def test_health_does_not_require_database():
    # Deliberately bypass the `client`/`db_session` fixtures (no DB override configured)
    # to prove GET /health has no database dependency.
    with TestClient(app) as no_db_client:
        response = no_db_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_rejects_unsupported_method(client):
    response = client.post("/health")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}
