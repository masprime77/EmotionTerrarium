import time
import config

from drivers.led_builtin import LEDBuiltin
from services.wifi import WiFiService
from services.weather_service import WeatherService
from utilities.pretty_weather import pretty_weather, pretty_weather_one_line

def main():
    # lat, lon = 49.8728, 8.6512
    # place = {"city": "Darmstadt", "country": "Germany"}

    lat, lon = -16.395578, -71.556022
    place = {"city": "Arequipa", "country": "Peru"}

    led = LEDBuiltin()
    wifi = WiFiService(config.SSID, config.PASSWORD, led=led)
    if wifi.connect(timeout_s=20): print("Connected!")
    else: print("Not connected :(")
    weather = WeatherService((lat, lon))

    wn = weather.get_now(cache_max_age_sec=0)
    pretty_weather(wn, place)
    pretty_weather_one_line(wn, place)

    weather_period_s = 600
    t0 = time.ticks_ms()
    while True:
        if time.ticks_diff(time.ticks_ms(), t0) >= weather_period_s * 1000:
            wn = weather.get_now(cache_max_age_sec=0)
            pretty_weather(wn, place)
            t0 = time.ticks_ms()
        time.sleep_ms(50)


if __name__ == "__main__":
    main()