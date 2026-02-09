from drivers import CameraDriver
import cv2
import base64
import asyncio
from state import SharedState

from .device import Device

import threading


class Camera(Device):
    def __init__(self, name: str, shared_state: SharedState, index=0):
        self.camera = CameraDriver(name, index)
        super().__init__(name, "camera", shared_state)

        self._reading_completed = threading.Event()

    def _read(self):
        self._reading_completed.clear()
        result = self.camera.read()
        self._reading_completed.set()
        return result

    async def process_output(self, frame):
        cv2.imshow("Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        

        _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

        jpg_base64 = base64.b64encode(buffer).decode("utf-8")

        self.stream.update(jpg_base64)
        await asyncio.sleep(0)
        return True
    
    def close(self):
        print(f"[Camera]: Waiting for reading to complete", flush=True)
        self._reading_completed.wait()
        print(f"[Camera]: Reading completed. Closing camera", flush=True)
        self.camera.close()
        print(f"[Camera]: Camera closed", flush=True)
        cv2.destroyAllWindows()

    def _start(self):
        self.camera.start()