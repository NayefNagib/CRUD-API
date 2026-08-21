import os

import psycopg
from psycopg.rows import dict_row

from app.repositories.base import TaskRepository


class PostgresTaskRepository(TaskRepository):

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not set")

    def get_connection(self):
        return psycopg.connect(
            self.database_url,
            row_factory=dict_row
        )

    def get_all(self) -> list[dict]:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    ORDER BY id
                    """
                )

                return cursor.fetchall()

    def get_by_id(self, task_id: int) -> dict | None:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    WHERE id = %s
                    """,
                    (task_id,)
                )

                return cursor.fetchone()

    def create(self, title: str) -> dict:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, FALSE)
                    RETURNING id, title, done
                    """,
                    (title,)
                )

                return cursor.fetchone()

    def update(
        self,
        task_id: int,
        title: str | None = None,
        done: bool | None = None
    ) -> dict | None:

        current = self.get_by_id(task_id)

        if current is None:
            return None

        new_title = (
            title
            if title is not None
            else current["title"]
        )

        new_done = (
            done
            if done is not None
            else current["done"]
        )

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s,
                        done = %s
                    WHERE id = %s
                    RETURNING id, title, done
                    """,
                    (new_title, new_done, task_id)
                )

                return cursor.fetchone()

    def delete(self, task_id: int) -> bool:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM tasks
                    WHERE id = %s
                    """,
                    (task_id,)
                )

                return cursor.rowcount > 0