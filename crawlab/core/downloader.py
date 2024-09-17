import asyncio
from typing import Final, Optional, Set, final

from flask import request, session
from crawlab import Request
import requests
from contextlib import asynccontextmanager
from aiohttp import (
    ClientSession,
    BaseConnector,
    TCPConnector,
    ClientTimeout,
    ClientResponse,
    TraceConfig,
)
from crawlab.http.response import Response
from crawlab.utils.log import get_logger


class RequestManager:

    def __init__(self) -> None:
        self._active: Final[Set] = set()

    def add(self, request: Request):
        self._active.add(request)

    def remove(self, request: Request):
        self._active.remove(request)

    @asynccontextmanager
    async def __call__(self, request: Request):

        try:
            yield self.add(request)
        finally:
            self.remove(request)

    def __len__(self) -> int:
        return len(self._active)


class Downloader:

    def __init__(self, crawler):
        self._active = RequestManager()
        self.crawler = crawler
        self.connector: Optional[BaseConnector] = None
        self.session: Optional[ClientSession] = None
        self._verify_ssl: Optional[bool] = None
        self._timeout: Optional[ClientTimeout] = None
        self._use_session: Optional[bool] = None
        self.logger = get_logger(
            self.__class__.__name__, level=crawler.settings.getint("LOG_LEVEL")
        )
        self.request_method = {"get": self._get, "post": self._post}

    def open(self):
        self.logger.info(
            f"{self.crawler.spider} <downloader class:{type(self).__name__}>"
            f"<concurrency: {self.crawler.settings.getint('CONCURRENCY')}>"
        )
        self._verify_ssl = self.crawler.settings.getbool("VERIFY_SSL")
        self._timeout = ClientTimeout(
            total=self.crawler.settings.getint("REQUEST_TIMEOUT")
        )
        self._use_session = self.crawler.settings.getbool("USE_SESSION")
        if self._use_session:
            self.connector = TCPConnector(ssl=self._verify_ssl)
            trace_config = TraceConfig()
            trace_config.on_request_start.append(self.on_request_start)
            self.session = ClientSession(
                connector=self.connector,
                timeout=self._timeout,
                trace_configs=[trace_config],
            )

    async def fetch(self, request: Request):
        async with self._active(request):
            response = await self.download(request)
            return response

    async def download(self, request: Request) -> Response:
        try:
            if self._use_session:
                response = await self.send_request(self.session, request)
                return response
            else:
                connector = TCPConnector(verify_ssl=self._verify_ssl)
                trace_config = TraceConfig()
                trace_config.on_request_start.append(self.on_request_start)
                async with ClientSession(
                    connector=connector,
                    timeout=self._timeout,
                    trace_configs=[trace_config],
                ) as session:
                    response = await self.send_request(session, request)
                    return response
        except Exception as exec:
            self.logger.error(f"ERROR during request: {exec}")
            raise exec

    async def send_request(self, session, request: Request) -> ClientResponse:
        response = await self.request_method[request.method.lower()](session, request)
        body = await response.content.read()

        return self.structure_request(request, response, body)

    @staticmethod
    def structure_request(request: Request, response, body) -> Response:
        return Response(
            url=request.url,
            status=response.status,
            headers=dict(response.headers),
            body=body,
            request=request,
        )

    async def _get(self, session, request: Request):
        response = await session.get(
            request.url,
            headers=request.headers,
            cookies=request.cookies,
            proxy=request.proxy,
        )
        return response

    async def _post(self, session, request: Request):
        response = await session.post(
            request.url,
            data=request.body,
            headers=request.headers,
            cookies=request.cookies,
            proxy=request.proxy,
        )
        return response

    def __len__(self):
        return len(self._active)

    def done(self):
        return len(self) == 0

    async def on_request_start(self, session, trace_config_ctx, params):
        self.logger.info(f"request download: {params.url},method:{params.method}")

    async def close(self):
        if self.connector:
            self.connector.close()
        if self.session:
            await self.session.close()
