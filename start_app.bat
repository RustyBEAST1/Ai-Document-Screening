@echo off
title AI Fake Identity & Document Screening System
cls
echo ===================================================================
echo    AI Fake Identity & Document Screening System
echo    Preliminary Forensic & Tampering Verification Platform
echo ===================================================================
echo.
echo  Starting local application server on http://127.0.0.1:8000 ...
echo.
python run.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application exited with code %ERRORLEVEL%.
    echo Please make sure Python is installed and run 'pip install -r requirements.txt'.
    echo.
    pause
)
