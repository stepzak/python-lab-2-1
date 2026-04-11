from datetime import datetime
import logging
from functools import wraps
from typing import Optional

import src.task_receiver.descriptors as descriptors
from src.task_receiver.exceptions import InvalidStatusError, ExpiredError, CancelledError


def not_completed(func):
    @wraps(func)
    def wrapper(self: 'Task', *args, **kwargs):
        if self.finished:
            raise InvalidStatusError('Task already finished')
        return func(self, *args, **kwargs)

    return wrapper

def not_expired(func):
    @wraps(func)
    def wrapper(self: 'Task', *args, **kwargs):
        if self.expired:
            exc = ExpiredError('Task expired')
            if not self.finished:
                self._exception = exc
                self.status = descriptors.Status.FAILURE
            raise exc

        return func(self, *args, **kwargs)

    return wrapper


logger = logging.getLogger(__name__)


class Task:
    """
    Class representing a task
    id: UUID
    description: str
    status: Status
    deadline: datetime
    payload: dict
    """
    __slots__ = (
        "_id", "_status", "_priority", "_created_at", "_description", "_result", "_exception", "_deadline", "_payload"
    )

    id = descriptors.TaskIdDescriptor("_id")
    status = descriptors.StatusDescriptor("_status")
    priority = descriptors.PriorityDescriptor("_priority", min_priority=1, max_priority=10)
    created_at_fmt = descriptors.FormattedCreatedAtDescriptor("_created_at")

    def __init__(self, description: str, priority: int = 5, deadline: Optional[datetime] = None,
                 payload: Optional[dict] = None):
        now = datetime.now()
        if deadline and now > deadline:
            raise ValueError("Deadline must be greater than or equal to now")
        self._description = description

        self.priority = priority
        self.status = descriptors.Status.NEW
        self._created_at = datetime.now()
        self._result = self._exception = None
        self._deadline = deadline
        self._payload = payload or {}

    @property
    def deadline(self) -> Optional[datetime]:
        return self._deadline

    @property
    def time_left(self) -> float:
        """
        Returns the time left in seconds.
        :return: float
        """
        deadline = self._deadline
        if not deadline:
            return float("inf")

        return (deadline - datetime.now()).total_seconds()

    @property
    def expired(self) -> bool:
        """
        Is task expired
        :return: bool
        """
        return self.time_left < 0

    @property
    def result(self):
        """
        Returns the result of the task.
        :return: Any
        :raises Exception if task failed
        """
        if self.exception:
            raise self.exception
        return self._result

    @result.setter
    @not_completed
    @not_expired
    def result(self, value):
        """
        Set the result of the task.
        :param value:
        :return: None
        :raise ExpiredError if task expired
        :raise CancelledError if task was cancelled
        """
        self._result = value
        self.status = descriptors.Status.SUCCESS

    @property
    def exception(self) -> Exception:
        return self._exception

    @exception.setter
    @not_completed
    @not_expired
    def exception(self, value: Exception):
        if not isinstance(value, Exception):
            raise TypeError("Must be an exception")

        self._exception = value
        self.status = descriptors.Status.FAILURE

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if self.finished:
            raise InvalidStatusError("Task is already finished")
        self._description = value

    @property
    def finished(self) -> bool:
        return self.status in {descriptors.Status.FAILURE, descriptors.Status.SUCCESS, descriptors.Status.CANCELLED}

    def __repr__(self):
        return f"<Task {self.id} | {self.status.value} | Priority: {self.priority}>"

    @not_completed
    @not_expired
    def start(self) -> None:
        self.status = descriptors.Status.PENDING
        logger.info(f"Task {self.__repr__()} started")
        logger.info(f"Payload: {self._payload}")


    @not_completed
    @not_expired
    def cancel(self, msg: Optional[str] = None):
        if not msg:
            msg = f"Task {self.id} cancelled"

        self._exception = CancelledError(msg)
        self.status = descriptors.Status.CANCELLED

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "status": self.status.value,
            "priority": self.priority,
            "description": self.description,
            "created_at": self.created_at_fmt,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "finished": self.finished,
            "expired": self.expired
        }


    def __lt__(self, other: 'Task') -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        if self.priority != other.priority:
            return self.priority > other.priority
        return self._created_at < other._created_at
