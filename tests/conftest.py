import pytest

from src.task_receiver import Task
from src.task_receiver.task_queue import TaskQueue
import asyncio
import logging
from src.task_receiver.ext.asyncio import AsyncExecutor


@pytest.fixture
def task_params():
    return {"description": "Test task", "priority": 5}


@pytest.fixture
def simple_task(task_params):
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

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def executor():
    async with AsyncExecutor(max_workers=2) as ex:
        yield ex

@pytest.fixture
def create_task():
    def _create(priority=5, desc="Test Task"):
        return Task(priority=priority, description=desc)
    return _create