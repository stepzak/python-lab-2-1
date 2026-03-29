import enum
import uuid

from src.task_receiver.exceptions import ImmutableError, NotCreatedError, InvalidStatusError, InvalidPriorityError


class Status(enum.Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    CANCELLED = "CANCELLED"


class BasicDescriptor:
    def __init__(self, inner_name: str):
        self.inner_name = inner_name

    def __set_name__(self, owner, name):
        if name == self.inner_name:
            raise ValueError("Inner name and attr name must not be the same")
        self.name = name


class StatusDescriptor(BasicDescriptor):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.inner_name)

    def __set__(self, instance, value):
        if not isinstance(value, Status):
            raise InvalidStatusError(f"{value} is not a valid status. Status must be of type {Status.__name__}")

        current_status = getattr(instance, self.inner_name, None)

        if current_status == Status.PENDING:
            if value == Status.NEW:
                raise InvalidStatusError(f"Cannot move task from PENDING to NEW")

        elif current_status in {Status.SUCCESS, Status.FAILURE, Status.CANCELLED}:
            raise InvalidStatusError(f"Task is already in terminal state: {current_status.value}")

        setattr(instance, self.inner_name, value)


class TaskIdDescriptor(BasicDescriptor):
    def __get__(self, instance, owner):
        if instance is None:
            return self

        if not hasattr(instance, self.inner_name):
            setattr(instance, self.inner_name, uuid.uuid4())

        return getattr(instance, self.inner_name)

    def __set__(self, instance, value):
        raise ImmutableError("Task ID is immutable")


class FormattedCreatedAtDescriptor(BasicDescriptor):
    def __get__(self, instance, owner):
        if instance is None:
            return self

        ts = getattr(instance, self.inner_name, None)
        if ts:
            return ts.strftime("%Y-%m-%d %H:%M:%S")
        raise NotCreatedError("Task was not created")


class PriorityDescriptor:
    def __init__(self, inner_name: str, min_priority: int, max_priority: int):
        self.inner_name = inner_name
        self.min_priority = min_priority
        self.max_priority = max_priority

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.inner_name, None)

    def __set__(self, instance, value):
        if not isinstance(value, int) or value < self.min_priority or value > self.max_priority:
            raise InvalidPriorityError(f"Priority must be between {self.min_priority} and {self.max_priority}")

        setattr(instance, self.inner_name, value)
