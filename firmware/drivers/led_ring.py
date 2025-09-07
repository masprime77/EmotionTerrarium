import machine
import neopixel
import time
from utilities.scale_rgb import scale_rgb

class Led_ring:
    def __init__(self, pin, pixel_count, brightness=1, auto_write=True):
        self._led = neopixel.NeoPixel(machine.Pin(pin), pixel_count)
        self._pixel_count = pixel_count
        self._brightness = brightness
        self._auto_write = auto_write
        self._frame = [(0, 0, 0)] * self._pixel_count
        self.off()

    def pixel_count(self):
        return self._pixel_count
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, value):
        if value < 0 or value > 1:
            raise ValueError("Brightness must be between 0 and 1")
        self._brightness = value

    def show(self):
        for pixel, color in enumerate(self._frame):
            self._led[pixel] = scale_rgb(color, self._brightness)
        self._led.write()

    def clear_buffer(self, show=None):
        self.set_all(0, 0, 0, show=show)

    def on(self):
        self.set_all(255, 255, 255, show=True)

    def off(self):
        self.clear_buffer(show=True)

    def toggle(self):
        for _, color in enumerate(self._frame):
            if color != (0, 0, 0):
                self.off()
                return
        self.on()

    def set_pixel(self, pixel, r, g, b, show=None):
        if pixel < 0 or pixel >= self._pixel_count:
            raise ValueError("Pixel index out of range")
        self._frame[pixel] = (r, g, b)
        show_it = self._auto_show if show is None else bool(show)
        if show_it:
            self.show()

    def set_all(self, r, g, b, show:bool):
        for pixel in range(self._pixel_count):
            self._frame[pixel] = (r, g, b)
        show_it = self._auto_show if show is None else bool(show)
        if show_it:
            self.show()

    def wheel(self, pos):
        pos = int(pos) & 255
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

