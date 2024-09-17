from typing import Dict
from crawlab.exceptions import DecodeError
from crawlab.http import Request
import ujson
import re
from urllib.parse import urljoin as _urljoin
from parsel import Selector


class Response:
    def __init__(
        self,
        url: str,
        *,
        request: Request,
        headers: Dict,
        body: bytes = b"",
        status: int = 200,
    ):
        self.url = url
        self.request = request
        self.status = status
        self.headers = headers
        self.body = body
        self.encoding = request.encoding
        self.text_cache = None
        self._selector = None

    def json(self):
        return ujson.loads(self.text)

    @property
    def text(self):
        if self.text_cache:
            return self.text_cache
        try:
            self.text_cache = self.body.decode(self.encoding)
        except UnicodeDecodeError:
            try:
                _encoding = re.compile(r"charset=([\w-]+)", flags=re.I).search(
                    self.headers.get("Content-Type", "")
                    or self.headers.get("content-type", "")
                )
                if _encoding:
                    _encoding = _encoding.group(1)
                    self.text_cache = self.body.decode(_encoding)
                else:
                    raise DecodeError(f"{self.encoding} decode error")
            except UnicodeDecodeError as exec:
                raise UnicodeDecodeError(
                    exec.encoding, exec.object, exec.start, exec.end, f"{self.requests}"
                )

        return self.text_cache

    def urljoin(self, url):
        return _urljoin(self.url, url)

    def xpath(self, xpath_str):
        if not self._selector:
            self._selector = Selector(self.text)

        return self._selector.xpath(xpath_str)

    def __str__(self) -> str:
        return f"<{self.status}> {self.url}"

    @property
    def meta(self):
        return self.request.meta
