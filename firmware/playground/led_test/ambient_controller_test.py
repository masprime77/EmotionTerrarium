# tests/test_ambient_m3.py
# Run this on the Pico W.
# Press Ctrl+C to stop; LEDs will be cleared on exit.

import time
from drivers.led_ring import LedRing
from controllers.ambient_controller import AmbientController

def W(wmo, *, ok=True, age_s=0):
    """Build a canonical M2 weather dict minimal for the controller."""
    return {
        "ok": ok,
        "wmo": wmo,
        "label": "",
        "temp": None,
        "humidity": None,
        "time": None,
        "source": "fake",
        "age_s": age_s,
    }

def demo_sequence():
    """
    Sequence of (description, weather dict, duration seconds).
    Includes a cached variant to verify the 20% dim behavior.
    """
    return [
        ("Unknown / error", W(None, ok=False), 4),
        ("Clear",           W(0),              4),
        ("Cloudy (breathing)", W(2),           6),
        ("Rain (moving drop)", W(63),          6),
        ("Snow (twinkles)", W(73),             6),
        ("Storm (flashes)", W(95),             6),
        ("Clear (cached dim)", W(0, age_s=120), 4),
    ]

def main():
    # Adjust pin/count to your hardware
    ring = LedRing(pin=16, count=32, brightness=1.0, auto_write=False)
    ctl  = AmbientController(ring, max_brightness=1.0,
                             rain_step_ms=60,  # raindrop speed
                             fps=30)        # target frame time for other patterns

    try:
        while True:
            for desc, weather, seconds in demo_sequence():
                print("Pattern:", desc)
                t0 = time.ticks_ms()
                # Run the pattern for 'seconds'
                while time.ticks_diff(time.ticks_ms(), t0) < seconds * 1000:
                    ctl.render(weather)     # non-blocking step
                    time.sleep_ms(40)       # ~25 FPS main loop pacing

    except KeyboardInterrupt:
        pass
    finally:
        # Ensure LEDs are turned off on exit
        ring.set_all(0, 0, 0, write=True)

if __name__ == "__main__":
    main()