from typing import Iterable

from src.task_receiver import Task
import time

class ApiSource:
    def __init__(self, url: str, n_tasks: int = 5):
        self.url = url
        self.n_tasks = n_tasks

    def get_tasks(self) -> Iterable[Task]:
        for i in range(self.n_tasks):
            payload = {"n_task": i, "url": self.url}
            yield Task(description = f"API Task {i}", payload = payload)
            time.sleep(0.02)
