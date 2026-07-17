@echo off
chcp 65001 >nul
title 👑 ABDULAZIZ AGENT — BULUTGA VA GITHUBGA AVTOMAT ULASH
color 0A
set PATH=%PATH%;C:\Program Files\GitHub CLI
echo ======================================================
echo    👑 ABDULAZIZ AGENT — 1-BOSISHDA BULUTGA ULASH     
echo    Yaratuvchi: Otajonov Abdulaziz                     
echo ======================================================
echo.
echo [1/3] 🌐 GitHub tizimiga ulanish tekshirilmoqda...
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 🔑 Hozir brauzeringiz ochilmoqda! Iltimos, GitHub hisobingiz bilan kirib ruxsat berish (Authorize) tugmasini bosing...
    echo.
    gh auth login --web
)

echo.
echo [2/3] 🚀 Abdulaziz-Agent loyihasi GitHub bulutida avtomatik yaratib, kodlar yuklanmoqda...
cd /d "D:\3D AI\Abdulaziz-Agent"
gh repo create Abdulaziz-Agent --public --source=. --remote=origin --push

echo.
echo [3/3] ☁️ 24/7 Bepul Bulutli Serverga (Render.com) o'tilmoqda...
echo.
echo ======================================================
echo ✅ KODLAR GITHUB'GA 100% YUKLANDI!
echo ======================================================
echo.
echo Endi ochilgan Render.com sahifasida:
echo 1. "New" -> "Background Worker" bosing.
echo 2. "Abdulaziz-Agent" repozitoriyangizni tanlang.
echo 3. Start Command bo'limiga: python main.py
echo 4. Environment Variables bo'limiga maxfiy kalitlaringizni kiriting va Create bosing!
echo.
echo 🌐 Render sahifasi ochilmoqda...
start https://dashboard.render.com
pause
