import asyncio
import sys
import time
import logging

from src.task_receiver import Task
from src.task_receiver.ext.asyncio import AsyncExecutor

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class ComputeHandler:
    async def handle(self, task: Task) -> int:
        await asyncio.sleep(1)
        payload_data = task.payload.get("data", 0)
        return payload_data * 2


async def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    async with AsyncExecutor(max_workers=2) as executor:
        executor.register_handler("compute", ComputeHandler())

        tasks = [
            Task(description = "", priority=1, payload={"data": 10}),
            Task(description = "", priority=10, payload={"data": 5}),
        ]
        now = time.time()
        for t in tasks:
            await executor.submit("compute", t)

    print(f"Total: {time.time() - now}s")


if __name__ == "__main__":
    asyncio.run(main())
