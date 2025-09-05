import machine
import dht
import time
import neopixel

# ==== Configuración del sensor DHT22 ====
PIN_DHT = 16
sensor = dht.DHT22(machine.Pin(PIN_DHT))

# ==== Configuración del anillo LED (WS2812/NeoPixel) ====
PIN_LED = 18        # GPIO donde está conectado el anillo
NUM_LEDS = 7       # Número de LEDs en tu anillo
np = neopixel.NeoPixel(machine.Pin(PIN_LED), NUM_LEDS)

# ==== Función para calcular color según humedad ====
def hum_to_color(hum):
    """
    Devuelve un color RGB en gradiente azul→rojo
    según la humedad entre 50 % y 60 %.
    """
    h_min = 50
    h_max = 70
    
    # Limitar el rango
    if hum < h_min:
        hum = h_min
    if hum > h_max:
        hum = h_max
    
    # Factor de interpolación (0 → azul, 1 → rojo)
    factor = (hum - h_min) / (h_max - h_min)
    
    # Azul (0,0,255) → Rojo (255,0,0)
    r = int(255 * factor)
    g = 0
    b = int(255 * (1 - factor))
    
    return (r, g, b)

# ==== Bucle principal ====
time.sleep(2)  # espera inicial para estabilizar el DHT22

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        print("Temp: {:.1f} °C  Hum: {:.1f} %".format(temp, hum))
        
        # Convertir humedad a color
        color = hum_to_color(hum)
        
        # Encender todos los LEDs con el color calculado
        for i in range(NUM_LEDS):
            np[i] = color
        np.write()
        
    except Exception as e:
        print("Error:", e)
        # En caso de error, parpadeo en violeta
        for i in range(NUM_LEDS):
            np[i] = (128, 0, 128)
        np.write()
        time.sleep(0.5)
        for i in range(NUM_LEDS):
            np[i] = (0, 0, 0)
        np.write()
        time.sleep(0.5)
    
    time.sleep(0.5)  # tiempo mínimo entre lecturas