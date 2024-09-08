from asyncio import PriorityQueue, TimeoutError
import asyncio


class SpiderPriorityQueue(PriorityQueue):

    def __init__(self, maxsize=0) -> None:
        super().__init__(maxsize=maxsize)

    async def get(self):
        f = super().get()
        try:
            return await asyncio.wait_for(f, 0.1)
        except TimeoutError:
            return None
