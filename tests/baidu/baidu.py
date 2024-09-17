from crawlab.http.response import Response
from crawlab.spider import Spider
from crawlab import Request
from tests.baidu.items import BaiduItem


class BaiduSpider(Spider):

    custom_settings = {"CONCURRENCY": 5}

    start_urls = ["https://www.baidu.com111/", "https://jd.com/"]

    async def parse(self, response):
        for i in range(10):
            yield Request(response.url, callback=self.parse_detail, meta="xxx")

    async def parse_detail(self, response: Response):
        item = BaiduItem()
        item["url"] = response.meta
        yield item
