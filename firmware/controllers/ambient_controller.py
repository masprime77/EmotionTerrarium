import time
import random
import math
from config import COLOR_CLEAR, COLOR_CLOUDY, COLOR_RAIN_0, COLOR_RAIN_1, COLOR_SNOW_0, COLOR_SNOW_1, COLOR_STORM_0, COLOR_STORM_1, COLOR_UNKNOWN
from config import COLOR_ON, COLOR_OFF
from utilities.scale_rgb import scale_rgb
from drivers.led_neopixel import LedNeopixel

class AmbientController:
    def __init__(self, led:LedNeopixel, brightness=1.0, cloud_speed_s=1.0, fps=24, dimmed_if_cached=True):
        self._led = led
        self._pixel_count = led.pixel_count()
        self._led.brightness = brightness
        self._default_brightness = brightness   

        fps_ms = int(1000 / fps)
        self._default_fps_ms = fps_ms
        self._fps_ms = fps_ms
        self._cloud_speed_ms = int(cloud_speed_s * 1000)

        now = time.ticks_ms()
        self._t_last_frame = now
        self._t_cloud_step = now
        self._cloud_pos = 0
        
        self._dimmed_if_cached = dimmed_if_cached

    def _pat_clear(self):
        self._led.set_all(*COLOR_CLEAR, show=True)

    def _pat_cloudy(self, clouds=3, visibility=0.75):
        cloudy = scale_rgb(COLOR_CLOUDY, visibility)
        now = time.ticks_ms()
        if time.ticks_diff(now, self._t_cloud_step) >= self._cloud_speed_ms:
            self._cloud_pos = (self._cloud_pos + 1) % self._pixel_count
            self._t_cloud_step = now

        self._led.set_all(*cloudy, show=False)
        for i in range(self._pixel_count):
            px_distance_to_cloud_px = (i - self._cloud_pos) % self._pixel_count
            if px_distance_to_cloud_px == 0:
                span = self._pixel_count // clouds
                for k in range(clouds):
                    span_n = k * span
                    for j in range(8):  # cloud size
                        self._led.set_pixel((i + j + span_n) % self._pixel_count, *COLOR_OFF, show=False)
                break
        self._led.show()

    def _pat_rain(self, rain_speed_ms=50, drops=4):
        base =  COLOR_RAIN_0
        rain = COLOR_RAIN_1
        
        self._led.set_all(*base, show=True)
        now = time.ticks_ms()

        while True:
            pixels = list(range(self._pixel_count))
            for i in range(len(pixels) - 1, 0, -1):
                j = random.randrange(i + 1)
                pixels[i], pixels[j] = pixels[j], pixels[i]

            for i in pixels[:drops]:
                self._led.set_pixel(i, *rain, show=False)
            self._led.show()

            if time.ticks_diff(time.ticks_ms(), now) > self._fps_ms:
                break
            time.sleep_ms(rain_speed_ms)

    def _pat_snow(self, snow_speed_ms=300, snow_flakes=2):
        base = COLOR_SNOW_0
        rain = COLOR_SNOW_1
        
        self._led.set_all(*base, show=True)
        now = time.ticks_ms()

        while True:
            pixels = list(range(self._pixel_count))
            for i in range(len(pixels) - 1, 0, -1):
                j = random.randrange(i + 1)
                pixels[i], pixels[j] = pixels[j], pixels[i]

            for i in pixels[:snow_flakes]:
                self._led.set_pixel(i, *rain, show=False)
            self._led.show()

            if time.ticks_diff(time.ticks_ms(), now) > self._fps_ms:
                break
            time.sleep_ms(snow_speed_ms)

    def _pat_storm(self, flash_prob=0.03):
        do_flash = (random.randint(0, 100) / 100.0) < flash_prob
        color = COLOR_STORM_1 if do_flash else COLOR_STORM_0
        self._led.set_all(*color, show=True)

    def _pat_unknown(self):
        self._led.set_all(*COLOR_UNKNOWN, show=True)

    def render(self, weather):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._t_last_frame) < self._fps_ms:
            return
        self._t_last_frame = now

        ok  = weather.get("ok", False)
        wmo = weather.get("wmo")
        age = weather.get("age_s", 0)

        if self._dimmed_if_cached:
            self._led.brightness = 0.8 if (age and age > 0) else self._default_brightness

        if not ok or wmo is None:
            self._pat_unknown()
        elif wmo == 0:
            self._pat_clear()
        elif wmo in (1, 2, 3, 45, 48):
            self._pat_cloudy()
        elif wmo in (61, 63, 65):
            self._pat_rain()
        elif wmo in (71, 73, 75):
            self._pat_snow()
        elif wmo in (95, 96, 99):
            self._pat_storm()
        else:
            self._pat_unknown()
    