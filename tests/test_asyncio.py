import pytest
import asyncio
from src.task_receiver.descriptors import Status


class MockHandler:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    async def handle(self, task):
        await asyncio.sleep(0.05)
        if self.should_fail:
            raise ValueError("Intentional failure")
        return f"Result for {task.description}"


@pytest.mark.asyncio
async def test_successful_execution(executor, create_task):
    handler = MockHandler()
    executor.register_handler("test_type", handler)
    task = create_task(desc="Task 1")

    await executor.submit("test_type", task)
    await asyncio.wait_for(executor.queue.join(), timeout=1.0)

    assert task.status == Status.SUCCESS
    assert task.result == "Result for Task 1"
    assert task.exception is None


@pytest.mark.asyncio
async def test_priority_logic(executor, create_task):
    class FastHandler:
        async def handle(self, task): return "done"

    executor.register_handler("prio", FastHandler())

    t_low = create_task(priority=10, desc="Low")
    t_high = create_task(priority=1, desc="High")

    await executor.submit("prio", t_low)
    await executor.submit("prio", t_high)

    await asyncio.wait_for(executor.queue.join(), timeout=2.0)

    assert t_high.status == Status.SUCCESS
    assert t_low.status == Status.SUCCESS


@pytest.mark.asyncio
async def test_handler_error_handling(executor, create_task):
    executor.register_handler("fail_type", MockHandler(should_fail=True))
    task = create_task()

    await executor.submit("fail_type", task)
    await asyncio.wait_for(executor.queue.join(), timeout=1.0)

    assert task.status == Status.FAILURE
    assert isinstance(task.exception, ValueError)
    assert str(task.exception) == "Intentional failure"


@pytest.mark.asyncio
async def test_missing_handler_logic(executor, create_task):
    task = create_task()

    await executor.submit("xd", task)
    await asyncio.wait_for(executor.queue.join(), timeout=1.0)

    assert task.status == Status.FAILURE
    assert "No handler for type" in str(task.exception)


@pytest.mark.asyncio
async def test_multiple_concurrent_tasks(executor, create_task):
    executor.register_handler("multi", MockHandler())
    tasks = [create_task(desc=f"T{i}") for i in range(5)]

    for t in tasks:
        await executor.submit("multi", t)

    await asyncio.wait_for(executor.queue.join(), timeout=2.0)

    assert all(t.status == Status.SUCCESS for t in tasks)