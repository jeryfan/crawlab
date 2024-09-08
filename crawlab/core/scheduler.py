from typing import Optional
from crawlab.utils.pqueue import SpiderPriorityQueue


class Scheduler:

    def __init__(self):
        self.request_queue: Optional[SpiderPriorityQueue] = None

    def open(self):
        self.request_queue = SpiderPriorityQueue()

    async def next_request(self):
        return await self.request_queue.get()

    async def enqueue_request(self, request):
        await self.request_queue.put(request)

    def __len__(self):
        return self.request_queue.qsize()

    def done(self):
        return len(self) == 0
