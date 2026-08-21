from fastapi import FastAPI

from app.repositories.postgres_task_repository import (
    PostgresTaskRepository
)
from app.routes.tasks import router
from app.services.tasks import TaskService


app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing tasks."
)


repository = PostgresTaskRepository()
task_service = TaskService(repository)

app.include_router(router)


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