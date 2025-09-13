import time
from config import DEBUG, M0_TEST, M1_TEST, M2_TEST, M3_TEST, M4_S1_TEST, M4_S2_TEST
from config import PIN_LED_RING, PIXEL_COUNT_RING, PIN_OVERHEAD_LED, PIXEL_COUNT_OVERHEAD
from config import COLOR_RED, COLOR_GREEN, COLOR_BLUE
from config import COLOR_ON, COLOR_OFF

from tests import m0_bootstrap
from tests import m1_wifi_http
from tests import m2_weather_service
from tests import m3_ambient_controller
from tests import m4_step1_ping
from tests import m4_step2_emotion

from drivers.led_builtin import LedBuiltin
from drivers.led_neopixel import LedNeopixel

    
def main():
    if DEBUG:
        if M0_TEST:
            print("=== Running m0_bootstrap ===")
            m0_bootstrap.main()
        
        if M1_TEST:
            print("=== Running m1_wifi_http ===")
            m1_wifi_http.main()

        if M2_TEST:
            print("=== Running m2_weather_service ===")
            m2_weather_service.main(location="D")
        
        if M3_TEST:
            print("=== Running m3_ambient_controller ===")
            m3_ambient_controller.main()

        if M4_S1_TEST:
            print("=== Running m4_step1_ping ===")
            m4_step1_ping.main()

        if M4_S2_TEST:
            print("=== Running m4_step2_emotion ===")
            m4_step2_emotion.main()

        return

    builtin = LedBuiltin()
    print("[BOOT] Built-in LED blinking test")
    builtin.blink(1, 0.5)
    builtin.off()

    ring = {
        "name": "Ring",
        "light": LedNeopixel(pin=PIN_LED_RING, pixel_count=PIXEL_COUNT_RING,auto_show=True)
    }

    overhead = {
        "name": "Overhead",
        "light": LedNeopixel(pin=PIN_OVERHEAD_LED, pixel_count=PIXEL_COUNT_OVERHEAD, auto_show=True)
    }

    rgb_lights = [ring, overhead]

    for light in rgb_lights:
        light["light"].off()

    for light in rgb_lights:
        print(f"[BOOT] {light["name"]} LED: RED")
        light["light"].set_all(*COLOR_RED, show=None)
        time.sleep(1)

        print(f"[BOOT] {light["name"]} LED: GREEN")
        light["light"].set_all(*COLOR_GREEN, show=None)
        time.sleep(1)

        print(f"[BOOT] {light["name"]} LED: BLUE")
        light["light"].set_all(*COLOR_BLUE, show=None)
        time.sleep(1)

        light["light"].off()

    print("[BOOT] Starting LED cycle test. Press Ctrl+C to stop.")
    builtin.on()

    try:
        while True:
            for light in rgb_lights:
                for i in range(light["light"]._pixel_count):
                    light["light"].set_pixel(i, *COLOR_ON)
                    time.sleep(0.5)
                    light["light"].set_pixel(i, *COLOR_OFF)
            time.sleep_ms(10)
    
    except KeyboardInterrupt:
        print("\n[BOOT] LED cycle test interrupted.\n" \
              "Interrupted by user.")
    
    finally:
        for light in rgb_lights:
            light["light"].off()
        builtin.off()
        print("[BOOT] All lights turned off. Exiting.")


if __name__ == "__main__":
    main()