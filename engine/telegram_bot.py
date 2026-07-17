import os
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from abdulaziz_loop import AbdulazizAgentEngine
from tools.terminal_ops import run_powershell_command

class AbdulazizTelegramBot:
    """
    Abdulaziz Telegram Bot — Connects Abdulaziz Agent Engine to Telegram directly.
    Created by Otajonov Abdulaziz.
    """
    def __init__(self):
        self.engine = AbdulazizAgentEngine()
        self.token = self._get_bot_token()
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.offset = 0
        self.dataset_path = "D:\\3D AI\\Abdulaziz-Agent\\dataset\\train_tool_use.jsonl"
        
    def _get_bot_token(self) -> str:
        # Check environment or local .env first
        for env_path in ["D:\\3D AI\\Abdulaziz-Agent\\.env", "C:\\Users\\Smart\\AppData\\Local\\hermes\\.env"]:
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                            return line.strip().split('=', 1)[1]
        return os.getenv("TELEGRAM_BOT_TOKEN", "")

    def _send_request(self, method: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.api_url}/{method}"
        try:
            if data:
                req_body = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(
                    url,
                    data=req_body,
                    headers={"Content-Type": "application/json"}
                )
            else:
                req = urllib.request.Request(url)
                
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f"[Xato] Telegram API bilan aloqa xatosi ({method}): {str(e)}")
            return {"ok": False}

    def send_message(self, chat_id: int, text: str):
        """Send a message to Telegram, splitting if longer than 4000 chars and auto-recovering from markdown errors."""
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)] if len(text) > 4000 else [text]
        for idx, chunk in enumerate(chunks):
            msg_text = f"(Qism {idx+1})\n{chunk}" if len(chunks) > 1 else chunk
            res = self._send_request("sendMessage", {"chat_id": chat_id, "text": msg_text, "parse_mode": "Markdown"})
            if not res.get("ok"):
                # Fallback to plain text if markdown parsing fails
                self._send_request("sendMessage", {"chat_id": chat_id, "text": msg_text})

    def save_live_harvest(self, user_text: str, agent_reply: str):
        """Automatically append high-quality interactions to train_tool_use.jsonl dataset!"""
        try:
            entry = {
                "messages": [
                    {"role": "system", "content": "Sen Abdulaziz Agent - Otajonov Abdulaziz tomonidan yaratilgan avtonom AI proger va dizaynersan."},
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": agent_reply}
                ]
            }
            with open(self.dataset_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            print(f"💾 [Live Harvest] Suhbat datasetga o'zlashtirildi! ({self.dataset_path})")
        except Exception as e:
            print(f"[Harvest Xato]: {str(e)}")

    def run(self):
        if not self.token:
            print("⚠️ [Diqqat] TELEGRAM_BOT_TOKEN topilmadi! Iltimos .env faylga token qo'shing.")
            return

        print("======================================================")
        print("   👑 ABDULAZIZ AGENT — TELEGRAM BOT ISHGA TUSHDI!   ")
        print("   Yaratuvchi: Otajonov Abdulaziz                     ")
        print("   Miya: OpenRouter Zero-Cost Pool + Ollama Fallback  ")
        print("======================================================")
        
        while True:
            try:
                res = self._send_request("getUpdates", {"offset": self.offset, "timeout": 30})
                if res.get("ok") and res.get("result"):
                    for update in res["result"]:
                        self.offset = update["update_id"] + 1
                        msg = update.get("message") or update.get("edited_message")
                        if not msg or "text" not in msg:
                            continue
                            
                        chat_id = msg["chat"]["id"]
                        user_text = msg["text"].strip()
                        sender_name = msg.get("from", {}).get("first_name", "Foydalanuvchi")
                        
                        print(f"\n📩 [Telegram] {sender_name} ({chat_id}): {user_text}")
                        
                        # Send typing indicator
                        self._send_request("sendChatAction", {"chat_id": chat_id, "action": "typing"})
                        
                        if user_text == "/start":
                            welcome = (
                                "👑 **Assalomu alaykum! Men Abdulaziz Agent — Otajonov Abdulazizning shaxsiy AI hamkoriman!**\n\n"
                                "🚀 Men **Claude Code** darajasida buyruqlar yozadigan, fayllaringizni avtonom tahrirlab, 400+ pro dizayn kitoblari asosida "
                                "bir ko'rishda WOW-effekt beradigan Glassmorphism saytlari yaratadigan avtonom hamkoringizman!\n\n"
                                "👉 Menga buyruq bering yoki yangi tizim buyruqlaridan foydalaning:\n"
                                "`/sysinfo` — Kompyuter xotirasi va tizim holatini tahlil qilish\n"
                                "`/scan [papka]` — Istalgan papka va fayllarni tahlil qilish\n"
                                "`/run [cmd]` — PowerShell buyruqlarini bevosita bajarish"
                            )
                            self.send_message(chat_id, welcome)
                            continue
                        elif user_text == "/sysinfo":
                            info_cmd = 'Get-WmiObject Win32_OperatingSystem | Select-Object Caption, FreePhysicalMemory, TotalVisibleMemorySize; Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{n="UsedGB";e={[math]::round($_.Used/1GB,2)}}, @{n="FreeGB";e={[math]::round($_.Free/1GB,2)}}'
                            res = run_powershell_command(info_cmd)
                            out = (res.get("stdout", "") or res.get("stderr", "") or "Tahlil yakunlandi.").strip()
                            self.send_message(chat_id, f"🖥️ **[Kompyuter Tizimining Tahlili]:**\n```\n{out}\n```")
                            continue
                        elif user_text.startswith("/scan "):
                            folder = user_text[6:].strip().strip('"')
                            scan_cmd = f'Get-ChildItem -LiteralPath "{folder}" -Force | Select-Object Name, Length, LastWriteTime | Select-Object -First 25'
                            res = run_powershell_command(scan_cmd)
                            out = (res.get("stdout", "") or res.get("stderr", "") or "Papkada fayl topilmadi yoki yo'l xato.").strip()
                            self.send_message(chat_id, f"📂 **[{folder} Papkasining Tahlili]:**\n```\n{out}\n```")
                            continue
                        elif user_text.startswith("/run "):
                            cmd = user_text[5:].strip()
                            res = run_powershell_command(cmd)
                            out = (res.get("stdout", "") or res.get("stderr", "") or "Buyruq bajarildi (ekranga matn chiqmaydi).").strip()
                            self.send_message(chat_id, f"⚡ **[PowerShell Natijasi]:**\n```\n{out[:3000]}\n```")
                            continue
                        
                        # Process turn with Abdulaziz Agent Engine
                        start_time = time.time()
                        reply = self.engine.execute_turn(user_text)
                        elapsed = round(time.time() - start_time, 2)
                        
                        print(f"✅ [Natija] {elapsed} soniyada javob yuborildi.")
                        self.send_message(chat_id, reply)
                        
                        # Live harvest to dataset
                        self.save_live_harvest(user_text, reply)
            except KeyboardInterrupt:
                print("\n🛑 Telegram bot to'xtatildi.")
                break
            except Exception as e:
                time.sleep(2)

if __name__ == "__main__":
    bot = AbdulazizTelegramBot()
    bot.run()
