from abc import ABC, abstractmethod
from argparse import Namespace

from src.task.exceptions.exceptions import DomainException
from src.task.repository import ITaskRepository
from src.task.task import Task, TaskStatus


class ICommand(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

class CommandExecutor:
    def run(self, command: ICommand) -> None:
        command.execute()

class CreateTaskCommand(ICommand):
    def __init__(self, repository: ITaskRepository, args: Namespace) -> None:
        self.repository = repository
        self.description = args.description

    def execute(self) -> None:
        task = Task(description=self.description)
        self.repository.create(task)
        print(f"Task added successfully (ID: {task.id})")

class ReadTaskCommand(ICommand):
    def __init__(self, repository: ITaskRepository, args: Namespace) -> None:
        self.repository = repository
        self.task_status = args.status

    def execute(self) -> None:

        status = TaskStatus(self.task_status) if self.task_status else None

        data = self.repository.read_all(status)

        if not data:
            print(f"There is no task for the given parameter ({self.task_status}).")
            return

        print("Tasks")
        for task in data:
            print(task)

class UpdateTaskCommand(ICommand):

    def __init__(self,repository: ITaskRepository, args: Namespace) -> None:
        self.repository = repository
        self.task_id = args.id
        self.description = args.description

    def execute(self) -> None:
        self.repository.update(self.task_id, self.description)

class DeleteTaskCommand(ICommand):
    def __init__(self, repository: ITaskRepository, args: Namespace) -> None:
        self.repository = repository
        self.task_id = args.id

    def execute(self) -> None:
        self.repository.delete(self.task_id)

class MarkInProgressTaskCommand(ICommand):
    def __init__(self,repository: ITaskRepository, args: Namespace) -> None:
        self.repository = repository
        self.task_id = args.id

    def execute(self) -> None:
        self.repository.mark_in_progress(self.task_id)

class MarkDoneTaskCommand(ICommand):
    def __init__(self, repository: ITaskRepository, args: Namespace) -> None:
        self.repository = repository
        self.task_id = args.id

    def execute(self) -> None:
        self.repository.mark_done(self.task_id)