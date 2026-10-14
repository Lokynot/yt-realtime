from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class AppHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response = {
                "status": "healthy",
                "application": "yt-realtime"
            }

            self.wfile.write(json.dumps(response).encode())

        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            self.wfile.write(
                b"Welcome to Real-Time CI/CD Pipeline Project!"
            )

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), AppHandler)
    print("Application running on port 8000")
    server.serve_forever()
