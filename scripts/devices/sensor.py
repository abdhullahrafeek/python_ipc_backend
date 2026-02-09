from drivers import SensorDriver
from services import AsyncRuntime
from .device import Device

class Sensor(Device):
    def __init__(self, name: str, shared_state):
        self.sensor = SensorDriver(name)
        super().__init__(name, "sensor", shared_state)

    def _read(self):
        return self.sensor.read()
    
    async def process_output(self, reading):
        print(f"[Sensor]: Sensor reading is {reading}", flush=True)

        self.stream.update(reading)
        return True
    
    def close(self):
        return super().close()
    
    def _start(self):
        self.sensor.start()