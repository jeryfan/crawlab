import asyncio
from typing import Final, Type
from crawlab.core.engine import Engine
from crawlab.settings.setting_manager import SettingManager
from crawlab.spider import Spider
from crawlab.utils.project import update_settings


class Crawler:

    def __init__(self, spider_cls: Type[Spider], settings: SettingManager):
        self.engine = None
        self.spider_cls = spider_cls
        self.settings = settings.copy()

    async def crawl(self):

        self.spider = self.create_spider()
        self.engine = self.create_engine()
        await self.engine.start_spider(self.spider)

    def create_engine(self):
        return Engine(self)

    def create_spider(self):
        spider = self.spider_cls.create_instance(self)
        self._set_spider(spider)
        return spider

    def _set_spider(self, spider):
        update_settings(spider, self.settings)


class CrawlerProcess:

    def __init__(self, settings):
        self.settings = settings
        self.task_queue = set()

    async def crawl(self, spider_cls: Type[Spider]):
        crawler = self._create_crawler(spider_cls)
        task = await self._crawl(crawler)
        self.task_queue.add(task)

    async def _crawl(self, crawler: Crawler):
        return asyncio.create_task(crawler.crawl())

    async def start(self):
        await asyncio.gather(*self.task_queue)

    def _create_crawler(self, spider_cls: Type[Spider]):
        if isinstance(spider_cls, str):
            raise ValueError("CrawlerProcess can only accept spider classes.")
        crawler = Crawler(spider_cls, self.settings)
        return crawler
