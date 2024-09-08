import asyncio
from crawlab import Request
import requests


class Downloader:

    def __init__(self):
        self._active = set()

    async def fetch(self, request: Request):
        self._active.add(request)
        response = await self.download(request)
        self._active.remove(request)
        return response

    async def download(self, request: Request):
        # resp = requests.get(request.url)
        # print(resp.status_code)
        # return resp
        await asyncio.sleep(1)

    def __len__(self):
        return len(self._active)

    def done(self):
        return len(self) == 0
