import machine

class LEDBuiltin:
    def __init__(self):
        self._led = machine.Pin("LED", machine.Pin.OUT)
        self.off()

    def on(self):
        self._led.value(1)
    
    def off(self):
        self._led.value(0)

    def toggle(self):
        self._led.toggle()