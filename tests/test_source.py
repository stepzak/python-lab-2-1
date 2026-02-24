import pytest
from src.constants import TASKS_FILE
from src.consumer import consumer
from src.sources import FileSource, GeneratorSource

@pytest.mark.parametrize(
    "source_cls, args, err",
    [
        (FileSource, (TASKS_FILE,), None),
        (GeneratorSource, (5,), None),
        (int, (1,), TypeError),
    ]
)
def test_source(source_cls, args, err):
    source = source_cls(*args)
    if not err:
        tasks = []
        for task in source.get_tasks():
            tasks.append(task)

        new_source = source_cls(*args)
        ret = consumer(new_source)
        assert ret == tasks
    else:
        with pytest.raises(TypeError):
            consumer(source)
