from typing import Protocol, runtime_checkable, Iterable

from src.task_receiver.task import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterable[Task]:
        """
        Get all tasks
        :return: iterable of Task
        """


    def load_tasks(self) -> None:
        """
        Load all tasks into TaskSource
        :return: None
        """