from services.http import http_get_json
from services.mapping_wmo import WMO

class WeatherService:
    def __init__(self, coordinates) -> None:
        self.coordinates = coordinates

    def get_weather(self):
        lat, lon = self.coordinates
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            "latitude={lat}&longitude={lon}"
            "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code"
            "&hourly=precipitation_probability"
            "&timezone=auto"
        ).format(lat=lat, lon=lon)

        data = http_get_json(url, timeout=10)
        cur = data.get("current", {})

        results = {
            "time": cur.get("time"),
            "temp_C": cur.get("temperature_2m"),
            "feels_like_C": cur.get("apparent_temperature"),
            "humidity_%": cur.get("relative_humidity_2m"),
            "wind_kmh": cur.get("wind_speed_10m"),
            "wmo_code": cur.get("weather_code")
        }

        return results
    
    def wmo_interpretation(code):
        try:
            return WMO.get(int(code), "Unknown")
        except:
            return "Unknown"
        
    def print_weather_interpretation(place, weather):
        print("\n==== CURRENT WEATHER ====")
        if place:
            name = "{} - {}".format(place.get("city") or "Location", place.get("country") or "")
            print("Place: ", name)
        if weather.get("time"):
            print("Time: ", w["time"])
        if weather.get("temp_C") is not None:
            print("Temp: {:.1f} C".format(w["temp_C"]))
        if weather.get("feels_like_C") is not None:
            print("Feels like: {:.1f} C".format(w["feels_like_C"]))
        if weather.get("humidity_%") is not None:
            print("Humidity: {} %".format(w["humidity_%"]))
        if weather.get("wind_kmh") is not None:
            print("Wind: {:.1f} km/h".format(w["wind_kmh"]))
        if weather.get("wmo_code") is not None:
            print("Sky: ", describe_wmo(w["wmo_code"]), "(WMO:", w["wmo_code"], ")")
        if weather.get("precip_prob_%") is not None:
            print("Precipitation probability (now): {} %".format(w["precip_prob_%"]))
        print("========================\n")