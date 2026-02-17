from typing import Protocol, runtime_checkable, Iterable

from src.task_receiver.task import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterable[Task]:
        """
        Get all tasks
        :return: iterable of Task
        """

    def get_task(self, id: int) -> Task:
        """
        Get task by id
        :param id: id of task
        :return: Task with passed id
        """
