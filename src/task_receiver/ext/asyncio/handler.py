from typing import Protocol, runtime_checkable, Any

from src.task_receiver import Task


@runtime_checkable
class AsyncTaskHandler(Protocol):
    """
    Async task handler protocol
    """
    async def handle(self, task: Task) -> Any:
        """
        Handler function that will be called within ```AsyncExecutor```
        :param task: Task to handle
        :return: Any
        """