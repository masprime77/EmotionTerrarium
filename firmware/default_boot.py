import time
from drivers.led_builtin import LedBuiltin
from drivers.led_neopixel import LedNeopixel
from config import PIN_LED_RING, PIXEL_COUNT_RING, PIN_OVERHEAD_LED, PIXEL_COUNT_OVERHEAD
from config import COLOR_RED, COLOR_GREEN, COLOR_BLUE
from config import COLOR_ON, COLOR_OFF

def main():
    builtin = LedBuiltin()
    print("[BOOT] Built-in LED ON")
    builtin.blink(5, 0.5)
    builtin.off()

    ring = {
        "name": "Ring",
        "light": LedNeopixel(pin=PIN_LED_RING, pixel_count=PIXEL_COUNT_RING,auto_write=True)
    }

    overhead = {
        "name": "Overhead",
        "light": LedNeopixel(pin=PIN_OVERHEAD_LED, pixel_count=PIXEL_COUNT_OVERHEAD, auto_write=True)
    }

    rgb_lights = [ring, overhead]

    for light in rgb_lights:
        light["light"].off()

    for light in rgb_lights:
        print(f"[BOOT] {light["name"]} LED: RED")
        light["light"].set_all(*COLOR_RED)
        time.sleep(1)

        print(f"[BOOT] {light["name"]} LED: GREEN")
        light["light"].set_all(*COLOR_GREEN)
        time.sleep(1)

        print(f"[BOOT] {light["name"]} LED: BLUE")
        light["light"].set_all(*COLOR_BLUE)
        time.sleep(1)

        light["light"].off()

    print("[BOOT] Starting LED cycle test. Press Ctrl+C to stop.")
    builtin.on()

    try:
        while True:
            for light in rgb_lights:
                for i in range(light["light"]._pixel_count):
                    light["light"].set_pixel(i, *COLOR_ON)
                    time.sleep(0.1)
                    light["light"].set_pixel(i, *COLOR_OFF)
            time.sleep_ms(50)
    
    except KeyboardInterrupt:
        print("\n[BOOT] LED cycle test interrupted by user.")
    
    finally:
        for light in rgb_lights:
            light["light"].off()
        builtin.off()
        print("[BOOT] All lights turned off. Exiting.")


if __name__ == "__main__":
    main()