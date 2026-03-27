from datetime import datetime

import src.task_receiver.descriptors as descriptors
from src.task_receiver.exceptions import InvalidStatusError


class Task:
    __slots__ = (
        "_id", "_status", "_priority", "_created_at", "_description"
    )

    id = descriptors.TaskIdDescriptor("_id")
    status = descriptors.StatusDescriptor("_status")
    priority = descriptors.PriorityDescriptor("_priority", min_priority=1, max_priority=10)
    created_at_fmt = descriptors.FormattedCreatedAtDescriptor("_created_at")

    def __init__(self, description: str, priority: int = 5):
        self._description = description

        self.priority = priority
        self.status = descriptors.Status.NEW
        self._created_at = datetime.now()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if self.finished:
            raise InvalidStatusError("Task is already finished")
        self._description = value

    @property
    def finished(self) -> bool:
        return self.status in {descriptors.Status.FAILURE, descriptors.Status.SUCCESS, descriptors.Status.CANCELLED}

    def __repr__(self):
        return f"<Task {self.id} | {self.status.value} | Priority: {self.priority}>"