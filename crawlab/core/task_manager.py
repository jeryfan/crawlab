import asyncio
from asyncio import Semaphore


class TaskManager:
    def __init__(self, concurrency=10) -> None:
        self.task_queue = set()
        self.semaphore: Semaphore = Semaphore(concurrency)

    def create_task(self, coroutine):

        task = asyncio.create_task(coroutine)
        self.task_queue.add(task)

        def done_callback(future):
            self.task_queue.remove(task)
            self.semaphore.release()

        task.add_done_callback(done_callback)
        return task

    def done(self):
        return len(self.task_queue) == 0
