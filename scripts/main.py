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

    system_task = asyncio.create_task(AsyncSystem.start())
    transport_task = asyncio.create_task(websocket_client.start_transport(shared_state))

    try:
        await asyncio.gather(
            system_task,
            transport_task
        )

    except asyncio.CancelledError:
        print(f"[main]: Asyncio gather cancelled", flush=True)
        raise


    finally:
        system_task.cancel()
        transport_task.cancel()
        await AsyncSystem.stop()
        await websocket_client.disconnect()
        AsyncRuntime.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print(f"[main]: Shutting down", flush=True)