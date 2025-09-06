import time
from drivers.led_builtin import LEDBuiltin

def main():
    print("LED Test")

    led = LEDBuiltin()

    # 1. Test ON
    print("Turning ON...")
    led.on()
    time.sleep(2)

    # 2. Test OFF
    print("Turning OFF...")
    led.off()
    time.sleep(2)

    # 3. Test TOGGLE
    print("Toggling 3 times...")
    for _ in range(3):
        led.toggle()
        time.sleep(0.5)

    # 4. Test BLINK (from Blink mixin)
    print("Blinking 5 times...")
    led.blink(times=5, duration=0.2)

if __name__ == "__main__":
    main()