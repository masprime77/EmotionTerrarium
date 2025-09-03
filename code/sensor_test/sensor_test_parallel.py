import machine
import dht
import time

# Definición de sensores en GP15 y GP16 (cambia si usas otros pines)
sensor1 = dht.DHT22(machine.Pin(17))
sensor2 = dht.DHT22(machine.Pin(16))

# LED integrado del Pico
led = machine.Pin("LED", machine.Pin.OUT)

# Espera inicial para que los sensores estén listos
time.sleep(2)

while True:
    try:
        # Medir ambos sensores
        sensor1.measure()
        temp1 = sensor1.temperature()
        hum1 = sensor1.humidity()
        
        sensor2.measure()
        temp2 = sensor2.temperature()
        hum2 = sensor2.humidity()
        
        # Mostrar resultados
        print("Sensor 1 -> Temp: {:.1f} C  Hum: {:.1f} %".format(temp1, hum1))
        print("Sensor 2 -> Temp: {:.1f} C  Hum: {:.1f} %".format(temp2, hum2))
        print("-------------------------------------------------")
        
        # LED encendido breve si ambas lecturas fueron exitosas
        led.on()
        time.sleep(0.5)
        led.off()
        
    except Exception as e:
        print("Error:", e)
        # Parpadeo rápido si hay error
        for _ in range(3):
            led.toggle()
            time.sleep(0.2)
    
    # Espera mínima entre lecturas (>=2s)
    time.sleep(2.5)