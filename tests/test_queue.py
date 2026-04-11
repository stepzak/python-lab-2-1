from src.task_receiver import Task
from src.task_receiver.descriptors import Status
from src.task_receiver.task_queue import TaskQueue


def test_priority_order(sample_tasks):
    queue = TaskQueue(sample_tasks)

    first = queue.pop()
    second = queue.pop()
    third = queue.pop()

    assert first.priority == 10
    assert second.priority == 5
    assert third.priority == 1
    assert len(queue) == 0


def test_heapify_in_init():
    tasks = [Task(f"T{i}", priority=i) for i in range(1, 6)]
    queue = TaskQueue(tasks)
    assert queue.pop().priority == 5


def test_push_maintains_heap(empty_queue):
    empty_queue.push(Task("Normal", priority=5))
    empty_queue.push(Task("Urgent", priority=10))
    assert empty_queue.pop().priority == 10


def test_query_filter_lazy(sample_tasks):
    queue = TaskQueue(sample_tasks)
    query = {"priority": {"min": 5}}

    results = queue.query(query)

    assert hasattr(results, "__next__")

    found_tasks = list(results)
    assert len(found_tasks) == 2
    assert all(t.priority >= 5 for t in found_tasks)


def test_query_complex_conditions():
    t1 = Task("T1", priority=10)
    t2 = Task("T2", priority=10)
    t2.status = Status.SUCCESS

    queue = TaskQueue([t1, t2])

    query = {
        "priority": {"eq": 10},
        "status": {"eq": Status.NEW}
    }

    results = list(queue.query(query))
    assert len(results) == 1
    assert results[0].description == "T1"


def test_iteration_repeatability(sample_tasks):
    queue = TaskQueue(sample_tasks)

    first_pass = [t.id for t in queue]
    second_pass = [t.id for t in queue]

    assert first_pass == second_pass
    assert len(first_pass) == 3


def test_compatibility_with_list_and_sum(sample_tasks):
    queue = TaskQueue(sample_tasks)

    assert len(queue) == 3
    assert isinstance(list(queue), list)
    assert sum(1 for t in queue if t.priority > 4) == 2