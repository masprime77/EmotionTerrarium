import time
from drivers.led_neopixel import LedNeopixel
from controllers.ambient_controller import AmbientController
from config import PIN_OVERHEAD_LED, PIXEL_COUNT_OVERHEAD, BRIGHTNESS_OVERHEAD_LED
from config import COLOR_OFF

def mock_weather(wmo, ok=True, age_s=0):
    return {
        "ok": ok,
        "wmo": wmo,
        "label": "",
        "temp": None,
        "humidity": None,
        "time": None,
        "source": "MOCK",
        "age_s": age_s,
    }

def demo_sequence():
    time_s = 3
    return [
        ("Unknown / error", mock_weather(None, ok=False), time_s),
        ("Clear", mock_weather(0), time_s),
        ("Cloudy (moving cloud)", mock_weather(1), time_s),
        ("Rain (drops)", mock_weather(63), time_s),
        ("Snow (twinkles)", mock_weather(73), time_s),
        ("Storm (flashes)", mock_weather(95), time_s),
        ("Clear (cached dim)", mock_weather(0, age_s=120), time_s),
    ]

def main():
    strip = LedNeopixel(pin=PIN_OVERHEAD_LED, pixel_count=PIXEL_COUNT_OVERHEAD, brightness=BRIGHTNESS_OVERHEAD_LED, auto_show=False)
    controller = AmbientController(strip, brightness=BRIGHTNESS_OVERHEAD_LED, dimmed_if_cached=True)

    print("[Test M3] Ambient LED controller demo")
    
    try:
        for description, weather, seconds in demo_sequence():
            print("Pattern:", description)
            t0 = time.ticks_ms()

            while time.ticks_diff(time.ticks_ms(), t0) < seconds * 1000:
                controller.render(weather)
                time.sleep_ms(10)

        print("Demo completed.")
        print("[Test M3] Done.\n")

    except KeyboardInterrupt:
        print("Demo interrupted by user")
        print("[Test M3] Done.\n")


    finally:
        strip.set_all(*COLOR_OFF, show=True)

if __name__ == "__main__":
    main()