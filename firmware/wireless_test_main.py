import time
import config

from drivers.led_builtin import LEDBuiltin
from services.wifi import WiFiService
from services.http import http_get_json

lat, lon = 49.8728, 8.6512
TEST_URL = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude={lat}&longitude={lon}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code"
        "&hourly=precipitation_probability"
        "&timezone=auto"
    ).format(lat=lat, lon=lon)

def main():
    led = LEDBuiltin()
    wifi = WiFiService(config.SSID, config.PASSWORD, led=led)

    if wifi.connect(timeout_s=20):
        print("Connected. IP:", wifi.ifconfig()[0])
        data = http_get_json(TEST_URL, timeout=10)
        cur = data.get("current", {})
        result = {
            "time": cur.get("time"),
            "temp_C": cur.get("temperature_2m"),
            "feels_like_C": cur.get("apparent_temperature"),
            "humidity_%": cur.get("relative_humidity_2m"),
            "wind_kmh": cur.get("wind_speed_10m"),
            "wmo_code": cur.get("weather_code")
        }
        print(result)
    else:
        print("No Wi-Fi connection")

if __name__ == "__main__":
    main()