import time
import random
import math
import urandom as random
from config import COLOR_CLEAR, COLOR_CLOUDY, COLOR_RAIN_0, COLOR_RAIN_1, COLOR_SNOW_0, COLOR_SNOW_1, COLOR_STORM_0, COLOR_STORM_1, COLOR_UNKNOWN
from utilities import scale_rgb

class AmbientController:
    def __init__(self, led, max_brightness=1.0, rain_step_ms=60, fps=30):
        self.led = led
        # self.led.brightness(max_brightness)
        self._pixel_count = led.count()
        fps_ms = int(1000 / fps)
        self.fps_ms = fps_ms

        now = time.ticks_ms()
        self._t_last_frame = now
        self._t_breathe0   = now # cloudy breathing phase
        self._rain_pos     = 0 # rain head index
        self._rain_step_ms = int(rain_step_ms)

        self._frame = [(0,0,0)] * self._n

    def _pat_clear(self, dim_k=1.0):
        self.ring.set_all(*scale_rgb(COLOR_CLEAR, dim_k), write=True)

    def _pat_cloudy(self, dim_k=1.0):
        # breathing on soft blue
        dt = time.ticks_diff(time.ticks_ms(), self.t_breathe0)
        k = 0.825 + 0.175 * math.sin(dt * 0.004)  # ~[0.65..1.0]
        c = scale_rgb(COLOR_CLOUDY, k * dim_k)
        self.ring.set_all(*c, write=True)

    def _pat_rain(self, dim_k=1.0):
        # move head every rain_step_ms
        now = time.ticks_ms()
        if time.ticks_diff(now, self.t_rain_step) >= self.rain_step_ms:
            self.rain_pos = (self.rain_pos + 1) % self.n
            self.t_rain_step = now

        # clear, then draw head + fading tail
        self.ring.set_all(0, 0, 0, write=False)
        tail = 4
        for i in range(self.n):
            d = (i - self.rain_pos) % self.n
            if d == 0:
                r, g, b = scale_rgb(COLOR_RAIN_1, dim_k)
                self.ring.set_pixel(i, r, g, b, write=False)
            elif d < tail:
                k = (tail - d) / tail
                r, g, b = scale_rgb(COLOR_RAIN_0, k * dim_k)
                self.ring.set_pixel(i, r, g, b, write=False)
        self.ring.show()

    def _pat_snow(self, dim_k=1.0, twinkle_prob=0.05):
        # cold base + random one-frame twinkles
        base = scale_rgb(COLOR_SNOW_0, dim_k)
        twk  = scale_rgb(COLOR_SNOW_1, dim_k)
        self.ring.set_all(*base, write=False)
        threshold = int(255 * twinkle_prob)
        for i in range(self.n):
            if (random.getrandbits(8) & 0xFF) < threshold:
                self.ring.set_pixel(i, *twk, write=False)
        self.ring.show()

    def _pat_storm(self, dim_k=1.0, flash_prob=0.03):
        do_flash = (random.getrandbits(8) & 0xFF) < int(255 * flash_prob)
        c = COLOR_STORM_1 if do_flash else COLOR_STORM_0
        self.ring.set_all(*scale_rgb(c, dim_k), write=True)

    def _pat_unknown(self, dim_k=1.0):
        self.ring.set_all(*scale_rgb(COLOR_UNKNOWN, dim_k), write=True)

    # --------- public render step ---------
    def render(self, weather):
        """
        Non-blocking render step. Call this every loop iteration.
        """
        # simple frame pacing (skip if too soon for non-rain patterns)
        now = time.ticks_ms()
        if time.ticks_diff(now, self.t_last_frame) < self.fps_ms:
            # rain self-clocks via rain_step_ms; others can skip
            if weather.get("wmo") not in (61, 63, 65):
                return
        self.t_last_frame = now

        ok  = weather.get("ok", False)
        wmo = weather.get("wmo")
        age = weather.get("age_s", 0)

        # dim 20% if data is cached
        dim_k = 0.8 if (age and age > 0) else 1.0

        if not ok or wmo is None:
            self._pat_unknown(dim_k)
        elif wmo in (0, 1):
            self._pat_clear(dim_k)
        elif wmo in (2, 3):
            self._pat_cloudy(dim_k)
        elif wmo in (61, 63, 65):
            self._pat_rain(dim_k)
        elif wmo in (71, 73, 75):
            self._pat_snow(dim_k)
        elif wmo in (95, 96, 99):
            self._pat_storm(dim_k)
        else:
            self._pat_unknown(dim_k)
    