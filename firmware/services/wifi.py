import time
import network

class WiFiService:
    def __init__(self, ssid: str, password: str, led=None):
        self.ssid = ssid
        self.password = password
        self.led = led  # opcional: LedBuiltin para señales

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self, timeout_s: int = 20) -> bool:
        if self.is_connected():
            return True

        # Turn the LED off before starting connection
        if self.led:
            self.led.off()

        self.wlan.connect(self.ssid, self.password)

        t0 = time.ticks_ms()
        while not self.is_connected():
            # Estado intermedio: parpadeo leve
            if self.led:
                self.led.on()
                time.sleep_ms(150)
                self.led.off()
            if time.ticks_diff(time.ticks_ms(), t0) > timeout_s * 1000:
                return False
        # Conectado: LED ON fijo
        if self.led:
            self.led.on()
        return True

    def is_connected(self) -> bool:
        try:
            return self.wlan.isconnected()
        except:
            return False

    def ifconfig(self):
        return self.wlan.ifconfig() if self.is_connected() else None

    def disconnect(self):
        try:
            self.wlan.disconnect()
        except:
            pass

    def ensure_connected(self, timeout_s: int = 10) -> bool:
        """
        Ensures that the device is connected to WiFi.
        If already connected, returns True immediately.
        Otherwise, attempts to connect with the given timeout.
        """
        if self.is_connected():
            return True
        return self.connect(timeout_s=timeout_s)