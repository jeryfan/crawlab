from crawlab.http.request import Request

class Spider:
    
    def __init__(self):
        if not hasattr(self, "start_urls"):
            self.start_urls = []
            
    def start_requests(self):
        if isinstance(self.start_urls,list):
            for url in self.start_urls:
                yield Request(url=url)
        else:
            if hasattr(self,"start_url") and isinstance(self.start_url,str):
                yield Request(url=self.start_url)
            
    def parse(self, response):
        raise NotImplementedError("parse method not implemented")