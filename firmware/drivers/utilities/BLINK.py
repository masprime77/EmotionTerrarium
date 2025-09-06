import time
from abc import ABC, abstractmethod

class Blink(ABC):
    def blink(self, times:int=1, duration:float=0.5) -> None:
        for _ in range(times):
            self.on()
            time.sleep(duration)
            self.off()
            time.sleep(duration)
