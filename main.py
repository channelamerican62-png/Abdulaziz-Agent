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

if __name__ == "__main__":
    print("======================================================")
    print("   👑 ABDULAZIZ AGENT — CLOUD & LOCAL ENTRYPOINT      ")
    print("   Yaratuvchi: Otajonov Abdulaziz                     ")
    print("   Miya: OpenRouter Zero-Cost Pool + Ollama Fallback  ")
    print("======================================================")
    bot = AbdulazizTelegramBot()
    bot.run()
