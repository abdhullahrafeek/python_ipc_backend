from .async_system import AsyncSystem
from concurrent.futures import ThreadPoolExecutor

import asyncio

class AsyncRuntime:
    executor = ThreadPoolExecutor(max_workers=2)

    @classmethod
    async def run_in_executor(cls, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(cls.executor, lambda: func(*args, **kwargs))


    @classmethod
    def close(cls):
        cls.executor.shutdown(wait=True)
        print("[AsyncRuntime]: AsyncRuntime closed")
