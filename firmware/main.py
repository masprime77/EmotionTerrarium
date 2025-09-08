import time
from drivers.led_neopixel import Led_neopixel
from config import PIN_LED_RING, PIXEL_COUNT_RING, BRIGHTNESS_LED_RING, PIN_OVERHEAD_LED, PIXEL_COUNT_OVERHEAD, BRIGHTNESS_OVERHEAD_LED
from config import COLOR_ON, COLOR_OFF

def main():
    ring = Led_neopixel(pin=16, pixel_count=7, brightness=BRIGHTNESS_LED_RING, auto_write=False)
    strip = Led_neopixel(pin=15, pixel_count=32, brightness=BRIGHTNESS_OVERHEAD_LED, auto_write=False)

    for c in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:
        r, g, b = c
        ring.set_all(r, g, b, show=True)
        strip.set_all(r, g, b, show=True)
        time.sleep(2)

    for p in range(256):
        ring.set_all(*ring.cycle(p), show=True)
        strip.set_all(*strip.cycle(p), show=True)
        time.sleep_ms(20)
    
    ring.off()
    strip.off()
    
    while True:
        for i in range(ring._pixel_count):
            ring.set_pixel(i, *COLOR_ON, show=True)
            time.sleep(0.1)
            ring.set_pixel(i, *COLOR_OFF, show=True)
        
        for i in range(strip._pixel_count):
            strip.set_pixel(i, *COLOR_ON, show=True)
            time.sleep(0.1)
            strip.set_pixel(i, *COLOR_OFF, show=True)
    
    ring.clear_buffer(show=True)
    strip.clear_buffer(show=True)


if __name__ == "__main__":
    main()