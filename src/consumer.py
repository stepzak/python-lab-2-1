from src.task_receiver.source import TaskSource
from src.task_receiver.task import Task
from src.utils.checkers import strict_annotations

@strict_annotations()
def consumer(source: TaskSource) -> list[Task]:
    """
    Example of task source consumer
    :param source: TaskSource
    :return: None
    :raises: TypeError if source is not TaskSource
    """
    tasks = source.get_tasks()
    completed = []
    for task in tasks:
        print(f"Executing task {task.id} with payload {task.payload}")
        completed.append(task)

    return completed