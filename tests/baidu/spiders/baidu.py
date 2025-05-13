


class BaiduSpider(Spider):
    
    start_urls = ["https://www.baidu.com/"]
    
    def parse(self, response):
        
        print(response)