import pytest

from src.task_receiver import Task


@pytest.fixture
def task_params():
    return {"description": "Test task", "priority": 5}


@pytest.fixture
def task(task_params):
    return Task(**task_params)