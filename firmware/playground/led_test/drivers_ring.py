import time
from drivers.led_neopixel import Led_neopixel
from config import PIN_LED_RING, PIXEL_COUNT_RING, BRIGHTNESS_LED_RING

def main():
    ring = Led_neopixel(pin=PIN_LED_RING, pixel_count=PIXEL_COUNT_RING, brightness=BRIGHTNESS_LED_RING, auto_write=False)

    for c in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:
        r, g, b = c
        ring.set_all(r, g, b, show=True)
        time.sleep(2)

    for p in range(256):
        ring.set_all(*ring.cycle(p), show=True)
        time.sleep_ms(20)
    
    ring.set_all(0,0,0, show=True)
    for i in range(10):
        for i in range(ring._pixel_count):
            ring.set_pixel(i, 60, 60, 120, show=False)
            ring.show()
            time.sleep(0.5)
            ring.set_pixel(i, 0, 0, 0, show=False)
    
    ring.clear_buffer(show=True)


if __name__ == "__main__":
    main()