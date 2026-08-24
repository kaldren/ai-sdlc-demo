import pytest

from app.services import task_service


# --- User Story 1: Create a Task ---


def test_create_task_with_title_and_description(db_session):
    task = task_service.create_task(db_session, "Buy milk", "2% milk, one gallon")
    assert task.id is not None
    assert task.title == "Buy milk"
    assert task.description == "2% milk, one gallon"
    assert task.archived is False
    assert task.created_at == task.updated_at


def test_create_task_with_title_only(db_session):
    task = task_service.create_task(db_session, "Buy milk")
    assert task.description == ""


def test_create_task_rejects_blank_title(db_session):
    with pytest.raises(task_service.TaskValidationError):
        task_service.create_task(db_session, "   ")


def test_create_task_rejects_overlong_title(db_session):
    with pytest.raises(task_service.TaskValidationError):
        task_service.create_task(db_session, "x" * 201)


def test_create_task_rejects_overlong_description(db_session):
    with pytest.raises(task_service.TaskValidationError):
        task_service.create_task(db_session, "Buy milk", "y" * 2001)


def test_list_tasks_defaults_to_active(db_session):
    active = task_service.create_task(db_session, "Active task")
    archived = task_service.create_task(db_session, "Archived task")
    task_service.update_task(db_session, archived.id, archived=True)

    active_list = task_service.list_tasks(db_session, archived=False)
    archived_list = task_service.list_tasks(db_session, archived=True)

    assert [t.id for t in active_list] == [active.id]
    assert [t.id for t in archived_list] == [archived.id]


# --- User Story 2: Edit a Task ---


def test_update_task_title_and_description(db_session):
    task = task_service.create_task(db_session, "Old title", "Old description")
    original_created_at = task.created_at

    updated = task_service.update_task(
        db_session, task.id, title="New title", description="New description"
    )

    assert updated.title == "New title"
    assert updated.description == "New description"
    assert updated.created_at == original_created_at
    assert updated.updated_at > original_created_at


def test_update_task_rejects_blank_title(db_session):
    task = task_service.create_task(db_session, "Title")
    with pytest.raises(task_service.TaskValidationError):
        task_service.update_task(db_session, task.id, title="   ")


def test_update_task_rejects_overlong_title(db_session):
    task = task_service.create_task(db_session, "Title")
    with pytest.raises(task_service.TaskValidationError):
        task_service.update_task(db_session, task.id, title="x" * 201)


def test_update_task_rejects_overlong_description(db_session):
    task = task_service.create_task(db_session, "Title")
    with pytest.raises(task_service.TaskValidationError):
        task_service.update_task(db_session, task.id, description="y" * 2001)


def test_update_task_succeeds_while_archived(db_session):
    task = task_service.create_task(db_session, "Title")
    task_service.update_task(db_session, task.id, archived=True)

    updated = task_service.update_task(db_session, task.id, title="New title")

    assert updated.title == "New title"
    assert updated.archived is True


def test_update_task_unknown_id_raises_not_found(db_session):
    with pytest.raises(task_service.TaskNotFoundError):
        task_service.update_task(db_session, 999, title="Anything")


# --- User Story 3: Archive and Unarchive a Task ---


def test_archive_active_task(db_session):
    task = task_service.create_task(db_session, "Title")
    original_updated_at = task.updated_at

    archived = task_service.update_task(db_session, task.id, archived=True)

    assert archived.archived is True
    assert archived.updated_at > original_updated_at


def test_archiving_already_archived_task_is_noop(db_session):
    task = task_service.create_task(db_session, "Title")
    archived = task_service.update_task(db_session, task.id, archived=True)
    updated_at_after_archive = archived.updated_at

    noop_result = task_service.update_task(db_session, task.id, archived=True)

    assert noop_result.archived is True
    assert noop_result.updated_at == updated_at_after_archive


def test_unarchive_archived_task(db_session):
    task = task_service.create_task(db_session, "Title")
    task_service.update_task(db_session, task.id, archived=True)

    unarchived = task_service.update_task(db_session, task.id, archived=False)

    assert unarchived.archived is False


def test_unarchiving_already_active_task_is_noop(db_session):
    task = task_service.create_task(db_session, "Title")
    original_updated_at = task.updated_at

    noop_result = task_service.update_task(db_session, task.id, archived=False)

    assert noop_result.archived is False
    assert noop_result.updated_at == original_updated_at


# --- User Story 4: Delete a Task ---


def test_delete_active_task(db_session):
    task = task_service.create_task(db_session, "Title")
    task_service.delete_task(db_session, task.id)

    with pytest.raises(task_service.TaskNotFoundError):
        task_service.get_task(db_session, task.id)


def test_delete_archived_task(db_session):
    task = task_service.create_task(db_session, "Title")
    task_service.update_task(db_session, task.id, archived=True)

    task_service.delete_task(db_session, task.id)

    with pytest.raises(task_service.TaskNotFoundError):
        task_service.get_task(db_session, task.id)


def test_delete_unknown_id_raises_not_found(db_session):
    with pytest.raises(task_service.TaskNotFoundError):
        task_service.delete_task(db_session, 999)


def test_deleted_task_not_retrievable(db_session):
    task = task_service.create_task(db_session, "Title")
    task_service.delete_task(db_session, task.id)

    with pytest.raises(task_service.TaskNotFoundError):
        task_service.update_task(db_session, task.id, title="Resurrect?")
