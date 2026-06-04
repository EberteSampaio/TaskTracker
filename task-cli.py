import argparse

from src.task.commands import CreateTaskCommand, UpdateTaskCommand, DeleteTaskCommand, ReadTaskCommand, CommandExecutor, \
    MarkDoneTaskCommand, MarkInProgressTaskCommand
from src.task.exceptions.exceptions import CommandNotFoundException, DomainException
from src.task.repository import JsonTaskRepository
from src.task.task import TaskStatus


def parser_config():
    parser   = argparse.ArgumentParser("CLI Task Tracker")
    subparse = parser.add_subparsers(dest="action",required=True, help="Add a new task")

    parser_add = subparse.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="Task description")

    parser_delete = subparse.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="Task ID")

    parser_update = subparse.add_parser("update", help="Delete a task")
    parser_update.add_argument("id", type=int, help="Task ID")
    parser_update.add_argument("description", type=str, help="new description for task")

    parser_list = subparse.add_parser("list", help="List all tasks")
    parser_list.add_argument(
        "status",
        nargs="?",
        choices=[TaskStatus.todo.value, TaskStatus.done.value, TaskStatus.in_progress.value],
        help="Filter by status: done, in-progress, or todo"
    )

    parser_mip= subparse.add_parser("mark-in-progress", help="Mark task as in-progress")
    parser_mip.add_argument("id", type=int, help="Task ID")

    parser_mo= subparse.add_parser("mark-done", help="Mark task as done")
    parser_mo.add_argument("id", type=int, help="Task ID")

    return parser.parse_args()


def dispach_command(args: argparse.Namespace) -> None:
    router = {
        "add": CreateTaskCommand,
        "update": UpdateTaskCommand,
        "delete": DeleteTaskCommand,
        "list": ReadTaskCommand,
        "mark-in-progress": MarkInProgressTaskCommand,
        "mark-done": MarkDoneTaskCommand,
    }

    CommandClass = router.get(args.action)

    if not CommandClass:
        raise CommandNotFoundException("The requested command does not exist.")

    command_executor = CommandExecutor()
    command_executor.run(
        CommandClass(
            repository=JsonTaskRepository(),
            args=args
        )
    )


def main() -> None:
    try:
        args = parser_config()
        dispach_command(args)
    except DomainException as e:
        print(e)
    except Exception as e:
        raise e

if __name__ == '__main__':
    main()