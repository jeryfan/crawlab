from asyncio import Queue
from typing import Union

from crawlab.http.request import Request
from crawlab.items.items import Item


class Processor:

    def __init__(self, crawler):
        self.queue = Queue()
        self.crawler = crawler

    async def process(self):
        while not self.done():
            o = await self.queue.get()
            if isinstance(o, Request):
                await self.crawler.engine.enqueue_request(o)
            else:
                assert isinstance(o, Item)
                await self.process_item(o)

    async def enqueue(self, output: Union[Request, Item]):
        await self.queue.put(output)
        await self.process()

    def done(self):
        return self.queue.qsize() == 0

    async def process_item(self, item: Item):
        print(item, 111)
