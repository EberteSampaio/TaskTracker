import json
import os
from abc import ABC, abstractmethod

from src.task.exceptions.exceptions import TaskNotFoundException
from src.task.task import Task, TaskStatus


class ITaskRepository(ABC):

    @abstractmethod
    def delete(self, task_id: int) -> None:
        ...

    @abstractmethod
    def read_all(self,task_status: TaskStatus|None) ->list[Task]:
        ...

    @abstractmethod
    def create(self, task: Task) -> Task:
        ...
    @abstractmethod
    def update(self, task_id: int, description: str) -> None:
        ...

    @abstractmethod
    def mark_in_progress(self, task_id: int) -> None:
        ...

    @abstractmethod
    def mark_done(self, task_id: int) -> None:
        ...

class JsonTaskRepository(ITaskRepository):

    def __init__(self, json_filepath: str = "tasks.json") -> None:
        self.json_filepath = json_filepath

    def create(self, task: Task):
        data = self._read_file()
        task_id = 1 if len(data) < 1 else max(item["id"] for item in data) + 1
        task.id = task_id
        data.append(task.to_dict())
        self._save_file(data)


    def delete(self, task_id: int):
        data = self._read_file()
        new_data = [item for item in data if item.get("id") != task_id]
        self._save_file(new_data)

    def read_all(self, task_status: TaskStatus| None = None) -> list[Task]:
        data = self._read_file()
        return [Task.from_dict(item) for item in data if item.get("status") == task_status]

    def update(self, task_id: int, description: str) -> None:
        data = self._read_file()
        for i, item in enumerate(data):
            if item["id"] == task_id:
                task = Task.from_dict(data[i])
                task.set_description(description)
                data[i] = task.to_dict()
                break

        self._save_file(data)

    def mark_in_progress(self, task_id: int) -> None:
        data = self._read_file()
        task = None

        for i, item in enumerate(data):
            if item.get("id") == task_id:
                task = Task.from_dict(data[i])
                task.mark_in_progress()
                data[i] = task.to_dict()
                break

        if not task:
            raise TaskNotFoundException("Task not found")

        self._save_file(data)

    def mark_done(self, task_id: int) -> None:
        data = self._read_file()
        task = None
        for i, item in enumerate(data):
            if item.get("id") == task_id:
                task = Task.from_dict(data[i])
                task.mark_done()
                data[i] = task.to_dict()
                break

        if not task:
            raise TaskNotFoundException("Task not found")
        self._save_file(data)

    def _read_file(self) -> list:
        if not os.path.exists(self.json_filepath):
            return []

        with open(self.json_filepath, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def _save_file(self, data: list) -> None:
        with open(self.json_filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)