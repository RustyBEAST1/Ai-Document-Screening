import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
SAMPLES_DIR = BASE_DIR / "samples"
DB_PATH = BASE_DIR / "screening.db"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_DOCUMENT_TYPES = [
    "Aadhaar Card",
    "PAN Card",
    "Driving Licence",
    "Voter ID Card",
    "Passport",
]

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".pdf", ".bmp"}
MAX_FILE_SIZE_MB = 15

DISCLAIMER_TEXT = (
    "This tool provides an AI-based preliminary screening only. "
    "It does not replace official government verification, KYC checks, or human review."
)

# Risk Thresholds
RISK_THRESHOLD_LOW = 35
RISK_THRESHOLD_MEDIUM = 69
