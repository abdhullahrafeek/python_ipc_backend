from websockets.asyncio.client import connect
import asyncio
import json

class WebsocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.ws = None
        self._connected = False

    async def _connect(self):
        if self._connected:
            print(f"[WebsocketClient]: Already connected to {self.uri}", flush=True)
            return
        
        self.ws = await connect(self.uri)
        self._connected = True

        print(f"[WebsocketClient]: Successfully connected to {self.uri}", flush=True)


    async def disconnect(self):
        if not self._connected:
            print(f"[WebsocketClient]: Not connected to {self.uri}", flush=True)

        await self.ws.close()
        self._connected = False

        print(f"[WebsocketClient]: Successfully disconnected from {self.uri}", flush=True)

    def isConnected(self):
        return self._connected


    async def _send(self, data):
        if not self._connected:
            print(f"[WebsocketClient]: Socket not connected", flush=True)
            return
        
        await self.ws.send(data)

    async def _sendloop(self, shared_state):
        last_seq = {}

        # streams = list(shared_state.get_streams().values())
        while self._connected:
            # tasks, _ = await asyncio.wait(
            #     [await stream.get_value() for stream in streams],
            #     return_when=asyncio.FIRST_COMPLETED
            # )

            # for task in tasks:
            #     payload = task.result()
            #     await self._send(json.dumps(payload))
                    
            for name, stream in shared_state.get_streams().items():
                # print(f"{stream.seq} \t {last_seq.get(name, 0)}")
                if stream.seq > last_seq.get(name, 0):

                    payload = {
                        "name": stream.name,
                        "type": stream.type,
                        "seq": stream.seq,
                        "timestamp": stream.timestamp,
                        "data": stream.data
                    }

                    await self._send(json.dumps(payload))

                    last_seq[name] = stream.seq

            # await asyncio.sleep(0)

            # print(shared_state.get_streams()["Sensor_01"].data ,flush=True)
            await asyncio.sleep(0)
            # await self._send(shared_state.latest_camera)
            # await self._send(shared_state.latest_sensor)
            # print(f"Sensor sent {shared_state.latest_sensor}")

    async def start_transport(self, shared_state):
        await self._connect()
        await self._sendloop(shared_state)




