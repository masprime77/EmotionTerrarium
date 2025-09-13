import config
import time
from drivers.led_builtin import LedBuiltin
from drivers.led_neopixel import LedNeopixel
from drivers.led_bar10 import LedBar10
from drivers.dht22_sensor import DHT22Sensor
from drivers.fan_pwm import FanPWM

def main():
    led_builtin = LedBuiltin()
    led_ring = LedNeopixel(config.PIN_LED_RING, config.BRIGHTNESS_LED_RING, auto_show=True)
    led_overhead = LedNeopixel(config.PIN_OVERHEAD_LED, config.BRIGHTNESS_OVERHEAD_LED, auto_show=True)
    led_bar = LedBar10(config.PIN_LED_BAR10)
    th_sensor = DHT22Sensor(config.PIN_DHT22_SENSOR, 500)
    fan = FanPWM(config.PIN_FAN_PWM)

    led_builtin.blink(5, 0.2)

    rgb_leds = [led_ring, led_overhead]

    for led in rgb_leds:
        led.set_all(*config.COLOR_RED)
        time.sleep(0.5)
        led.set_all(*config.COLOR_GREEN)
        time.sleep(0.5)
        led.set_all(*config.COLOR_BLUE)
        time.sleep(0.5)
        led.set_all(*config.COLOR_OFF)

    for i, _ in enumerate(config.PIN_LED_BAR10):
        led_bar.set_level(i)
        time.sleep(0.2)

    led_bar.set_mask(0b1010101010)
    time.sleep(0.75)
    led_bar.set_mask(0b0101010101)
    time.sleep(0.75)
    led_bar.off()

    fan.on()
    time.sleep(5)
    fan.off()

    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < 5000:
        if time.ticks_diff(time.ticks_ms(), t0) >= th_sensor.refresh_rate():
            t, h = th_sensor.read()
            print("T: ", t, ". H: ", h)
        time.sleep_ms(50)

    for _ in range(5):
        led_builtin.blink(1, 0.1)

        for led in rgb_leds:
            for i in range(led.pixel_count()):
                led.set_pixel(i, *config.COLOR_ON)
                time.sleep(0.1)
                led.set_pixel(i, *config.COLOR_OFF)

        for i, _ in enumerate(config.PIN_LED_BAR10):
            led_bar.set_led(i, "on")
            time.sleep(0.1)
            led_bar.set_led(i, "off")

if __name__ == "__main__":
    main()