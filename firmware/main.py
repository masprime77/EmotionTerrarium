import time
import firmware.config as config

from services.wifi import WiFiService
from drivers.led_builtin import LEDBuiltin

def main():
    led = LEDBuiltin()
    wifi = WiFiService(config.WIFI_SSID, config.WIFI_PASSWORD, led = led)

    print("[WiFi] Connecting to:", config.WIFI_SSID)
    ok = wifi.connect(timeout_s=20)
    if not ok:
        print("[WiFi] Error (timeout). Verify SSID or PASSWORD.")
    else:
        print("[WiFi] CONNECTED. IFCONFIG:", wifi.ifconfig())

    while True:
        if not wifi.ensure_connected(timeout_s=10):
            print("[WiFi] Disconnected. Retrying...")
        time.sleep(5)

if __name__ == "__main__":
    main()
