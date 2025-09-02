import network
import time
import secrets

wlan = network.WLAN(network.STA_IF)  # modo estación (cliente)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)

# Esperar hasta que se conecte
while not wlan.isconnected():
    print("Conectando...")
    time.sleep(1)

print("Conectado!")
print("IP:", wlan.ifconfig())