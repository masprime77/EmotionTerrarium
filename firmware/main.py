import time
import config

from drivers.led_builtin import LedBuiltin
from services.wifi import WiFiService
from services.http import http_get_json

TEST_URL = "http://worldtimeapi.org/api/ip"  # usamos http plano

def main():
    led = LedBuiltin()
    wifi = WiFiService(config.SSID, config.PASSWORD, led=led)

    if wifi.connect(timeout_s=20):
        print("Connected. IP:", wifi.ifconfig()[0])
        data = http_get_json(TEST_URL, timeout=10)
        tz = data.get("timezone", "?")
        print("Timezone:", tz)
    else:
        print("No Wi-Fi connection")

    while True:
        wifi.ensure_connected(timeout_s=10)
        time.sleep(5)

if __name__ == "__main__":
    main()