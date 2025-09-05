import time
import config.config as config

from services.wifi import WiFiService
from drivers.led_builtin import LEDBuiltin

def main():
    led = LEDBuiltin()
    wifi = WiFiService(config.WIFI_SSID, config.WIFI_PASSWORD, led = led)

    print("[WiFi] Conectando a:", config.WIFI_SSID)
    ok = wifi.connect(timeout_s=20)
    if not ok:
        print("[WiFi] No se pudo conectar (timeout). Verifica SSID/clave o tipo de red.")
    else:
        print("[WiFi] Conectado. IFCONFIG:", wifi.ifconfig())

    # Bucle mínimo que vigila conexión
    while True:
        if not wifi.ensure_connected(timeout_s=10):
            print("[WiFi] Desconectado. Reintentando...")
        time.sleep(5)

if __name__ == "__main__":
    main()
