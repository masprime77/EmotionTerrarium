class EmotionController:
    def __init__(self, led, brightness=1.0):
        self._led = led
        self._led.brightness = brightness
        self._led.off()

    def render_color(self, color):
        self._led.set_all(*color, show=True)

    def off(self):
        self._led.off()