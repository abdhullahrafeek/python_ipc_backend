import cv2

class CameraDriver:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def start(self):
        self.cap = cv2.VideoCapture(self.index)

        if not self.cap.isOpened():
            raise ConnectionError(f"Camera at index {self.index} is not available")
    
    def read(self):
        ret, frame = self.cap.read()

        if not ret:
            raise RuntimeError("Camera frame not available")
        
        return frame
    
    def close(self):
        self.cap.release()