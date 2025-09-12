# services/http_server.py  (MicroPython)
import usocket as socket

def _send_headers(conn, status="200 OK", ctype="application/json", cors=True):
    conn.send("HTTP/1.1 %s\r\n" % status)
    conn.send("Content-Type: %s\r\n" % ctype)
    if cors:
        conn.send("Access-Control-Allow-Origin: *\r\n")
        conn.send("Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n")
        conn.send("Access-Control-Allow-Headers: Content-Type\r\n")
    conn.send("Connection: close\r\n\r\n")

def serve(handle_request, host="0.0.0.0", port=80):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(2)
    while True:
        conn, addr = s.accept()
        try:
            req = conn.recv(1024).decode()
            if not req:
                conn.close(); continue
            line0 = req.split("\r\n", 1)[0]
            method, path, _ = line0.split(" ")

            if method == "OPTIONS":
                _send_headers(conn, "204 No Content"); conn.close(); continue

            status, ctype, body = handle_request(method, path, req)
            _send_headers(conn, status, ctype)
            if body:
                conn.send(body)
        except Exception as e:
            try:
                _send_headers(conn, "500 Internal Server Error")
                conn.send('{"ok":false,"error":"%s"}' % str(e))
            except:
                pass
        finally:
            conn.close()