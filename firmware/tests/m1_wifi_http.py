from config import SSID, PASSWORD
from services.wifi import WiFiService
from services.http import http_get_json
from drivers.led_builtin import LedBuiltin

def main():
    led = LedBuiltin()
    wifi = WiFiService(SSID, PASSWORD, led)

    try:
        print("[Test M1] Connecting to Wi-Fi...")
        wifi.connect(timeout_s=30)
        print("[Test M1] Connected. IP:", wifi.ifconfig()[0])

        print("[Test M1] Fetching test JSON...")
        url = "http://ip-api.com/json"
        data = http_get_json(url, timeout=10)

        print("[Test M1] HTTP GET OK:")
        print("  City:", data.get("city"))
        print("  Country:", data.get("country"))
        print("  Lat/Lon:", data.get("lat"), ",", data.get("lon"))

        led.blink(3, 0.5)

    except Exception as e:
        print("[Test M1] ERROR:", e)
        led.blink(5, 0.2)

    finally:
        print("[Test M1] Finished.")

if __name__ == "__main__":
    main()