# drivers/fan_pwm.py
import machine
import time

class FanPWM:
    def __init__(self, pin, freq=25000, kick_ms=200):
        self._pin = machine.Pin(pin, machine.Pin.OUT)
        self._pwm = machine.PWM(self._pin)
        self._pwm.freq(int(freq))
        self._speed = 0.0
        self._kick_ms = int(kick_ms) if kick_ms else 0
        self.set_speed(0.0)

    def set_speed(self, speed):
        if speed < 0:
            speed = 0.0
            
        if speed > 1:
            speed = 1.0

        if self._speed == 0.0 and speed > 0.0 and speed < 0.3 and self._kick_ms > 0:
            self._pwm.duty_u16(65535)
            time.sleep_ms(self._kick_ms)

        self._speed = speed
        self._pwm.duty_u16(int(speed * 65535))

    def on(self):
        self.set_speed(1.0)

    def off(self):
        self.set_speed(0.0)

    def speed(self):
        return self._speed