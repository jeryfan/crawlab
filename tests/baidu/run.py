import os, sys
import time

import os, sys

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.dirname(project_dir)
print(project_dir)
sys.path.append(project_dir)

from crawlab.crawler import CrawlerProcess


project_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_dir)
import asyncio
from baidu import BaiduSpider
from crawlab.core.engine import Engine
from crawlab.utils.project import get_settings


async def main():
    crawlerProcess = CrawlerProcess(settings=get_settings())
    await crawlerProcess.crawl(BaiduSpider)
    await crawlerProcess.start()


start = time.time()
asyncio.run(main())
print(time.time() - start)
