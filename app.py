import json
import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


POD_NAME = os.environ.get("POD_NAME", socket.gethostname())
NOT_READY_FILE = Path("/tmp/inventory-not-ready")


class InventoryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/inventory":
            status = 200
            body = {
                "pod": POD_NAME,
                "items": [
                    {"name": "Notebook", "quantity": 20},
                    {"name": "Pencil", "quantity": 50},
                ],
            }

        elif self.path == "/ready":
            ready = not NOT_READY_FILE.exists()
            status = 200 if ready else 503
            body = {"pod": POD_NAME, "ready": ready}

        else:
            status = 404
            body = {"error": "Not found"}

        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8080), InventoryHandler)
    print("Inventory listening on port 8080", flush=True)
    server.serve_forever()