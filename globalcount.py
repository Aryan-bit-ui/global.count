import http.server
import socketserver
import time

PORT = 8000
stats = {"total_visits": 0}

class StableBlockHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Using a very basic protocol response to keep Windows curl happy
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()

        stats["total_visits"] += 1
        my_id = stats["total_visits"]

        # ANSI Escape Codes
        HOME = "\033[H"   # Moves cursor to row 0, col 0
        CLEAR = "\033[2J" # Completely clears the terminal screen

        # Optional: Clear the screen once at the very start
        self.wfile.write(CLEAR.encode("utf-8"))

        try:
            while True:
                count = stats["total_visits"]
                # We start every frame with the HOME command
                output = (
                    f"{HOME}"
                    f"--------------------------\n"
                    f"   GLOBAL VISITOR COUNT   \n"
                    f"          >> {count} <<\n"
                    f"--------------------------\n"
                    f"You are visitor number: {my_id}\n"
                    f"Updating live... (Ctrl+C to stop)By Aryam from 7MB\n"
                )

                self.wfile.write(output.encode("utf-8"))
                self.wfile.flush()
                
                time.sleep(1)
                
        except (ConnectionResetError, BrokenPipeError):
            pass

    def log_message(self, format, *args): return

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), StableBlockHandler) as httpd:
        print(f"Server is running. Run: curl localhost:{PORT}")
        httpd.serve_forever()
