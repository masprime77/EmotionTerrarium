import ujson as json
import time

from services.http_server import serve
from services.wifi import WiFiService
from services.emotion_service import EmotionService
from controllers.emotion_controller import EmotionController
from drivers.led_neopixel import LedNeopixel
import config

# --- init devices/services ---
_led = None
_ctr = None
_emo = None

def _init_once():
    global _led, _ctr, _emo
    if _led is None:
        # Usa overhead o ring; cambia si prefieres el ring
        _led = LedNeopixel(
            pin=config.PIN_LED_RING,
            pixel_count=config.PIXEL_COUNT_RING,
            auto_show=True
        )
        _ctr = EmotionController(_led, brightness=0.25)
        _emo = EmotionService(label="default")
        _ctr.render_color(_emo.get_color())
        
        try:
            import ujson as json
            with open("last_emotion.json") as f:
                saved = json.loads(f.read() or "{}")
                # usa el top-1 si existen labels
                labels = saved.get("labels") or []
                if labels:
                    _emo.set_emotion(labels[0])
                    _ctr.render_color(_emo.get_color())
        except:
            pass

# --- HTTP handlers ---
def handle_request(method, path, raw_req):
    _init_once()

    if method == "GET" and path == "/ping":
        return "200 OK", "application/json", json.dumps({"ok": True})

    if path == "/emotion":
        if method == "GET":
            st = _emo.to_dict()
            body = json.dumps({"ok": True, "state": st})
            return "200 OK", "application/json", body

        if method == "POST":
            try:
                body = raw_req.split("\r\n\r\n", 1)[1]
                data = json.loads(body) if body else {}
            except Exception as e:
                return "400 Bad Request", "application/json", json.dumps({"ok": False, "error": "bad json: %s" % e})

            labels = data.get("labels") or []
            text = data.get("text") or ""

            if not labels:
                return "400 Bad Request", "application/json", json.dumps({"ok": False, "error": "labels required (1..3)"} )

            # M4: tomamos top-1 (mezclas llegan en M5)
            label = str(labels[0]).strip().lower()

            try:
                state = _emo.set_emotion(label)
                _ctr.render_color(_emo.get_color())
            except Exception as e:
                return "400 Bad Request", "application/json", json.dumps({"ok": False, "error": str(e)})

            # opcional: persistir último estado
            try:
                with open("last_emotion.json", "w") as f:
                    f.write(json.dumps({"labels": labels[:3], "text": text, "applied": state}))
            except:
                pass

            resp = {
                "ok": True,
                "applied": {
                    "label": _emo.label(),
                    "rgb": _emo.get_color()
                },
                "echo": {"labels": labels[:3], "text": text}
            }
            return "200 OK", "application/json", json.dumps(resp)

        return "405 Method Not Allowed", "application/json", json.dumps({"ok": False})

    return "404 Not Found", "application/json", json.dumps({"ok": False, "error": "route"})

def main():
    wlan = WiFiService(config.SSID, config.PASSWORD)
    wlan.connect()
    ip = wlan.ifconfig()[0]
    print("[M4/Step2] Open GET :  http://%s/emotion" % ip)
    print("[M4/Step2] POST labels: curl -X POST http://%s/emotion -H 'Content-Type: application/json' -d '{\"labels\":[\"happy\",\"calm\"],\"text\":\"optional\"}'" % ip)
    serve(handle_request)

if __name__ == "__main__":
    main()