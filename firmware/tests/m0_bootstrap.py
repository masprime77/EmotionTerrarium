import time
from drivers.led_builtin import LedBuiltin

def main():
    led = LedBuiltin()
    print("[Test M0] Starting FIRST blink test for 5 seconds...")
    t0 = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), t0) < 10000:
        led.on()
        time.sleep_ms(1000)
        led.off()
        time.sleep_ms(1000)

    print("[Test M0] Starting SECOND blink test for 5 seconds...")

    led.blink(5, 1)

    print("[Test M0] Done. Entering idle (LED off).")
    led.off()

if __name__ == "__main__":
    main()