from config import SSID, PASSWORD
from drivers.led_builtin import LedBuiltin
from services.wifi import WiFiService
from services. weather_service import WeatherService
from utilities.pretty_weather import pretty_weather, pretty_weather_one_line

def main(location="D"):
    if location == "D":
        lat, lon = 49.8728, 8.6512
        place = {"city": "Darmstadt", "country": "Germany"}

    if location == "A":
        lat, lon = -16.395578, -71.556022
        place = {"city": "Arequipa", "country": "Peru"}

    print("[Test M2] Starting weather fetch test for location:", place["city"], place["country"])

    led = LedBuiltin()
    wifi = WiFiService(SSID, PASSWORD, led=led)

    if wifi.connect(timeout_s=20):
        print("Connected!")
    else:
        print("Not connected :(\n" \
        "Skipping weather fetch.\n")
        print("[Test M2] Done.")
        return
    
    weather = WeatherService((lat, lon))

    wn = weather.get_now(cache_max_age_sec=0, timeout=5)
    pretty_weather(wn, place)
    pretty_weather_one_line(wn, place)

    led.off()
    print("[Test M2] Weather fetch test completed.\n")
    print("[Test M2] Done.")

if __name__ == "__main__":
    main()