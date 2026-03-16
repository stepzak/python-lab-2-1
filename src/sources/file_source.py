from pathlib import Path
from typing import Iterable

from src.task_receiver.task import Task

class FileSource:
    def __init__(self, filepath: Path):
        self.filepath = filepath

    def get_tasks(self) -> Iterable[Task]:
        with open(self.filepath) as f:
            head = next(f)
            headers = head.rstrip().split(",")[1:]
            for line in f:
                payload = {}
                data = line.rstrip().split(",")
                if len(headers) != len(data)-1:
                    raise TypeError(f"Expected {len(headers)} headers, got {len(data) - 1}")
                for i in range(1, len(data)):
                    payload[headers[i-1]] = data[i]
                yield Task(id = int(data[0]), payload = payload)

