import os, sys
import time


project_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_dir)
import asyncio
from baidu import BaiduSpider
from crawlab.core.engine import Engine
from crawlab.utils.project import get_settings


async def main():
    # spider = BaiduSpider()
    # engine = Engine()
    # await engine.start_spider(spider)
    settings = get_settings()
    print(settings.items())


start = time.time()
asyncio.run(main())
print(time.time() - start)
