import ujson as json
from services.http_server import serve
from services.wifi import WiFiService
import config

def handle_request(method, path, raw_req):
    if method == "GET" and path == "/ping":
        return "200 OK", "application/json", json.dumps({"ok": True})
    return "404 Not Found", "application/json", json.dumps({"ok": False})

def main():
    wlan = WiFiService(config.SSID, config.PASSWORD)
    wlan.connect()
    ip = wlan.ifconfig()[0]
    print("[M4/Step1] Open: http://%s/ping" % ip)
    serve(handle_request)

if __name__ == "__main__":
    main()