import asyncio
import logging
from typing import Optional

from src.task_receiver import Task
from src.task_receiver.ext.asyncio import TaskHandler

logger = logging.getLogger("AsyncExecutor")


class AsyncExecutor:
    __slots__ = ("queue", "handlers", "max_workers", "_workers", "_is_running")

    def __init__(self, max_workers: int = 3):
        self.queue = asyncio.PriorityQueue()
        self.handlers: dict[str, TaskHandler] = {}
        self.max_workers = max_workers
        self._workers: list[asyncio.Task] = []
        self._is_running = False

    def register_handler(self, handler_type: str, handler: TaskHandler):
        self.handlers[handler_type] = handler

    async def submit(self, handle_type: str, task: Task):
        await self.queue.put((task.priority, handle_type, task))
        logger.info(f"Task {task.id} was put into queue with priority {task.priority}")

    async def _worker(self):
        while self._is_running:
            try:
                try:
                    prio, h_t, task = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue

                try:
                    handler = self.handlers.get(h_t)
                    if not handler:
                        raise ValueError(f"No handler for type {h_t}")

                    task.start()
                    result = await handler.handle(task)
                    task.result = result
                    logger.info(f"Task {task.id} finished")
                except Exception as e:
                    logger.error(f"Task {task.id} failed: {e}")
                    task.exception = e
                finally:
                    self.queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.critical(f"Worker fatal error: {e}")

    async def __aenter__(self):
        self._is_running = True
        self._workers = [asyncio.create_task(self._worker()) for _ in range(self.max_workers)]
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is None:
            try:
                await asyncio.wait_for(self.queue.join(), timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Queue join timed out during exit")

        self._is_running = False
        for w in self._workers:
            w.cancel()

        await asyncio.gather(*self._workers, return_exceptions=True)
        logger.info("Executor stopped")