# services/http.py
from utils.logger import log

# En MicroPython normalmente se usa 'urequests'
try:
    import urequests as requests
except ImportError:
    import requests

def http_get_json(url: str, timeout: int = 10):
    r = None
    try:
        r = requests.get(url, timeout=timeout)
        if hasattr(r, "status_code") and r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}")
        return r.json()
    finally:
        try:
            if r: r.close()
        except:
            pass