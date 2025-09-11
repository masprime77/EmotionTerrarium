from drivers.led_neopixel import Led_neopixel
import time
from config import PIN_OVERHEAD_LED, PIXEL_COUNT_OVERHEAD, BRIGHTNESS_OVERHEAD_LED
from config import COLOR_ON

def main():
    led = Led_neopixel(PIN_OVERHEAD_LED, PIXEL_COUNT_OVERHEAD, BRIGHTNESS_OVERHEAD_LED, True)

    for i in range(PIXEL_COUNT_OVERHEAD):
        led.set_pixel(i, 100, 100, 100, None)
        time.sleep(0.3)

    led.off()

if __name__ == "__main__":
    main()