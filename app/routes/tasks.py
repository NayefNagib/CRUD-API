from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.services.tasks import TaskService
from app.repositories.postgres_task_repository import PostgresTaskRepository


router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


def get_task_service() -> TaskService:
    repository = PostgresTaskRepository()
    return TaskService(repository)


@router.get("")
def get_tasks(
    service: TaskService = Depends(get_task_service),
):
    return service.get_tasks()


@router.get("/{task_id}")
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.post("", status_code=201)
def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.create_task(task.title)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    try:
        updated_task = service.update_task(
            task_id=task_id,
            title=task.title,
            done=task.done,
        )

        if updated_task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return updated_task

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    deleted_task = service.delete_task(task_id)

    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return deleted_task