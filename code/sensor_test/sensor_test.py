import machine
import dht
import time

# Sensor DHT22 en GP15
sensor = dht.DHT22(machine.Pin(17))

# LED integrado del Pico
led = machine.Pin("LED", machine.Pin.OUT)

# Espera inicial para que el sensor esté listo
time.sleep(2)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        print("Temp: {:.1f} C  Hum: {:.1f} %".format(temp, hum))
        
        # Enciende el LED si la lectura fue exitosa
        led.value(1)
        time.sleep(0.5)
        led.value(0)

    except Exception as e:
        print("Error:", e)
        # Parpadeo rápido si hay error
        for _ in range(3):
            led.toggle()
            time.sleep(0.2)
    
    time.sleep(2)