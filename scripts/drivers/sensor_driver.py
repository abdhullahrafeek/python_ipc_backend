import time
import random

class SensorDriver:
    def __init__(self, name: str):
        self.name = name

    def start(self):
        pass
    
    def read(self):
        time.sleep(round(random.uniform(0,2), 2))
        return round(random.uniform(1,10), 2)