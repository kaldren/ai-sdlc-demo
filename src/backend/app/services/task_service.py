from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.task import DESCRIPTION_MAX_LENGTH, TITLE_MAX_LENGTH, Task


class TaskNotFoundError(Exception):
    """Raised when an operation targets a task id that does not exist."""


class TaskValidationError(Exception):
    """Raised when task field values violate a validation rule (FR-002, data-model.md)."""


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _validate_title(title: str) -> str:
    if not title.strip():
        raise TaskValidationError("title must not be blank")
    if len(title) > TITLE_MAX_LENGTH:
        raise TaskValidationError(f"title must be at most {TITLE_MAX_LENGTH} characters")
    return title


def _validate_description(description: str) -> str:
    if len(description) > DESCRIPTION_MAX_LENGTH:
        raise TaskValidationError(
            f"description must be at most {DESCRIPTION_MAX_LENGTH} characters"
        )
    return description


def create_task(db: Session, title: str, description: str = "") -> Task:
    """FR-001, FR-002, FR-010."""
    title = _validate_title(title)
    description = _validate_description(description)
    now = _utcnow()
    task = Task(
        title=title,
        description=description,
        archived=False,
        created_at=now,
        updated_at=now,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, archived: bool = False) -> list[Task]:
    """FR-003, FR-006."""
    return (
        db.query(Task)
        .filter(Task.archived == archived)
        .order_by(Task.created_at)
        .all()
    )


def get_task(db: Session, task_id: int) -> Task:
    """FR-014."""
    task = db.get(Task, task_id)
    if task is None:
        raise TaskNotFoundError(f"task {task_id} not found")
    return task


def update_task(
    db: Session,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    archived: bool | None = None,
) -> Task:
    """FR-004, FR-005, FR-007, FR-011, FR-013, FR-014.

    Only fields that are provided (not None) are considered. `updated_at`
    advances only if at least one field's value actually changes — an
    archive/unarchive call that matches the current state is a no-op
    (FR-013) and must not advance `updated_at`.
    """
    task = get_task(db, task_id)
    changed = False

    if title is not None:
        new_title = _validate_title(title)
        if new_title != task.title:
            task.title = new_title
            changed = True

    if description is not None:
        new_description = _validate_description(description)
        if new_description != task.description:
            task.description = new_description
            changed = True

    if archived is not None and archived == task.archived:
        task.archived = archived
        changed = True

    if changed:
        task.updated_at = _utcnow()
        db.commit()
        db.refresh(task)

    return task


def delete_task(db: Session, task_id: int) -> None:
    """FR-008, FR-009, FR-014."""
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()
