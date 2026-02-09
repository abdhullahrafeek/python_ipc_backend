from drivers import CameraDriver
import cv2
import base64
import asyncio
from state import SharedState

from .device import Device

import threading


class Camera(Device):
    def __init__(self, name: str, shared_state: SharedState, index=0):
        self._reading_completed = threading.Event()
        self._stop_called = threading.Event()

        self.camera = CameraDriver(name, index)
        super().__init__(name, "camera", shared_state)


    def _read(self):
        if self._stop_called.is_set():
            return None
        
        self._reading_completed.clear()
        
        try:
            return self.camera.read()
        
        finally:
            self._reading_completed.set()
        

    async def process_output(self, frame):
        if frame is None:
            return False
        cv2.imshow("Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        

        _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

        jpg_base64 = base64.b64encode(buffer).decode("utf-8")

        self.stream.update(jpg_base64)
        await asyncio.sleep(0)
        return True
    
    def close(self):
        self._stop_called.set()
        print(f"[Camera]: Waiting for reading to complete", flush=True)
        self._reading_completed.wait()
        print(f"[Camera]: Reading completed. Closing camera", flush=True)
        self.camera.close()
        print(f"[Camera]: Camera closed", flush=True)
        cv2.destroyAllWindows()

    def _start(self):
        self._stop_called.clear()
        self.camera.start()