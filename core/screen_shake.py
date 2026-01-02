import random

class ScreenShake:
    def __init__(self):
        self.intensity = 0
    def start(self,intensity=5):
        self.intensity = intensity
    def update(self):
        if self.intensity > 0:
            self.intensity -= 1
            return random.randint(-self.intensity,self.intensity) , 0
        return 0,0