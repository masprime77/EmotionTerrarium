import time
from drivers.led_neopixel import Led_neopixel
from controllers.ambient_controller import AmbientController

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
    return [
        ("Unknown / error", mock_weather(None, ok=False), 5),
        ("Clear", mock_weather(0), 5),
        ("Cloudy (breathing)", mock_weather(2), 5),
        ("Rain (moving drop)", mock_weather(63), 5),
        ("Snow (twinkles)", mock_weather(73), 5),
        ("Storm (flashes)", mock_weather(95), 5),
        ("Clear (cached dim)", mock_weather(0, age_s=120), 5),
    ]

def main():
    strip = Led_neopixel(pin=15, pixel_count=32, brightness=1.0, auto_write=False)
    controller = AmbientController(strip)
    while True:
        try:
            for description, weather, seconds in demo_sequence():
                print("Pattern:", description)
                t0 = time.ticks_ms()
                # Run the pattern for 'seconds'
                while time.ticks_diff(time.ticks_ms(), t0) < seconds * 1000:
                    controller.render(weather)
                    time.sleep_ms(5) # small delay to avoid busy loop for CPU

        except KeyboardInterrupt:
            break

        finally:
            strip.set_all(0, 0, 0, show=True)

if __name__ == "__main__":
    main()