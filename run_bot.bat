@echo off
chcp 65001 >nul
title 👑 ABDULAZIZ AGENT — TELEGRAM BOT
color 0A
echo ======================================================
echo    👑 ABDULAZIZ AGENT — TELEGRAM BOT ISHGA TUSHDI!   
echo    Yaratuvchi: Otajonov Abdulaziz                     
echo    Miya: OpenRouter Zero-Cost Pool + Ollama Fallback  
echo ======================================================
echo.
cd /d "D:\3D AI\Abdulaziz-Agent"
set PYTHONIOENCODING=utf-8
"D:\3D AI\Новая папка\VD\AI MODEL\hermes-agent-main\hermes-agent-main\.venv\Scripts\python.exe" -X utf8 engine/telegram_bot.py
pause
