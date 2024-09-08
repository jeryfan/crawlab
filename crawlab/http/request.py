from typing import Callable, Dict, Optional


class Request:

    def __init__(
        self,
        url: str,
        *,
        method: str = "GET",
        callback: Optional[Callable] = None,
        headers: Optional[Dict] = None,
        priority: int = 0,
        cookies: Optional[Dict] = None,
        proxy: Optional[Dict] = None,
        body="",
    ) -> None:
        self.url = url
        self.method = method
        self.headers = headers
        self.priority = priority
        self.cookies = cookies
        self.proxy = proxy
        self.body = body
        self.callback = callback

    def __lt__(self, other):
        return self.priority < other.priority
