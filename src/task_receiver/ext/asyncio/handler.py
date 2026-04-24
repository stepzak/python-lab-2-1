from typing import Protocol, runtime_checkable, Any

from src.task_receiver import Task


@runtime_checkable
class TaskHandler(Protocol):
    async def handle(self, task: Task) -> Any: ...