# main.py - MicroPython (Raspberry Pi Pico W)
import time
import sys
import gc
import network
import machine
import ujson as json

try:
    import urequests as requests
except ImportError:
    import requests  # in case your firmware exposes it as 'requests'

SSID = "iPhone 13 Pro Max de Mate"
PASSWORD = "Mateoooo11..."

LED = machine.Pin("LED", machine.Pin.OUT)

# --- Utilities --------------------------------------------------------------

def blink(n=2, on_ms=100, off_ms=100):
    for _ in range(n):
        LED.on()
        time.sleep_ms(on_ms)
        LED.off()
        time.sleep_ms(off_ms)

def wifi_connect(ssid, password, timeout_s=20):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    if not wlan.isconnected():
        print("[WiFi] Connecting to:", ssid)
        wlan.connect(ssid, password)
        t0 = time.ticks_ms()
        while not wlan.isconnected() and (time.ticks_diff(time.ticks_ms(), t0) < timeout_s*1000):
            print(".", end="")
            time.sleep_ms(500)
        print()
    if not wlan.isconnected():
        raise RuntimeError("Failed to connect to Wi-Fi.")
    print("[WiFi] Connected. IP:", wlan.ifconfig()[0])
    return wlan

def http_get_json(url, timeout=10):
    r = None
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            raise RuntimeError("HTTP %d" % r.status_code)
        data = r.json()
        return data
    finally:
        try:
            if r:
                r.close()
        except:
            pass

# --- Geolocation by IP (no API key) -----------------------------------

def get_location_ip():
    """
    Uses ipapi.co to obtain lat/lon/city based on the public IP.
    Note: On some routers/ISPs it may return the city of the exit node.
    """
    print("[Geo] Detecting location by IP...")
    url = "https://ipapi.co/json/"
    data = http_get_json(url, timeout=10)
    loc = {
        "lat": data.get("latitude"),
        "lon": data.get("longitude"),
        "city": data.get("city"),
        "country": data.get("country_name"),
    }
    if loc["lat"] is None or loc["lon"] is None:
        raise RuntimeError("Failed to obtain lat/lon.")
    print("[Geo] Location:", loc["city"], "-", loc["country"], "(%.4f, %.4f)" % (loc["lat"], loc["lon"]))
    return loc

# --- Weather with Open-Meteo (no API key) -------------------------------------

WMO_CODES = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm (light or moderate)",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def get_weather(lat, lon):
    # current: temp, feels like, humidity, wind, WMO code
    # hourly: precipitation probability (useful as extra data near current hour)
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude={lat}&longitude={lon}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code"
        "&hourly=precipitation_probability"
        "&timezone=auto"
    ).format(lat=lat, lon=lon)

    data = http_get_json(url, timeout=10)

    cur = data.get("current", {})
    hourly = data.get("hourly", {})

    # Extra: precipitation probability at current hour if found
    precip_prob_now = None
    try:
        times = hourly.get("time", [])
        probs = hourly.get("precipitation_probability", [])
        # Search for the exact current hour index if it matches
        now_iso = cur.get("time")
        if now_iso and times and probs and len(times) == len(probs):
            # Linear search; arrays usually ~24-48 h
            for i, t in enumerate(times):
                if t == now_iso:
                    precip_prob_now = probs[i]
                    break
    except:
        pass

    result = {
        "time": cur.get("time"),
        "temp_C": cur.get("temperature_2m"),
        "feels_like_C": cur.get("apparent_temperature"),
        "humidity_%": cur.get("relative_humidity_2m"),
        "wind_kmh": cur.get("wind_speed_10m"),
        "wmo_code": cur.get("weather_code"),
        "precip_prob_%": precip_prob_now,
    }
    return result

def describe_wmo(code):
    try:
        return WMO_CODES.get(int(code), "Unknown")
    except:
        return "Unknown"

def pretty_print_weather(place, w):
    print("\n==== CURRENT WEATHER ====")
    if place:
        name = "{} - {}".format(place.get("city") or "Location", place.get("country") or "")
        print("Place: ", name)
    if w.get("time"):
        print("Time:   ", w["time"])
    if w.get("temp_C") is not None:
        print("Temp:   {:.1f} °C".format(w["temp_C"]))
    if w.get("feels_like_C") is not None:
        print("Feels like: {:.1f} °C".format(w["feels_like_C"]))
    if w.get("humidity_%") is not None:
        print("Humidity: {} %".format(w["humidity_%"]))
    if w.get("wind_kmh") is not None:
        print("Wind:   {:.1f} km/h".format(w["wind_kmh"]))
    if w.get("wmo_code") is not None:
        print("Sky:    ", describe_wmo(w["wmo_code"]), "(WMO:", w["wmo_code"], ")")
    if w.get("precip_prob_%") is not None:
        print("Precipitation probability (now): {} %".format(w["precip_prob_%"]))
    print("========================\n")

# --- Main --------------------------------------------------------------------

def main():
    try:
        blink(1, 80, 80)
        wifi_connect(SSID, PASSWORD)
        blink(2, 60, 60)

        # 1) Location by IP
        try:
            place = get_location_ip()
            lat, lon = place["lat"], place["lon"]
        except Exception as e:
            # Fallback: set your lat/lon manually here if IP geo fails
            print("[Geo] Fallback to manual coordinates:", e)
            # EXAMPLE: Darmstadt, DE
            lat, lon = 49.8728, 8.6512
            place = {"city": "Darmstadt", "country": "Germany", "lat": lat, "lon": lon}

        # 2) Weather
        w = get_weather(lat, lon)
        pretty_print_weather(place, w)
        blink(3, 50, 80)

    except Exception as e:
        print("[ERROR]", e)
        # Error blinking
        for _ in range(5):
            LED.on()
            time.sleep_ms(80)
            LED.off()
            time.sleep_ms(80)

    finally:
        gc.collect()

if __name__ == "__main__":
    main()