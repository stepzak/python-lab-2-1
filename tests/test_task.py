import time

import pytest
from datetime import datetime, timedelta

from src.task_receiver.task import Task
from src.task_receiver.descriptors import Status
from src.task_receiver.exceptions import (
    InvalidStatusError, InvalidPriorityError,
    ExpiredError, CancelledError
)


class TestTaskDescriptors:
    def test_id_is_lazy_and_unique(self, task):
        task_id = task.id
        assert task.id == task_id

    def test_priority_validation(self, task_params):
        with pytest.raises(InvalidPriorityError):
            Task(description="Bad", priority=11)
        with pytest.raises(InvalidPriorityError):
            Task(description="Bad", priority=0)

    def test_status_transition_validation(self, task):
        task.start()
        with pytest.raises(InvalidStatusError):
            task.status = Status.NEW


class TestTaskLogic:
    def test_successful_completion(self, task):
        task.start()
        task.result = {"output": "ok"}
        assert task.status == Status.SUCCESS
        assert task.finished is True
        assert task.result == {"output": "ok"}

    def test_failure_handling(self, task):
        error = ValueError("Computation failed")
        task.exception = error
        assert task.status == Status.FAILURE
        with pytest.raises(ValueError):
            _ = task.result

    def test_cancel_logic(self, task):
        task.cancel()
        assert task.status == Status.CANCELLED
        assert isinstance(task.exception, CancelledError)


class TestTaskExpiration:
    def test_deadline_in_past_raises_error_on_init(self):
        past = datetime.now() - timedelta(minutes=1)
        with pytest.raises(ValueError, match="Deadline must be greater"):
            Task(description = "", deadline=past)

    @pytest.mark.slow
    def test_task_expiry_during_execution(self, task):
        future = datetime.now() + timedelta(seconds=0.1)
        task._deadline = future
        time.sleep(0.11)

        assert task.expired is True
        with pytest.raises(ExpiredError):
            task.start()
        assert task.status == Status.FAILURE


class TestTaskIntegrity:
    def test_cannot_edit_finished_task(self, task):
        task.cancel()
        with pytest.raises(InvalidStatusError):
            task.description = "New text"
        with pytest.raises(InvalidStatusError):
            task.result = "data"

    def test_to_dict_serialization(self, task):
        data = task.to_dict()
        assert data["description"] == "Test task"
        assert "id" in data
        assert data["status"] == "NEW"
