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
        # try:
        last_seq = {}
        while self._connected:  
            for name, stream in shared_state.get_streams().items():
                if ((stream.seq > last_seq.get(name, 0)) or 
                    (stream.seq == 0 and last_seq.get(name, 0) > 0)):

                    payload = {
                        "name": stream.name,
                        "type": stream.type,
                        "seq": stream.seq,
                        "timestamp": stream.timestamp,
                        "data": stream.data
                    }

                    await self._send(json.dumps(payload))

                    last_seq[name] = stream.seq
            await asyncio.sleep(0)

        # except asyncio.CancelledError:
        #     print(f"[WebsocketClient]: Send loop cancelled", flush=True)
        #     raise

        # except Exception as e:
        #     print(f"[WebsocketClient]: Send loop error {e}", flush=True)
        #     raise

        # finally:
        #     await self.disconnect()

    async def start_transport(self, shared_state):
        await self._connect()
        await self._sendloop(shared_state)




