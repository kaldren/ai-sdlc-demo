# --- User Story 1: Create a Task ---


def test_post_task_creates_and_returns_201(client):
    response = client.post(
        "/api/tasks", json={"title": "Buy milk", "description": "2% milk"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["description"] == "2% milk"
    assert body["archived"] is False
    assert "created_at" in body and "updated_at" in body


def test_post_task_blank_title_returns_422(client):
    response = client.post("/api/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_post_task_overlong_title_returns_422(client):
    response = client.post("/api/tasks", json={"title": "x" * 201})
    assert response.status_code == 422


def test_post_task_overlong_description_returns_422(client):
    response = client.post(
        "/api/tasks", json={"title": "Title", "description": "y" * 2001}
    )
    assert response.status_code == 422


def test_get_tasks_defaults_to_active_list(client):
    client.post("/api/tasks", json={"title": "Active"})
    archived_resp = client.post("/api/tasks", json={"title": "Archived"})
    archived_id = archived_resp.json()["id"]
    client.patch(f"/api/tasks/{archived_id}", json={"archived": True})

    response = client.get("/api/tasks")

    assert response.status_code == 200
    titles = [t["title"] for t in response.json()["tasks"]]
    assert titles == ["Active"]


# --- User Story 2: Edit a Task ---


def test_get_task_by_id(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()

    response = client.get(f"/api/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_task_unknown_id_returns_404(client):
    response = client.get("/api/tasks/999")
    assert response.status_code == 404


def test_patch_task_edits_title_and_description(client):
    created = client.post("/api/tasks", json={"title": "Old"}).json()

    response = client.patch(
        f"/api/tasks/{created['id']}",
        json={"title": "New", "description": "New description"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New"
    assert body["description"] == "New description"
    assert body["updated_at"] >= created["updated_at"]


def test_patch_task_unknown_id_returns_404(client):
    response = client.patch("/api/tasks/999", json={"title": "Anything"})
    assert response.status_code == 404


def test_patch_task_blank_title_returns_422(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()

    response = client.patch(f"/api/tasks/{created['id']}", json={"title": "   "})

    assert response.status_code == 422


def test_patch_task_overlong_title_returns_422(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()

    response = client.patch(f"/api/tasks/{created['id']}", json={"title": "x" * 201})

    assert response.status_code == 422


def test_patch_task_overlong_description_returns_422(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()

    response = client.patch(
        f"/api/tasks/{created['id']}", json={"description": "y" * 2001}
    )

    assert response.status_code == 422


# --- User Story 3: Archive and Unarchive a Task ---


def test_patch_task_archives_and_appears_in_archived_list(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()

    patch_response = client.patch(
        f"/api/tasks/{created['id']}", json={"archived": True}
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["archived"] is True

    archived_list = client.get("/api/tasks?archived=true").json()["tasks"]
    assert any(t["id"] == created["id"] for t in archived_list)

    active_list = client.get("/api/tasks?archived=false").json()["tasks"]
    assert all(t["id"] != created["id"] for t in active_list)


def test_patch_task_unarchive_restores_to_active_list(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()
    client.patch(f"/api/tasks/{created['id']}", json={"archived": True})

    response = client.patch(f"/api/tasks/{created['id']}", json={"archived": False})

    assert response.status_code == 200
    assert response.json()["archived"] is False
    active_list = client.get("/api/tasks?archived=false").json()["tasks"]
    assert any(t["id"] == created["id"] for t in active_list)


# --- User Story 4: Delete a Task ---


def test_delete_active_task_returns_204(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()

    response = client.delete(f"/api/tasks/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404


def test_delete_archived_task_returns_204(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()
    client.patch(f"/api/tasks/{created['id']}", json={"archived": True})

    response = client.delete(f"/api/tasks/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404


def test_delete_unknown_id_returns_404(client):
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404


def test_delete_already_deleted_task_returns_404(client):
    created = client.post("/api/tasks", json={"title": "Title"}).json()
    client.delete(f"/api/tasks/{created['id']}")

    response = client.delete(f"/api/tasks/{created['id']}")

    assert response.status_code == 404
