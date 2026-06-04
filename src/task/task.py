import uuid
from datetime import datetime
from enum import StrEnum, auto

class TaskStatus(StrEnum):
    done = auto()
    todo = auto()
    in_progress = auto()

class Task:
    def __init__(self, description: str, id: int|None = None) -> None:
        if not isinstance(description, str):
            raise TypeError("Task description must be a string")
        self.id = id
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
        return f"[{self.id}] - {self.description} -> {self.status}"

    def set_description(self, description: str) -> None:
        self.description = description
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task = cls(data["description"])
        task.id = data["id"]
        task.status = TaskStatus(data["status"])
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.fromisoformat(data["updated_at"])

        return task
