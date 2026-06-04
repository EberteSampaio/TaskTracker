import argparse

from src.task.commands import CreateTaskCommand, UpdateTaskCommand, DeleteTaskCommand, ReadTaskCommand, CommandExecutor, \
    MarkDoneTaskCommand, MarkInProgressTaskCommand
from src.task.dispatch_action import DispatchAction
from src.task.exceptions.exceptions import CommandNotFoundException, DomainException
from src.task.repository import JsonTaskRepository


def parser_config():
    parser = argparse.ArgumentParser("CLI Task Tracker")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-a","--add",    action=DispatchAction,  type=str,help="Add a task")
    group.add_argument("-u","--update", action=DispatchAction, nargs=2, metavar=("Id", "Description"), type=str,help="Update a task")
    group.add_argument("-d","--delete", action=DispatchAction,  type=str,help="Delete a task")

    group.add_argument(
        "-l",
        "--list",
        action=DispatchAction,
        nargs="?",
        const="all",
        choices=["todo", "done", "in_progress", "all"],
        type=str,
        help="List tasks"
    )


    group.add_argument("-mi","--mark_in_progress", action=DispatchAction,  metavar=("Id"), type=str,help="Mark in progress a task")
    group.add_argument("-md","--mark_done", action=DispatchAction, metavar=("Id"), type=str,help="Mark done a task")

    return parser.parse_args()


def dispach_command(args: argparse.Namespace) -> None:
    router = {
        "add": CreateTaskCommand,
        "update": UpdateTaskCommand,
        "delete": DeleteTaskCommand,
        "list": ReadTaskCommand,
        "mark_in_progress": MarkInProgressTaskCommand,
        "mark_done": MarkDoneTaskCommand,
    }

    CommandClass = router.get(args.command_allowed)

    if not CommandClass:
        raise CommandNotFoundException("The requested command does not exist.")

    command_executor = CommandExecutor()
    command_executor.run(
        CommandClass(
            repository=JsonTaskRepository(),
            payload=args.command_value
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