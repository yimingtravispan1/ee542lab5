from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

THINGSBOARD_URL = "http://127.0.0.1:8080/api/v1/9n4cI1g93SuOkDPK9Eui/telemetry"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)

        req = urllib.request.Request(
            THINGSBOARD_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as response:
                response.read()

            body = b"[]"

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except Exception as e:
            print(e)
            self.send_response(500)
            self.end_headers()

HTTPServer(("0.0.0.0", 8081), Handler).serve_forever()
