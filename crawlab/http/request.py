

class Request:
    
    def __init__(self, url, *, method='GET', headers={}, body='', priority=0,callback=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.priority = priority
        self.callback = callback
        
    def __lt__(self, other):
        return self.priority < other.priority