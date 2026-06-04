from abc import ABC, abstractmethod
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
    def __init__(self, repository: ITaskRepository, payload: str) -> None:
        self.repository = repository
        self.description = payload

    def execute(self) -> None:
        task = Task(self.description)
        self.repository.create(task)
        print(f"Task added successfully (ID: {task.id})")

class ReadTaskCommand(ICommand):
    def __init__(self, repository: ITaskRepository, payload: str|None = None) -> None:
        self.repository = repository
        self.task_status = payload

    def execute(self) -> None:
        filter = None

        if self.task_status and self.task_status != "all":
            filter = TaskStatus(self.task_status)

        data = self.repository.read_all(filter)

        if not data:
            print(f"There is no task for the given parameter ({self.task_status}).")
            return

        print("Tasks")
        for task in data:
            print(f"""
{task}
            """)



class UpdateTaskCommand(ICommand):

    def __init__(self,repository: ITaskRepository, payload:str) -> None:
        self.repository = repository
        self.task_id = payload[0]
        self.description = payload[1]

    def execute(self) -> None:
        self.repository.update(self.task_id, self.description)

class DeleteTaskCommand(ICommand):
    def __init__(self, repository: ITaskRepository, payload: str) -> None:
        self.repository = repository
        self.task_id = payload

    def execute(self) -> None:
        self.repository.delete(self.task_id)

class MarkInProgressTaskCommand(ICommand):
    def __init__(self,repository: ITaskRepository, payload: str) -> None:
        self.repository = repository
        self.task_id = payload

    def execute(self) -> None:
        self.repository.mark_in_progress(self.task_id)

class MarkDoneTaskCommand(ICommand):
    def __init__(self, repository: ITaskRepository, payload: str) -> None:
        self.repository = repository
        self.task_id = payload

    def execute(self) -> None:
        self.repository.mark_done(self.task_id)