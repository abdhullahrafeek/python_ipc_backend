from websockets.asyncio.client import connect
import asyncio
import json

TIME_OUT_SEC = 1
MAX_RETRY_TIMES = 10

class WebsocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.ws = None
        self._connected = False

    async def _connect(self):
        if self._connected:
            print(f"[WebsocketClient]: Already connected to {self.uri}", flush=True)
            return
        
        retry_attempt = 1

        while retry_attempt <= MAX_RETRY_TIMES:
            try:
                self.ws = await connect(self.uri)
                self._connected = True

                print(f"[WebsocketClient]: Successfully connected to {self.uri}", flush=True)
                return

            except ConnectionRefusedError:
                print(f"[WebsocketClient]: Connection refused. Retrying {retry_attempt}.....")
                retry_attempt += 1
                continue
        
        print(f"[WebsocketClient]: Could not connect.")


    async def disconnect(self):
        if not self._connected:
            print(f"[WebsocketClient]: Not connected to {self.uri}", flush=True)
            return

        await self.ws.close()
        self._connected = False

        print(f"[WebsocketClient]: Successfully disconnected from {self.uri}", flush=True)

    def isConnected(self):
        return self._connected


    async def _send(self, data):
        if not self._connected:
            print(f"[WebsocketClient]: Socket not connected", flush=True)
            return
        
        try:
            await self.ws.send(data)

        except Exception as e:
            self._connected = False
            print(e)
            print("[WebsocketClient]: Connection failed. Trying to reconnect.")
            await self._connect()

    async def _sendloop(self, shared_state):
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

    async def start_transport(self, shared_state):
        await self._connect()
        await self._sendloop(shared_state)




