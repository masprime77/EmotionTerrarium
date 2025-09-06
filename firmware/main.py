import time
import config

from drivers.led_builtin import LEDBuiltin
from services.wifi import WiFiService
from services.http import http_get_json
from services.weather_service import WeatherService
from utilities.pretty_weather import pretty_weather



def main():
    lat, lon = 49.8728, 8.6512
    place = {"city": "Darmstadt", "country": "Germany"}

    led = LEDBuiltin()
    wifi = WiFiService(config.SSID, config.PASSWORD, led=led)
    weather = WeatherService((lat, lon))
    connection = False

    wn = weather.get_now()
    pretty_weather


if __name__ == "__main__":
    main()