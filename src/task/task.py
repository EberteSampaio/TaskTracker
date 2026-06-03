import uuid
from datetime import datetime
from enum import StrEnum, auto

class TaskStatus(StrEnum):
    done = auto()
    todo = auto()
    in_progress = auto()

class Task:
    def __init__(self, description: str) -> None:
        if not isinstance(description, str):
            raise TypeError("Task description must be a string")
        self.id = str(uuid.uuid4())
        self.description = description
        self.status = TaskStatus.todo
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


    def mark_in_progress(self) -> None:
        self.status = TaskStatus.in_progress
        self.updated_at = datetime.now()

    def mark_done(self) -> None:
        self.status = TaskStatus.done
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        return f"{self.description} - {self.status}"
