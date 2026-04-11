import json
from pathlib import Path
from typing import Iterable, Union
from datetime import datetime
from jsonschema import validate, ValidationError

from src.task_receiver.task import Task
from src.task_receiver.source import TaskSource
from src.task_receiver.task_queue import TaskQueue


class FileSource(TaskSource):
    TASK_SCHEMA = {
        "type": "object",
        "properties": {
            "description": {"type": "string", "minLength": 1},
            "priority": {"type": "integer", "minimum": 1, "maximum": 10},
            "deadline": {"type": "string", "format": "date-time"},
            "payload": {"type": "object"}
        },
        "required": ["description"],
        "additionalProperties": False
    }

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self._tasks = TaskQueue()
        self._loaded = False

    def load_tasks(self):
        self._loaded = True
        if not self.file_path.exists():
            return

        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON root must be a list of tasks")
            except json.JSONDecodeError:
                return

        for index, item in enumerate(data):
            try:
                validate(instance=item, schema=self.TASK_SCHEMA)
                self._tasks.push(self._create_task(item))
            except ValidationError as e:
                print(f"Skipping task at index {index}: {e.message}")

    def get_tasks(self) -> Iterable[Task]:
        """

        :return: Iterable[Task]
        :raise RuntimeError: source was not loaded
        """
        if not self._loaded:
            raise RuntimeError("File source is not loaded")
        return self._tasks

    @staticmethod
    def _create_task(item: dict) -> Task:
        deadline_str = item.get("deadline")
        deadline = datetime.fromisoformat(deadline_str) if deadline_str else None

        return Task(
            description=item["description"],
            priority=item.get("priority", 5),
            deadline=deadline,
            payload=item.get("payload")
        )
