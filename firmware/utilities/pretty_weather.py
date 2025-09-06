def _fmt(v, unit=""):
    if v is None: 
        return "—"
    try:
        if isinstance(v, float):
            v = round(v, 1)
    except: 
        pass
    return f"{v}{unit}"

def _wmo_emoji(code):
    try: code = int(code)
    except: return "❓"
    if code == 0: return "☀️"
    if code in (1,): return "🌤️"
    if code in (2,): return "⛅"
    if code in (3,): return "☁️"
    if code in (45,48): return "🌫️"
    if code in (51,53,55): return "🌦️"
    if code in (61,63,65,80,81,82): return "🌧️"
    if code in (66,67): return "🌧️❄️"
    if code in (71,73,75,77,85,86): return "❄️"
    if code in (95,96,99): return "⛈️"
    return "❓"

def pretty_weather(w, place=None):
    """
    w: canonical dict -> {"ok","wmo","label","temp","humidity","time","source","age_s"}
    place: optional dict -> {"city","country"} or None
    """
    city = (place or {}).get("city") or "Location"
    country = (place or {}).get("country") or ""
    when = w.get("time") or "—"
    ok = w.get("ok", False)

    line_hdr = f"=== WEATHER NOW ==="
    loc_line = f"Place: {city}" + (f", {country}" if country else "")
    emoji = _wmo_emoji(w.get("wmo"))
    sky = f"{emoji}  {w.get('label','n/a')} (WMO: {w.get('wmo','—')})"
    t = _fmt(w.get("temp"), " C")
    h = _fmt(w.get("humidity"), " %")
    # age = w.get("age_s", 0)
    # age_str = f"{age}s old cache" if age else "fresh"

    print(line_hdr)
    print(loc_line)
    print("Time:", when, f" | Source: {w.get('source','?')}")
    if ok:
        print("Temp:", t, " | Humidity:", h)
        print("Sky: ", sky)
    else:
        print("Status: ❌ no data")
    print("====================\n")

def pretty_weather_one_line(w, place=None):
    """
    Compact single-line version.
    """
    city = (place or {}).get("city") or ""
    emoji = _wmo_emoji(w.get("wmo"))
    t = _fmt(w.get("temp"), "°C")
    lab = w.get("label","n/a")
    print(f"{city} {emoji} {lab} {t} @ {w.get('time','—')}")