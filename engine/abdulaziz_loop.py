import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from typing import List, Dict, Any

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from tools.file_ops import view_file_lines, replace_code_chunk, search_workspace
from tools.terminal_ops import run_powershell_command

class AbdulazizAgentEngine:
    """
    Abdulaziz Agent — Autonomous AI Coding & Design Assistant
    Created by Otajonov Abdulaziz.
    Combines Claude Code's pair programming loop with 400+ UI/UX design book knowledge.
    """
    def __init__(self, config_path: str = "D:\\3D AI\\Abdulaziz-Agent\\engine\\config.json"):
        self._load_env_keys()
        self.config = self._load_config(config_path)
        self.agent_name = self.config.get("agent_name", "Abdulaziz Agent")
        self.creator = self.config.get("creator", "Otajonov Abdulaziz")
        self.cloud_models = self.config.get("engines", {}).get("cloud_free_pool", [])
        self.local_model = self.config.get("engines", {}).get("local_offline_model", {}).get("model", "qwen2.5-coder:1.5b")
        self.design_lib_path = self.config.get("knowledge_base", {}).get("design_ui_ux_path", "")
        self.conversation_history: List[Dict[str, Any]] = []
        
    def _load_env_keys(self):
        """Automatically load OPENROUTER_API_KEY and other keys from .env files."""
        for env_path in ["C:\\Users\\Smart\\AppData\\Local\\hermes\\.env", "D:\\3D AI\\Abdulaziz-Agent\\.env"]:
            if os.path.exists(env_path):
                try:
                    with open(env_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if '=' in line and not line.strip().startswith('#'):
                                k, v = line.strip().split('=', 1)
                                if k and not os.getenv(k):
                                    os.environ[k] = v
                except Exception:
                    pass
        
    def _load_config(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _get_system_prompt(self) -> str:
        return f"""You are {self.agent_name}, created by {self.creator}. You are a state-of-the-art autonomous AI coding and design assistant engineered to match and surpass Claude Code.

### RULES & CAPABILITIES:
1. **Pair Programming Loop:** You autonomously inspect code (`view_file_lines`), search codebases (`search_workspace`), make exact diff edits (`replace_code_chunk`), and run terminal tests (`run_powershell_command`). If a command returns an error, you must read the `stderr` and fix the bug immediately without giving up.
2. **Premium Web Aesthetics & Glassmorphism:** Whenever tasked with creating or editing a web interface (HTML/CSS/JS/Web App), YOU MUST apply vibrant, sleek designs, Glassmorphism (`backdrop-filter: blur(16px); background: rgba(255, 255, 255, 0.05);`), modern dark themes (`#0a0a0f`), Google Fonts (`Inter`, `Outfit`), and smooth hover micro-animations (`transition: all 0.3s cubic-bezier`). Never produce plain or ugly 1990s HTML.
3. **400+ UI/UX Book Library Access:** You apply principles from Refactoring UI, Laws of UX, and Color Theory to every visual structure.
4. **Language Purity (Standard Uzbek):** You must ALWAYS respond in standard, high-literary, clear Uzbek language using strict Latin script (`a-z`, `o'`, `g'`, `sh`, `ch`). You have full comprehension of inputs written in English and Russian (and can read/analyze English and Russian documentation/code seamlessly), but your explanation and dialogue output to the user must always be in Standard Uzbek. Do not use dialect/Khorezmian slang.
5. **Pro Backend & Full-Stack Mastery:** When tasked with creating backend code, APIs, or full-stack web applications, you are an expert in Python (`FastAPI`, `Flask`, `Django`), Node.js (`Express`), and SQLite/PostgreSQL databases. Write clean REST API endpoints (`GET /api/menu`, `POST /api/orders`), integrate database schemas cleanly, and connect the frontend Glassmorphism UI to the backend via modern `fetch()` or `axios` requests.
6. **Warm Communication & Explicit URL Presentation:** Always communicate with genuine warmth, friendly enthusiasm, and encouraging words right from the start to the end of your response (just like Otajonov Abdulaziz's most loyal and motivating AI partner!). Furthermore, whenever you create web interfaces, backends, or local servers, YOU MUST explicitly provide a clear, dedicated summary section listing the exact clickable URL addresses (e.g., `http://localhost:3000`, `http://localhost:8000/docs`, or exact API endpoints) so the user can immediately click, open, and verify them without guessing.
7. **Windows System Analyzer & Automation Mastery:** You have direct access to run commands on the user's Windows PC. When asked to inspect the computer (`Kompyuterni tahlil qil`), check files/RAM/disk, clean folders, or automate workflows, you must write clean PowerShell or Python scripts enclosed within `<powershell>` ... `</powershell>` (or `<python>` ... `</python>`) tags. The engine will automatically execute your script right on the user's computer and return the real output directly to Telegram! CRITICAL RULE: All scripts run in a non-interactive background process. NEVER include `Read-Host`, `input()`, `pause`, `$input`, or any interactive console questions inside your `<powershell>` or `<python>` scripts. Automate the task completely without stopping for user input. Always explain what action you are taking clearly and warmly.
8. **Multi-Step Self-Healing Architecture:** If a `<powershell>` or `<python>` script you generate encounters an error (`SyntaxError`, `Access Denied`, or unexpected output), do not give up or apologize passively. Inspect the `stderr` or error trace, analyze the bug autonomously, and output a corrected `<powershell>` or `<python>` script to fix the issue on the spot.
9. **Live Web & Data Collector:** When asked to gather web data, exchange rates, news, or site content, write Python scripts using `urllib`, `requests`, or `BeautifulSoup` inside `<python>` tags to fetch, parse, and summarize real-time web data cleanly and deliver the summarized report directly to the user on Telegram.
10. **Long-Term Memory & User Preferences:** You remember Otajonov Abdulaziz's core habits (`Glassmorphism dark mode #0a0a0f`, standard paths like `D:\3D AI\Abdulaziz-Agent`, Standard Uzbek language). Whenever tasked with storing or recalling habits, read or write from `D:\3D AI\Abdulaziz-Agent\brain_memory.json`.
11. **Destructive Command Guardrails:** Safety comes first! Never execute scripts that wipe entire drives, format disks (`Format-Volume`), recursively delete `C:\Windows`, or delete major project directories without explicitly warning the user first and verifying their confirmation.
12. **GUI & Screen Vision Automation:** When tasks require desktop GUI interaction (clicking buttons inside apps or web browsers where CLI is impossible), write Python scripts using `pyautogui` or `win32api` inside `<python>` tags to take screenshots, inspect screen coordinates, and move/click smoothly like a human."""


    def call_model(self, prompt: str) -> str:
        """Call zero-cost cloud engine via OpenRouter, falling back to local Ollama if offline."""
        messages = [{"role": "system", "content": self._get_system_prompt()}]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        # 1. Try free cloud models first (Zero-cost pool)
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if api_key:
            for model_id in self.cloud_models:
                for attempt in range(2):
                    try:
                        req_body = json.dumps({"model": model_id, "messages": messages}).encode('utf-8')
                        req = urllib.request.Request(
                            "https://openrouter.ai/api/v1/chat/completions",
                            data=req_body,
                            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                        )
                        with urllib.request.urlopen(req, timeout=35) as resp:
                            res_json = json.loads(resp.read().decode('utf-8'))
                            reply = res_json["choices"][0]["message"]["content"]
                            self.conversation_history.append({"role": "user", "content": prompt})
                            self.conversation_history.append({"role": "assistant", "content": reply})
                            return reply
                    except Exception as e:
                        time.sleep(1.5)
                        continue
        
        # 2. Fallback to offline Ollama model (`0% cost, 0 MB internet`)
        try:
            req_body = json.dumps({"model": self.local_model, "messages": messages, "stream": False}).encode('utf-8')
            req = urllib.request.Request(
                "http://localhost:11434/api/chat",
                data=req_body,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=40) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                reply = res_json["message"]["content"]
                self.conversation_history.append({"role": "user", "content": prompt})
                self.conversation_history.append({"role": "assistant", "content": reply})
                return f"[Oflayn Ollama Motori — {self.local_model}]\n{reply}"
        except Exception as e:
            return f"⚠️ [Diqqat] Bulutli API kaliti va Oflayn Ollama motori topilmadi. Iltimos Ollama ishga tushiring yoki OpenRouter kalitini o'rnating. Xato: {str(e)}"

    def execute_turn(self, user_prompt: str) -> str:
        """Execute a full pair programming loop turn, automatically running extracted scripts."""
        print(f"\n🚀 [Abdulaziz Agent] Yangi vazifa qabul qilindi: '{user_prompt}'")
        response = self.call_model(user_prompt)
        
        # Check for powershell automation execution requests
        ps_matches = re.findall(r'<powershell>(.*?)</powershell>', response, re.DOTALL | re.IGNORECASE)
        for ps_code in ps_matches:
            ps_code_clean = ps_code.strip()
            print(f"\n⚡ [Tizim Avtomatlashtirish] PowerShell buyruq bajarilmoqda:\n{ps_code_clean}")
            cmd_res = run_powershell_command(ps_code_clean)
            out_str = (cmd_res.get("stdout", "") or cmd_res.get("stderr", "") or "Bajarildi.").strip()
            response += f"\n\n⚡ **[Windows Tizimidan Amaliy Natija]:**\n```\n{out_str[:1500]}\n```"
            
        # Check for python automation execution requests
        py_matches = re.findall(r'<python>(.*?)</python>', response, re.DOTALL | re.IGNORECASE)
        for py_code in py_matches:
            py_code_clean = py_code.strip()
            print(f"\n🐍 [Tizim Avtomatlashtirish] Python skript bajarilmoqda...")
            escaped_py = py_code_clean.replace('"', '\\"')
            cmd_res = run_powershell_command(f'python -c "{escaped_py}"')
            out_str = (cmd_res.get("stdout", "") or cmd_res.get("stderr", "") or "Bajarildi.").strip()
            response += f"\n\n🐍 **[Python Avtomatlashtirish Natijasi]:**\n```\n{out_str[:1500]}\n```"
            
        return response

if __name__ == "__main__":
    agent = AbdulazizAgentEngine()
    print("======================================================")
    print("   👑 ABDULAZIZ AGENT v1.0 — CLAUDE CODE KILLER      ")
    print("   Yaratuvchi: Otajonov Abdulaziz                     ")
    print("======================================================")
    if len(sys.argv) > 1:
        res = agent.execute_turn(" ".join(sys.argv[1:]))
        print(res)
    else:
        print("Tizim tayyor. Buyruqni parametr sifatida yuboring.")
