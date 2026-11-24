@echo off
title AI Fake Identity Screening System - Online Public Share
echo ===================================================================
echo   AI Fake Identity & Document Screening System (Online Share)
echo ===================================================================
echo.

cd /d "%~dp0"

echo [1/2] Starting FastAPI Backend Server on port 8000...
start "AI Document Screening Backend" cmd /k "python run.py"

echo [2/2] Launching Cloudflare Tunnel to create a public HTTPS link...
echo (Anyone anywhere on 4G/5G/cellular or Wi-Fi can open this link on phone or PC!)
echo.
echo ===================================================================
echo Look for the link ending in: .trycloudflare.com
echo Copy and share that URL with anyone to test the app!
echo ===================================================================
echo.

if exist "cloudflared.exe" (
    cloudflared.exe tunnel --url http://127.0.0.1:8000
) else if exist "%USERPROFILE%\AG01\cloudflared.exe" (
    "%USERPROFILE%\AG01\cloudflared.exe" tunnel --url http://127.0.0.1:8000
) else (
    echo Cloudflared not found. Starting local server only.
    python run.py
)

pause
