from abc import ABC, abstractmethod
from typing import Any


class TaskRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def create(self, title: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def update(
        self,
        task_id: int,
        title: str | None = None,
        done: bool | None = None
    ) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass