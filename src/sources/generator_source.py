from typing import Iterable

from src.task_receiver.task import Task


class GeneratorSource:
    def __init__(self, max_tasks: int = 5):
        self.cur_task = 0
        self.max_tasks = max_tasks

    def get_tasks(self) -> Iterable[Task]:
        while self.cur_task < self.max_tasks:
            yield Task(
                description = f"Task {self.cur_task}",
                payload = {"name": f"Task N {self.cur_task}", "n": self.cur_task},
            )
            self.cur_task += 1

    def load_tasks(self) -> None: ...