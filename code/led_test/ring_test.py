import machine, neopixel, time

PIN = 15     # usa GP2; cambia si conectaste otro
N = 7       # número de LEDs del anillo
BRIGHT = 0.2  # limita consumo (0.0–1.0)

np = neopixel.NeoPixel(machine.Pin(PIN), N)

def set_all(r, g, b):
    for i in range(N):
        np[i] = (int(r*BRIGHT), int(g*BRIGHT), int(b*BRIGHT))
    np.write()

# Test 1: secuencia RGB + blanco
for color in [(255,0,0), (0,255,0), (0,0,255), (255,255,255), (0,0,0)]:
    set_all(*color)
    time.sleep(0.6)

# Test 2: barrido uno por uno
set_all(0,0,0)
for i in range(N):
    np[i] = (int(255*BRIGHT), 0, 0)
    np.write()
    time.sleep(0.15)
    np[i] = (0,0,0)
    np.write()

# Test 3: arcoíris suave (para observar estabilidad)
def wheel(pos):
    if pos < 85:
        return (255 - pos*3, pos*3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos*3, pos*3)
    else:
        pos -= 170
        return (pos*3, 0, 255 - pos*3)

j = 0
while True:
    for i in range(N):
        np[i] = tuple(int(v*BRIGHT) for v in wheel((i*256//N + j) & 255))
    np.write()
    j = (j + 1) & 255
    time.sleep(0.02)