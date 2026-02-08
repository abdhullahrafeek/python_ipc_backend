from drivers import SensorDriver
from services import AsyncRuntime
from .device import Device

class Sensor(Device):
    def __init__(self, name: str, shared_state):
        super().__init__(name, "sensor", shared_state)
        self.sensor = SensorDriver(name)

    def _read(self):
        return self.sensor.read()
    
    async def process_output(self, reading):
        print(f"[Sensor]: Sensor reading is {reading}", flush=True)

        self.stream.update(reading)

        # payload = {
        #     "type": "sensor",
        #     "timestamp": time.time(),
        #     "data" : reading
        # }

        # shared_state.latest_sensor = json.dumps(payload)
        # print(shared_state.latest_sensor, flush=True)
        return True
    
    def close(self):
        return super().close()