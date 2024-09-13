from crawlab.spider import Spider
from crawlab import Request
from tests.baidu.items import BaiduItem


class BaiduSpider(Spider):

    custom_settings = {"CONCURRENCY": 5}

    start_urls = ["https://www.baidu.com/", "https://jd.com/"]

    async def parse(self, response):
        for i in range(10):
            yield Request("https://www.baidu.com/", callback=self.parse_detail)

    async def parse_detail(self, response):
        item = BaiduItem()
        item["url"] = "xxxxxx"
        yield item
