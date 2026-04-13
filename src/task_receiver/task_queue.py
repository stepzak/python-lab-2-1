import heapq
from typing import Optional, Iterable, Any, Iterator

from src.task_receiver import Task

TaskQueueQuery = dict[str, dict[str, Any]]

class TaskQueue(Iterable[Task]):
    __slots__ = ("_storage", "_index")
    """
    Tasks Priority Queue.
    Old tasks prioritised over new ones
    """

    def __init__(self, tasks: Optional[Iterable[Task]] = None):
        self._storage = tasks or []
        self._storage = list(self._storage)
        self._index = 0
        heapq.heapify(self._storage)

    def push(self, task: Task):
        heapq.heappush(self._storage, task)

    def pop(self) -> Task:
        if not self._storage:
            raise IndexError("Task queue is empty")
        return heapq.heappop(self._storage)

    def peek(self) -> Task:
        if not self._storage:
            raise IndexError("Task queue is empty")

        return self._storage[-1]

    def __iter__(self) -> Iterable[Task]:
        for task in self._storage:
            yield task

    def query(self, params: TaskQueueQuery) -> Iterator['Task']:
        """
        Get Iterator of Task by query
        :param params: dict of params. Example: {"attr1": {"min": 1, "max": 4}, "attr2": {"eq": 3}}
        Will return tasks that have "attr1" between 1 and 4; and attr2 == 3
        :return:
        """
        return filter(lambda x: self._matches(x, params), self._storage)

    @staticmethod
    def _matches(task: 'Task', params: dict[str, dict[str, Any]]) -> bool:
        for attr, conditions in params.items():
            val = getattr(task, attr, None)

            for op, target in conditions.items():
                if op == "eq" and not (val == target):
                    return False
                elif op == "min" and not (val >= target):
                    return False
                elif op == "max" and not (val <= target):
                    return False
        return True

    def __len__(self) -> int:
        return len(self._storage)

