import network
import time
from config import SSID, PASSWORD

wlan = network.WLAN(network.STA_IF)  # modo estación (cliente)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Esperar hasta que se conecte
while not wlan.isconnected():
    print("Conectando...")
    time.sleep(1)

print("Conectado!")
print("IP:", wlan.ifconfig())