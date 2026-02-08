import asyncio
from services import AsyncRuntime, AsyncSystem
from devices import Camera, Sensor
from state import SharedState

from transport import WebsocketClient
 
async def main():

    shared_state = SharedState()
    websocket_client = WebsocketClient("ws://localhost:8765/")
    
    AsyncSystem.register_device(Sensor("Sensor_01", shared_state))
    AsyncSystem.register_device(Camera("Camera_01",shared_state, 0))

    try:
        await asyncio.gather(
            asyncio.create_task(websocket_client.start_transport(shared_state)),
            asyncio.create_task(AsyncSystem.start())
        )


    finally:
        await AsyncSystem.stop()
        await websocket_client.disconnect()
        AsyncRuntime.close()

if __name__ == "__main__":
    asyncio.run(main())