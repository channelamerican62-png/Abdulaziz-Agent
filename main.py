import os
import sys

# Ensure engine path is cleanly accessible whether running on Windows or Linux Cloud VPS
root_dir = os.path.dirname(os.path.abspath(__file__))
engine_dir = os.path.join(root_dir, "engine")
if engine_dir not in sys.path:
    sys.path.insert(0, engine_dir)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from telegram_bot import AbdulazizTelegramBot
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("👑 Abdulaziz Agent is LIVE & HEALTHY on Cloud 24/7!".encode('utf-8'))
    def log_message(self, format, *args):
        pass # Suppress HTTP access spam in logs

def start_health_server():
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"🌐 [Cloud Health Server] Port {port} da tekshiruv serveri ishga tushdi!")
        server.serve_forever()
    except Exception as e:
        print(f"⚠️ Health server start error: {e}")

if __name__ == "__main__":
    print("======================================================")
    print("   👑 ABDULAZIZ AGENT — CLOUD & LOCAL ENTRYPOINT      ")
    print("   Yaratuvchi: Otajonov Abdulaziz                     ")
    print("   Miya: OpenRouter Zero-Cost Pool + Ollama Fallback  ")
    print("======================================================")
    
    # Start background HTTP server so Render / Railway detects open port instantly
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    bot = AbdulazizTelegramBot()
    bot.run()
