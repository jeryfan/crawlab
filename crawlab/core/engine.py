import asyncio
from inspect import iscoroutine
from typing import Generator, Optional
from crawlab.core.downloader import Downloader
from crawlab.core.processor import Processor
from crawlab.core.scheduler import Scheduler
from crawlab.core.task_manager import TaskManager

# from crawlab.crawler import Crawler
from crawlab.items.items import Item
from crawlab.spider import Spider
from crawlab import Request
from crawlab.utils.spider import transform


class Engine:

    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = self.crawler.settings
        self.downloader: Optional[Downloader] = None
        self.scheduler: Optional[Scheduler] = None
        self.processor: Optional[Processor] = None
        self.task_manager: TaskManager = TaskManager(
            self.settings.getint("CONCURRENCY")
        )
        self.start_requests: Optional[Generator] = None
        self.spider: Optional[Spider] = None
        self.running = False

    async def start_spider(self, spider: Spider):
        self.running = True
        self.spider = spider
        self.downloader = Downloader()
        self.scheduler = Scheduler()
        self.processor = Processor(self.crawler)
        if hasattr(self.scheduler, "open"):
            self.scheduler.open()
        self.start_requests = iter(spider.start_requests())
        await self.open_spider()

    async def open_spider(self):
        crawling = asyncio.create_task(self.crawl())
        await crawling

    async def crawl(self):
        while self.running:
            if request := await self.get_next_request():
                await self._crawl(request)
            try:
                start_request = next(self.start_requests)
            except StopIteration:
                self.start_requests = None
            except Exception as e:
                if await self._exit():
                    self.running = False

                if not self.running:
                    break
            else:
                # enqueue request
                await self.enqueue_request(start_request)

    async def _crawl(self, request: Request):
        async def crawl_task():
            outputs = await self._fetch(request)
            if outputs:
                await self._handle_spider_output(outputs)

        await self.task_manager.semaphore.acquire()
        self.task_manager.create_task(crawl_task())

    async def _fetch(self, request: Request):
        async def _success(_response):
            callback = request.callback or self.spider.parse
            if _output := callback(_response):
                if iscoroutine(_output):
                    await _output
                else:
                    return transform(_output)

        _response = await self.downloader.fetch(request)
        return await _success(_response)

    async def enqueue_request(self, request: Request):
        await self._schedule_request(request)

    async def _schedule_request(self, request: Request):
        await self.scheduler.enqueue_request(request)

    async def get_next_request(self):
        return await self.scheduler.next_request()

    async def _handle_spider_output(self, outputs):
        async for output in outputs:
            if isinstance(output, (Request, Item)):
                await self.processor.enqueue(output)

    async def _exit(self):
        if (
            self.scheduler.done()
            and self.downloader.done()
            and self.task_manager.done()
            and self.processor.done()
        ):
            return True
        return False
