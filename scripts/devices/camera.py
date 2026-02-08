from drivers import CameraDriver
from services import AsyncRuntime
import cv2
import base64
import asyncio
from state import SharedState

from .device import Device


class Camera(Device):
    def __init__(self, name: str, shared_state: SharedState, index=0):
        super().__init__(name, "camera", shared_state)
        self.camera = CameraDriver(name, index)

    def _read(self):
        return self.camera.read()

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
        cv2.destroyAllWindows()
        self.camera.close()

        print("[Camera]: Camera closed")