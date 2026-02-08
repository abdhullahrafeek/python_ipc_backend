import time
import asyncio

class StreamState():
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
        self.data = None
        self.timestamp: float = 0.0
        self.seq: int = 0

        # self._event = asyncio.Event()

    def update(self, data):
        self.data = data
        self.timestamp = time.time()
        self.seq += 1

        # self._event.set()

    # async def get_value(self):
    #     await self._event.wait()
    #     self._event.clear()

    #     return {
    #         "name": self.name,
    #         "type": self.type,
    #         "seq": self.seq,
    #         "timestamp": self.timestamp,
    #         "data": self.data
    #     }