import cv2

class CameraDriver:
    def __init__(self, name, index):
        self.name = name
        self.cap = cv2.VideoCapture(index)

        if not self.cap.isOpened():
            raise ConnectionError(f"Camera at index {index} is not available")
    
    def read(self):
        ret, frame = self.cap.read()

        if not ret:
            raise RuntimeError("Camera frame not available")
        
        return frame
    
    def close(self):
        self.cap.release()