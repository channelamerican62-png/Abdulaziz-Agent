@echo off
chcp 65001 >nul
title 👑 ABDULAZIZ AGENT — GITHUB AUTO-BACKUP
color 0B
echo ======================================================
echo    👑 ABDULAZIZ AGENT — GITHUB BULUTGA SAQLASH       
echo    Yaratuvchi: Otajonov Abdulaziz                     
echo ======================================================
echo.
cd /d "D:\3D AI\Abdulaziz-Agent"
git add .
set /p msg="O'zgarish haqida izoh yozing (yoki Enter bosing): "
if "%msg%"=="" set msg=🔄 Avtomat zaxira nusxasi (Cloud Sync)
git commit -m "%msg%"
echo.
echo 🚀 GitHub bulutiga yuklanmoqda...
git push -u origin main
echo.
echo ======================================================
echo ✅ Barcha kodlar GitHub bulutiga muvaffaqiyatli saqlandi!
echo ======================================================
pause
