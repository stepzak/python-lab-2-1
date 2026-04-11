import logging

from src.task_receiver.source import TaskSource
from src.task_receiver.task import Task
from src.utils.checkers import strict_annotations

logger = logging.getLogger(__name__)

@strict_annotations()
def consumer(source: TaskSource) -> list[Task]:
    """
    Example of task source consumer
    :param source: TaskSource
    :return: None
    :raises: TypeError if source is not TaskSource
    """
    source.load_tasks()
    tasks = source.get_tasks()
    completed = []
    for task in tasks:
        logger.info(f"Executing task {task.id}")
        task.start()
        task.result = {"result": "ok"}
        completed.append((task.result, task.description, task.status))

    return completed