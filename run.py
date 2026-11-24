#!/usr/bin/env python3
"""
AI Fake Identity & Document Screening System
Entry point to run both the Backend API and Web Frontend.
Supports access from Local PC and Mobile Phones on the same Wi-Fi network.
"""

import sys
import os
import socket
import webbrowser
from pathlib import Path

# Add backend directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "backend"))

import uvicorn
from app.database import init_db
from samples.generate_samples import (
    generate_all_samples,
    SAMPLES_DIR
)

def get_local_ip():
    """Detects the computer's Wi-Fi / Local Area Network IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not send actual traffic, just routes to determine local network interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def setup_environment():
    print("=" * 70)
    print("   AI Fake Identity & Document Screening System")
    print("   Mobile & Desktop Accessible Platform")
    print("=" * 70)
    
    # 1. Initialize SQLite Database
    print("[1/3] Initializing local database...")
    init_db()

    # 2. Check / Generate Sample Documents
    print("[2/3] Checking test sample documents...")
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    if not (SAMPLES_DIR / "sample_voter_clean.png").exists() or not (SAMPLES_DIR / "sample_passport_clean.png").exists():
        print("      Generating sample test identity documents...")
        generate_all_samples()
    print("      Samples verified.")

    # 3. Detect Network IP & Launch Server
    port = 8000
    host = "0.0.0.0"  # Binds to all network interfaces so phones can connect
    local_ip = get_local_ip()

    print("[3/3] Starting web server on all network interfaces...")
    print("=" * 70)
    print(f"  💻 On this PC:     http://localhost:{port}")
    print(f"  📱 On your Phone:  http://{local_ip}:{port}")
    print("=" * 70)
    print("  NOTE FOR PHONE ACCESS:")
    print("  1. Make sure your phone is connected to the same Wi-Fi network.")
    print(f"  2. Open your phone's browser and type: http://{local_ip}:{port}")
    print("=" * 70)
    print("  Press CTRL+C in this terminal window to stop the server.")
    print("=" * 70)

    # Attempt to open PC browser
    try:
        webbrowser.open(f"http://localhost:{port}")
    except Exception:
        pass

    uvicorn.run("app.main:app", host=host, port=port, reload=False, log_level="info")

if __name__ == "__main__":
    setup_environment()
