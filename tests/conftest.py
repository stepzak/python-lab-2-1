import pytest

from src.task_receiver import Task
from src.task_receiver.task_queue import TaskQueue


@pytest.fixture
def task_params():
    return {"description": "Test task", "priority": 5}


@pytest.fixture
def task(task_params):
    return Task(**task_params)


@pytest.fixture
def sample_tasks():
    return [
        Task("Low priority", priority=1),
        Task("High priority", priority=10),
        Task("Medium priority", priority=5),
    ]

@pytest.fixture
def empty_queue():
    return TaskQueue()