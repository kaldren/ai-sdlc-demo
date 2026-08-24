from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.schemas import TaskCreate, TaskListResponse, TaskRead, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> TaskRead:
    try:
        task = task_service.create_task(db, payload.title, payload.description)
    except task_service.TaskValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return TaskRead.model_validate(task)


@router.get("", response_model=TaskListResponse)
def list_tasks(archived: bool = False, db: Session = Depends(get_db)) -> TaskListResponse:
    tasks = task_service.list_tasks(db, archived=archived)
    return TaskListResponse(tasks=[TaskRead.model_validate(t) for t in tasks])


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskRead:
    try:
        task = task_service.get_task(db, task_id)
    except task_service.TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)) -> TaskRead:
    try:
        task = task_service.update_task(
            db,
            task_id,
            title=payload.title,
            description=payload.description,
            archived=payload.archived,
        )
    except task_service.TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except task_service.TaskValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    try:
        task_service.delete_task(db, task_id)
    except task_service.TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
