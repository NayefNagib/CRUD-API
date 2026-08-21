from app.repositories.base import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_tasks(self):
        return self.repository.get_all()

    def get_task(self, task_id: int):
        return self.repository.get_by_id(task_id)

    def create_task(self, title: str):
        title = title.strip()

        if not title:
            raise ValueError("Title cannot be empty")

        return self.repository.create(title)

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        done: bool | None = None
    ):
        if title is not None:
            title = title.strip()

            if not title:
                raise ValueError("Title cannot be empty")

        return self.repository.update(
            task_id,
            title,
            done
        )

    def delete_task(self, task_id: int):
        return self.repository.delete(task_id)