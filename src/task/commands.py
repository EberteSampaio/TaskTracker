import uuid
from abc import ABC, abstractmethod

from src.task.task import Task, TaskStatus


class ICommand(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

class CommandExecutor:
    def run(self, command: ICommand) -> None:
        command.execute()

class CreateTaskCommand(ICommand):
    def __init__(self, description: str) -> None:
        self.description = description

    def execute(self) -> None:
        task = Task(self.description)
        print(f"Criando tarefa '{self.description}' com ID: {task.id}")

class ReadTaskCommand(ICommand):
    def __init__(self, task_status: TaskStatus) -> None:
        self.task_status = task_status

    def execute(self) -> None:
        print(f"{self.task_status}")

class UpdateTaskCommand(ICommand):

    def __init__(self,update_data:list[str]) -> None:
        self.task_id = update_data[0]
        self.description = update_data[1]

    def execute(self) -> None:
        print(f"Update - id: {self.task_id} -> new: {self.description}")

class DeleteTaskCommand(ICommand):
    def __init__(self, task_id: str) -> None:
        self.task_id = task_id

    def execute(self) -> None:
        print(f"Delete - id: {self.task_id}")