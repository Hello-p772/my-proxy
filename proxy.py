from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.request
import os

TARGET_URL = "https://duckduckgo.com"

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = TARGET_URL + self.path

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

        try:
            response = urllib.request.urlopen(req)
            data = response.read()

            self.send_response(response.status)
            self.send_header("Content-Type", response.headers.get("Content-Type", "text/html"))
            self.end_headers()
            self.wfile.write(data)

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Proxy error: {e}".encode())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = ThreadingHTTPServer(("0.0.0.0", port), ProxyHandler)
    print(f"Proxy running on port {port}")
    server.serve_forever()
