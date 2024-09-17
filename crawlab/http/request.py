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
        encoding="utf-8",
        meta: Optional[Dict] = None,
    ) -> None:
        self.url = url
        self.method = method
        self.headers = headers
        self.priority = priority
        self.cookies = cookies
        self.proxy = proxy
        self.body = body
        self.callback = callback
        self.encoding = encoding
        self._meta = meta if meta is not None else {}

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return f"{self.url} {self.method}"

    @property
    def meta(self):
        return self._meta
