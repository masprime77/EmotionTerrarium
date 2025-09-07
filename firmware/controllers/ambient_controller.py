import time
import random
import math
import urandom as random
from config import COLOR_CLEAR, COLOR_CLOUDY, COLOR_RAIN_0, COLOR_RAIN_1, COLOR_SNOW_0, COLOR_SNOW_1, COLOR_STORM_0, COLOR_STORM_1, COLOR_UNKNOWN
from utilities import scale_rgb
from drivers.led_neopixel import Led_neopixel

class AmbientController:
    def __init__(self, led:Led_neopixel, brightness=1.0, rain_step_ms=60, fps=30, dimmed_if_cached=True):
        self._led = led
        self._pixel_count = led.pixel_count()
        self._led.brightness = brightness
        self._default_brightness = brightness

        fps_ms = int(1000 / fps)
        self._fps_ms = fps_ms
        self._rain_step_ms = int(rain_step_ms)

        now = time.ticks_ms()
        self._t_last_frame = now
        self._t_breathe0 = now
        self._t_rain_step = now
        self._rain_pos = 0
        
        self._dimmed_if_cached = dimmed_if_cached

    def _pat_clear(self):
        self._led.set_all(*COLOR_CLEAR, write=True)

    def _pat_cloudy(self, speed=0.004):
        difference = time.ticks_diff(time.ticks_ms(), self._t_breathe0)
        intensity = 0.825 + 0.175 * math.sin(difference * speed)
        color = scale_rgb(COLOR_CLOUDY, intensity)
        self._led.set_all(*color, write=True)

    def _pat_rain(self, tail=4):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._t_rain_step) >= self._rain_step_ms:
            self._rain_pos = (self._rain_pos + 1) % self._pixel_count
            self._t_rain_step = now

        self._led.clear_buffer(show=True)
        for i in range(self._pixel_count):
            px_distance_to_rain_px = (i - self._rain_pos) % self._pixel_count
            if px_distance_to_rain_px == 0:
                r, g, b = scale_rgb(COLOR_RAIN_1)
                self._led.set_pixel(i, r, g, b, write=False)
            elif px_distance_to_rain_px < tail:
                intensity = (tail - px_distance_to_rain_px) / tail
                r, g, b = scale_rgb(COLOR_RAIN_0, intensity)
                self._led.set_pixel(i, r, g, b, write=False)
        self._led.show()

    def _pat_snow(self, twinkle_prob=0.05):
        base = COLOR_SNOW_0
        twinkle = COLOR_SNOW_1
        self._led.set_all(*base, write=False)
        for i in range(self._pixel_count):
            if (random.randint(0, 100) / 100.0) < twinkle_prob:
                self._led.set_pixel(i, *twinkle, write=False)
        self._led.show()

    def _pat_storm(self, flash_prob=0.03):
        do_flash = (random.randint(0, 100) / 100.0) < flash_prob
        color = COLOR_STORM_1 if do_flash else COLOR_STORM_0
        self._led.set_all(*color, write=True)

    def _pat_unknown(self):
        self._led.set_all(COLOR_UNKNOWN, write=True)

    def render(self, weather):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.t_last_frame) < self.fps_ms:
            if weather.get("wmo") not in (61, 63, 65):
                return
        self._t_last_frame = now

        ok  = weather.get("ok", False)
        wmo = weather.get("wmo")
        age = weather.get("age_s", 0)

        if self._dimmed_if_cached:
            self._led.brightness = 0.8 if (age and age > 0) else self._default_brightness

        if not ok or wmo is None:
            self._pat_unknown()
        elif wmo in (0, 1):
            self._pat_clear()
        elif wmo in (2, 3):
            self._pat_cloudy()
        elif wmo in (61, 63, 65):
            self._pat_rain()
        elif wmo in (71, 73, 75):
            self._pat_snow()
        elif wmo in (95, 96, 99):
            self._pat_storm()
        else:
            self._pat_unknown()
    