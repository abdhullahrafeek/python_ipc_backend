import asyncio

class AsyncSystem:

    devices = []
    tasks = []
    stop_event = asyncio.Event()
    
    @classmethod
    def register_device(cls, device):
        cls.devices.append(device)

    @classmethod
    async def start(cls):
        for device in cls.devices:
            cls.tasks.append(asyncio.create_task(cls._run_device(device)))

        # cls.tasks.append(asyncio.create_task(cls._start_transport(ws, shared_state)))

        await asyncio.gather(*cls.tasks)

    @classmethod
    async def stop(cls):
        cls.stop_event.set()

        for task in cls.tasks:
            task.cancel()
        
        await asyncio.gather(*cls.tasks, return_exceptions=True)


    @classmethod
    async def _run_device(cls, device):
        try:
            async for data in device:
                output = await device.process_output(data)

                if not output or cls.stop_event.is_set():
                    break
        finally:
            if hasattr(device, "close"):
                device.close()
