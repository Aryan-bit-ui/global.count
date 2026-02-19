import http.server
import socketserver
import os
import random

# Railway provides the PORT automatically
PORT = int(os.environ.get("PORT", 8000))

# Shared stats (Reset when server restarts on free tier)
stats = {"total_visits": 0}

RAINBOW = ["\033[1;31m", "\033[1;33m", "\033[1;32m", "\033[1;36m", "\033[1;34m", "\033[1;35m"]
RESET = "\033[0m"

class RailwayHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Update Count
        stats["total_visits"] += 1
        count = stats["total_visits"]
        color = random.choice(RAINBOW)

        # 2. Send Headers
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()

        # 3. Create the Box (One-time delivery, no loop)
        output = (
            f"\n{color}"
            f"--------------------------\n"
            f"   GLOBAL VISITOR COUNT   \n"
            f"          >> {count} <<\n"
            f"--------------------------{RESET}\n"
            f"You are visitor number: {count}\n"
            f"By Aryan 7MB | Refresh to update\n\n"
        )

        # 4. Write and Close
        self.wfile.write(output.encode("utf-8"))

    def log_message(self, format, *args): return

if __name__ == "__main__":
    # Important: Bind to 0.0.0.0 so Railway can see it
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), RailwayHandler) as httpd:
        print(f"Server live on port {PORT}")
        httpd.serve_forever()
