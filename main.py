from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple in-memory CRUD API for managing tasks."
)


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Publish project to GitHub", "done": False},
]


@app.get("/", summary="Get API information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Check API health")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get a task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )


@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
def create_task(task_data: TaskCreate):
    title = task_data.title.strip()

    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and cannot be empty"
        )

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, task_data: TaskUpdate):
    task = next(
        (task for task in tasks if task["id"] == task_id),
        None
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    updates = task_data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body cannot be empty"
        )

    if "title" in updates:
        title = updates["title"]

        if not isinstance(title, str) or not title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title is required and cannot be empty"
            )

        task["title"] = title.strip()

    if "done" in updates:
        task["done"] = updates["done"]

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task"
)
def delete_task(task_id: int):
    task_index = next(
        (index for index, task in enumerate(tasks) if task["id"] == task_id),
        None
    )

    if task_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    tasks.pop(task_index)

    return None