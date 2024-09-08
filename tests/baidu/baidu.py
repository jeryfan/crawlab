from crawlab.spider import Spider
from crawlab import Request


class BaiduSpider(Spider):

    start_urls = ["https://www.baidu.com/", "https://jd.com/"]

    async def parse(self, response):
        print(111)
        for i in range(10):
            yield Request("https://www.baidu.com/", callback=self.parse_detail)

    async def parse_detail(self, response):
        print(222)
