import time

class Blink:
    def blink(self, times:int=1, duration:float=0.5) -> None:
        for _ in range(times):
            self.on()
            time.sleep(duration)
            self.off()
            time.sleep(duration)
