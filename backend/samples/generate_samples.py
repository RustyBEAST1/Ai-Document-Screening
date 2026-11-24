import cv2
import numpy as np
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.validators.verhoeff import generate_verhoeff
from app.validators.passport import compute_mrz_checksum

SAMPLES_DIR = Path(__file__).resolve().parent
DEMO_DIR = SAMPLES_DIR.parent.parent / "demo_samples"

def draw_realistic_photo_box(img: np.ndarray, x: int, y: int, w: int, h: int):
    """Draws a portrait photo box with gradient facial features and photo border."""
    cv2.rectangle(img, (x, y), (x + w, y + h), (210, 215, 220), -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), (90, 95, 100), 2)
    # Face head
    center = (x + w // 2, y + int(h * 0.40))
    cv2.ellipse(img, center, (int(w * 0.32), int(h * 0.28)), 0, 0, 360, (180, 160, 140), -1)
    # Hair
    cv2.ellipse(img, (x + w // 2, y + int(h * 0.22)), (int(w * 0.34), int(h * 0.16)), 0, 180, 360, (40, 30, 25), -1)
    # Eyes
    ey = y + int(h * 0.38)
    cv2.circle(img, (x + int(w * 0.36), ey), int(w * 0.05), (30, 30, 30), -1)
    cv2.circle(img, (x + int(w * 0.64), ey), int(w * 0.05), (30, 30, 30), -1)
    # Eyebrows
    cv2.line(img, (x + int(w * 0.28), ey - 8), (x + int(w * 0.44), ey - 8), (40, 30, 20), 2)
    cv2.line(img, (x + int(w * 0.56), ey - 8), (x + int(w * 0.72), ey - 8), (40, 30, 20), 2)
    # Nose
    cv2.line(img, (x + w // 2, ey), (x + w // 2, ey + int(h * 0.12)), (140, 110, 90), 2)
    # Mouth
    cv2.line(img, (x + int(w * 0.40), ey + int(h * 0.17)), (x + int(w * 0.60), ey + int(h * 0.17)), (120, 70, 70), 2)
    # Shoulders
    cv2.ellipse(img, (x + w // 2, y + h + int(h * 0.15)), (int(w * 0.55), int(h * 0.40)), 0, 180, 360, (50, 70, 110), -1)

def draw_clean_qr(img: np.ndarray, x: int, y: int, size: int):
    """Draws a clean scannable QR pattern."""
    cv2.rectangle(img, (x, y), (x + size, y + size), (250, 250, 250), -1)
    cv2.rectangle(img, (x, y), (x + size, y + size), (0, 0, 0), 2)
    corners = [(x + 4, y + 4), (x + size - 28, y + 4), (x + 4, y + size - 28)]
    for cx, cy in corners:
        cv2.rectangle(img, (cx, cy), (cx + 24, cy + 24), (0, 0, 0), -1)
        cv2.rectangle(img, (cx + 4, cy + 4), (cx + 20, cy + 20), (255, 255, 255), -1)
        cv2.rectangle(img, (cx + 8, cy + 8), (cx + 16, cy + 16), (0, 0, 0), -1)
    np.random.seed(101)
    for _ in range(40):
        rx = np.random.randint(x + 28, x + size - 12)
        ry = np.random.randint(y + 28, y + size - 12)
        cv2.rectangle(img, (rx, ry), (rx + 5, ry + 5), (0, 0, 0), -1)

# ==========================================
# 1. AADHAAR CARD (Authentic & Tampered)
# ==========================================

def generate_clean_aadhaar():
    """Authentic Aadhaar Card with valid Verhoeff checksum and clean layout."""
    w, h = 1000, 630
    img = np.ones((h, w, 3), dtype=np.uint8)
    img[:, :] = (242, 244, 243)
    
    cv2.rectangle(img, (10, 10), (w - 10, h - 10), (180, 185, 190), 2)
    
    # Red & Green Aadhaar header bands
    cv2.rectangle(img, (12, 12), (w - 12, 45), (20, 120, 230), -1)
    cv2.rectangle(img, (12, 45), (w - 12, 60), (220, 220, 220), -1)
    cv2.rectangle(img, (12, 60), (w - 12, 85), (50, 160, 50), -1)
    
    cv2.putText(img, "GOVERNMENT OF INDIA", (280, 125), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (20, 20, 20), 3)
    cv2.putText(img, "UNIQUE IDENTIFICATION AUTHORITY OF INDIA", (210, 158), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (70, 70, 70), 2)
    
    draw_realistic_photo_box(img, 60, 190, 175, 225)
    
    cv2.putText(img, "Name: ARUN KUMAR SHARMA", (270, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    cv2.putText(img, "DOB: 15/08/1992", (270, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Gender: MALE", (270, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    
    # 12-digit number with valid Verhoeff checksum
    base11 = "54829104372"
    chk = generate_verhoeff(base11)
    valid_aadhaar = f"{base11[:4]} {base11[4:8]} {base11[8:]}{chk}"
    
    cv2.rectangle(img, (180, 480), (820, 555), (235, 238, 240), -1)
    cv2.rectangle(img, (180, 480), (820, 555), (190, 195, 200), 2)
    cv2.putText(img, valid_aadhaar, (220, 535), cv2.FONT_HERSHEY_SIMPLEX, 1.45, (20, 20, 180), 3)
    
    draw_clean_qr(img, 760, 200, 180)
    
    cv2.putText(img, "Mera Aadhaar, Meri Pehchan", (340, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (100, 100, 100), 2)
    
    out_path = SAMPLES_DIR / "sample_aadhaar_clean.png"
    cv2.imwrite(str(out_path), img)
    return out_path

def generate_tampered_aadhaar():
    """Tampered Aadhaar Card with invalid Verhoeff checksum and spliced number box."""
    w, h = 1000, 630
    img = np.ones((h, w, 3), dtype=np.uint8)
    img[:, :] = (242, 244, 243)
    
    cv2.rectangle(img, (10, 10), (w - 10, h - 10), (180, 185, 190), 2)
    
    cv2.rectangle(img, (12, 12), (w - 12, 45), (20, 120, 230), -1)
    cv2.rectangle(img, (12, 45), (w - 12, 60), (220, 220, 220), -1)
    cv2.rectangle(img, (12, 60), (w - 12, 85), (50, 160, 50), -1)
    
    cv2.putText(img, "GOVERNMENT OF INDIA", (280, 125), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (20, 20, 20), 3)
    cv2.putText(img, "UNIQUE IDENTIFICATION AUTHORITY OF INDIA", (210, 158), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (70, 70, 70), 2)
    
    draw_realistic_photo_box(img, 60, 190, 175, 225)
    
    cv2.putText(img, "Name: ANIL VERMA", (270, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    cv2.putText(img, "DOB: 22/07/1989", (270, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Gender: MALE", (270, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    
    # Spliced Aadhaar Number Patch with high ELA noise and INVALID checksum
    # 5482 9104 3729 (correct is 3, 9 fails Verhoeff)
    cv2.rectangle(img, (180, 480), (820, 555), (255, 255, 255), -1)
    noise = np.random.normal(0, 30, (75, 640, 3)).astype(np.uint8)
    img[480:555, 180:820] = cv2.add(img[480:555, 180:820], noise)
    cv2.rectangle(img, (180, 480), (820, 555), (100, 100, 100), 2)
    cv2.putText(img, "5482 9104 3729", (220, 535), cv2.FONT_HERSHEY_TRIPLEX, 1.45, (160, 0, 0), 3)
    
    draw_clean_qr(img, 760, 200, 180)
    cv2.putText(img, "Mera Aadhaar, Meri Pehchan", (340, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (100, 100, 100), 2)
    
    out_path = SAMPLES_DIR / "sample_aadhaar_tampered.png"
    cv2.imwrite(str(out_path), img)
    return out_path

# ==========================================
# 2. PAN CARD (Authentic & Tampered)
# ==========================================

def generate_clean_pan():
    """Authentic PAN Card with valid syntax ABCPS2345F and entity 'P'."""
    w, h = 950, 600
    img = np.ones((h, w, 3), dtype=np.uint8)
    img[:, :] = (235, 242, 238)
    
    cv2.rectangle(img, (10, 10), (w - 10, h - 10), (170, 185, 175), 2)
    cv2.putText(img, "INCOME TAX DEPARTMENT", (260, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (120, 30, 20), 3)
    cv2.putText(img, "GOVT. OF INDIA", (380, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (60, 60, 60), 2)
    
    draw_realistic_photo_box(img, 50, 150, 160, 210)
    
    cv2.putText(img, "Name / Naam", (260, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    cv2.putText(img, "SURESH SHARMA", (260, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    
    cv2.putText(img, "Father's Name", (260, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    cv2.putText(img, "RAMESH SHARMA", (260, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    
    cv2.putText(img, "Date of Birth", (260, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    cv2.putText(img, "12/05/1988", (260, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    
    # Valid PAN format: ABCPS2345F ('P' = Individual, 'S' = Sharma)
    cv2.putText(img, "Permanent Account Number", (260, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80, 80, 80), 1)
    cv2.putText(img, "ABCPS2345F", (260, 490), cv2.FONT_HERSHEY_DUPLEX, 1.25, (0, 0, 0), 3)
    
    # Signature Box
    cv2.rectangle(img, (50, 400), (210, 470), (250, 250, 250), -1)
    cv2.rectangle(img, (50, 400), (210, 470), (180, 180, 180), 1)
    cv2.putText(img, "Suresh", (65, 445), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.9, (20, 20, 100), 2)
    cv2.putText(img, "Signature", (95, 495), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
    
    out_path = SAMPLES_DIR / "sample_pan_clean.png"
    cv2.imwrite(str(out_path), img)
    return out_path

def generate_tampered_pan():
    """Tampered PAN Card with altered DOB patch and invalid entity code 'X'."""
    w, h = 950, 600
    img = np.ones((h, w, 3), dtype=np.uint8)
    img[:, :] = (230, 240, 235)
    
    cv2.putText(img, "INCOME TAX DEPARTMENT", (260, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (120, 30, 20), 3)
    cv2.putText(img, "GOVT. OF INDIA", (380, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (60, 60, 60), 2)
    
    draw_realistic_photo_box(img, 50, 150, 160, 210)
    
    cv2.putText(img, "Name / Naam", (260, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    cv2.putText(img, "VIKRAM SINGH", (260, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    
    cv2.putText(img, "Father's Name", (260, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    cv2.putText(img, "RAJENDRA SINGH", (260, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
    
    cv2.putText(img, "Date of Birth", (260, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    
    # Tampered patch over DOB
    cv2.rectangle(img, (255, 350), (520, 405), (255, 255, 255), -1)
    noise = np.random.normal(0, 35, (55, 265, 3)).astype(np.uint8)
    img[350:405, 255:520] = cv2.add(img[350:405, 255:520], noise)
    cv2.putText(img, "10/02/1985", (270, 395), cv2.FONT_HERSHEY_TRIPLEX, 1.1, (20, 0, 180), 2)
    
    # Invalid PAN 4th char 'X'
    cv2.putText(img, "Permanent Account Number", (260, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80, 80, 80), 1)
    cv2.putText(img, "ABCXE9874F", (260, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)
    
    out_path = SAMPLES_DIR / "sample_pan_tampered.png"
    cv2.imwrite(str(out_path), img)
    return out_path

# ==========================================
# 3. DRIVING LICENCE (Authentic & Blurry)
# ==========================================

def generate_clean_dl():
    """Authentic Driving Licence with standard Sarathi format (DL0420210012345)."""
    w, h = 920, 580
    img = np.ones((h, w, 3), dtype=np.uint8)
    img[:, :] = (238, 244, 248)
    
    cv2.rectangle(img, (10, 10), (w - 10, h - 10), (170, 185, 200), 2)
    cv2.rectangle(img, (12, 12), (w - 12, 50), (30, 60, 120), -1)
    cv2.putText(img, "UNION OF INDIA - DRIVING LICENCE", (180, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2)
    cv2.putText(img, "DELHI TRANSPORT DEPARTMENT", (260, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (60, 60, 80), 2)
    
    draw_realistic_photo_box(img, 50, 120, 160, 205)
    
    # Sarathi DL Format: DL04 2021 0012345
    cv2.putText(img, "DL No: DL04 2021 0012345", (245, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (10, 10, 80), 2)
    cv2.putText(img, "Name: ROHIT SHARMA", (245, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "DOB: 18/06/1990", (245, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "Issue Date: 12/01/2021", (245, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
    cv2.putText(img, "Authorised to Drive: LMV, MCWG", (245, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
    cv2.putText(img, "Validity: 17/06/2040", (245, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
    
    # Clean Smart Card Chip
    cv2.rectangle(img, (50, 360), (130, 430), (200, 190, 130), -1)
    cv2.rectangle(img, (50, 360), (130, 430), (140, 130, 80), 2)
    cv2.rectangle(img, (75, 375), (105, 415), (170, 160, 100), -1)
    
    out_path = SAMPLES_DIR / "sample_dl_clean.png"
    cv2.imwrite(str(out_path), img)
    return out_path

def generate_blurry_dl():
    """Blurry Driving Licence with glare hotspot and heavy Gaussian blur."""
    w, h = 900, 560
    img = np.ones((h, w, 3), dtype=np.uint8) * 240
    
    cv2.putText(img, "UNION OF INDIA - DRIVING LICENCE", (150, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (20, 20, 120), 2)
    cv2.putText(img, "DELHI TRANSPORT DEPARTMENT", (260, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80, 80, 80), 2)
    
    draw_realistic_photo_box(img, 50, 140, 150, 190)
    
    cv2.putText(img, "DL No: DL0420180012345", (240, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (0, 0, 0), 2)
    cv2.putText(img, "Name: MANISH GUPTA", (240, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "DOB: 24/11/1988", (240, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "Authorised to Drive: LMV, MCWG", (240, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
    
    # Glare hotspot
    cv2.circle(img, (760, 140), 110, (255, 255, 255), -1)
    
    # Heavy blur
    blurred = cv2.GaussianBlur(img, (31, 31), 9.0)
    
    out_path = SAMPLES_DIR / "sample_dl_blurry.png"
    cv2.imwrite(str(out_path), blurred)
    return out_path

# ==========================================
# 4. VOTER ID CARD (Authentic & Tampered)
# ==========================================

def generate_clean_voter():
    """Authentic Voter ID Card with standard ECI EPIC format (WBF2345678)."""
    w, h = 900, 580
    img = np.ones((h, w, 3), dtype=np.uint8)
    img[:, :] = (244, 248, 240)
    
    cv2.rectangle(img, (10, 10), (w - 10, h - 10), (160, 180, 170), 2)
    cv2.rectangle(img, (12, 12), (w - 12, 55), (180, 70, 30), -1)
    cv2.putText(img, "ELECTION COMMISSION OF INDIA", (180, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (255, 255, 255), 2)
    cv2.putText(img, "ELECTOR PHOTO IDENTITY CARD", (240, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.78, (30, 30, 30), 2)
    
    draw_realistic_photo_box(img, 50, 130, 165, 210)
    
    # EPIC Box: 3 letters + 7 digits
    cv2.rectangle(img, (250, 130), (620, 185), (230, 238, 230), -1)
    cv2.rectangle(img, (250, 130), (620, 185), (140, 160, 140), 2)
    cv2.putText(img, "EPIC: WBF2345678", (265, 172), cv2.FONT_HERSHEY_DUPLEX, 1.05, (10, 10, 120), 2)
    
    cv2.putText(img, "Elector's Name: RAJESH VERMA", (250, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Father's Name: SURESH VERMA", (250, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Gender: MALE", (250, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "DOB / Age: 28", (250, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Official ECI Stamp Circle
    cv2.circle(img, (760, 270), 75, (180, 60, 40), 2)
    cv2.circle(img, (760, 270), 65, (180, 60, 40), 1)
    cv2.putText(img, "BHARAT", (725, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (180, 60, 40), 1)
    cv2.putText(img, "NIRVACHAN", (710, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 60, 40), 1)
    
    cv2.putText(img, "IDENTITY CARD", (350, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (120, 120, 120), 2)
    
    out_path = SAMPLES_DIR / "sample_voter_clean.png"
    cv2.imwrite(str(out_path), img)
    return out_path

def generate_tampered_voter():
    """Tampered Voter ID Card with irregular EPIC format and spliced photo box."""
    w, h = 900, 580
    img = np.ones((h, w, 3), dtype=np.uint8)
    img[:, :] = (240, 240, 240)
    
    # Missing standard English header "ELECTION COMMISSION OF INDIA"
    cv2.putText(img, "BHARAT NIRVACHAN AYOG", (220, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (120, 30, 20), 2)
    cv2.putText(img, "IDENTITY CARD", (330, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (80, 80, 80), 2)
    
    # Tampered photo box with mismatched seam
    draw_realistic_photo_box(img, 50, 130, 165, 210)
    cv2.rectangle(img, (45, 125), (220, 345), (0, 0, 255), 1)
    
    # Irregular EPIC: VTR9874X2 (not 3 letters + 7 digits)
    cv2.putText(img, "EPIC: VTR9874X2", (250, 170), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    cv2.putText(img, "Elector's Name: MOHAN LAL", (250, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Father's Name: RADHE SHYAM", (250, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Gender: MALE", (250, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "DOB / Age: 35", (250, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    out_path = SAMPLES_DIR / "sample_voter_tampered.png"
    cv2.imwrite(str(out_path), img)
    return out_path

# ==========================================
# 5. PASSPORT (Authentic & Corrupt MRZ)
# ==========================================

def generate_clean_passport():
    """Authentic Indian Passport with valid ICAO Doc 9303 MRZ and clear portrait."""
    w, h = 950, 650
    img = np.ones((h, w, 3), dtype=np.uint8)
    img[:, :] = (242, 244, 246)
    
    cv2.rectangle(img, (10, 10), (w - 10, h - 10), (160, 170, 185), 2)
    cv2.putText(img, "PASSPORT - REPUBLIC OF INDIA", (220, 55), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (10, 10, 80), 3)
    cv2.putText(img, "Type: P   Code: IND   Passport No: A2094851", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    draw_realistic_photo_box(img, 50, 130, 175, 230)
    
    cv2.putText(img, "Surname: SHARMA", (260, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Given Name: VIKRAM", (260, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Nationality: INDIAN", (260, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "Sex: M", (260, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "DOB: 15/08/1992", (380, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "Place of Birth: NEW DELHI", (260, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "Date of Expiry: 14/08/2032", (260, 385), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Mathematically Valid 2-Line ICAO Doc 9303 MRZ
    # Passport: A2094851, Checksum digit = 7
    cv2.rectangle(img, (20, 480), (w - 20, 620), (255, 255, 255), -1)
    cv2.rectangle(img, (20, 480), (w - 20, 620), (190, 195, 205), 1)
    
    line1 = "P<INDSHARMA<<VIKRAM<<<<<<<<<<<<<<<<<<<<<<<<<"
    line2 = "A2094851<7IND9208153M3208140<<<<<<<<<<<<<<0"
    cv2.putText(img, line1, (35, 535), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)
    cv2.putText(img, line2, (35, 585), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 1)
    
    out_path = SAMPLES_DIR / "sample_passport_clean.png"
    cv2.imwrite(str(out_path), img)
    return out_path

def generate_passport_mismatch():
    """Fraudulent Passport with missing photo and corrupt MRZ checksum."""
    w, h = 950, 650
    img = np.ones((h, w, 3), dtype=np.uint8) * 240
    
    cv2.putText(img, "PASSPORT - REPUBLIC OF INDIA", (220, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (10, 10, 80), 3)
    cv2.putText(img, "Type: P   Code: IND   Passport No: Z9999999", (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Missing photo box
    cv2.rectangle(img, (50, 150), (220, 370), (200, 200, 200), -1)
    cv2.putText(img, "[Photo Missing]", (65, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (120, 120, 120), 2)
    
    cv2.putText(img, "Surname: VERMA", (260, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Given Name: SUNIL", (260, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 0), 2)
    cv2.putText(img, "Nationality: INDIAN", (260, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(img, "DOB: 12/04/1990", (260, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Corrupt MRZ (check digit 9 is invalid for Z9999999)
    cv2.rectangle(img, (20, 500), (w - 20, 620), (230, 230, 230), -1)
    cv2.putText(img, "P<INDVERMA<<SUNIL<<<<<<<<<<<<<<<<<<<<<<<<<<<", (40, 545), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (0, 0, 0), 2)
    cv2.putText(img, "Z9999999<9IND9004128M3004124<<<<<<<<<<<<<<0", (40, 595), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (0, 0, 0), 2)
    
    out_path = SAMPLES_DIR / "sample_passport_mismatch.png"
    cv2.imwrite(str(out_path), img)
    return out_path

# ==========================================
# MASTER GENERATOR & DEMO ORGANIZER
# ==========================================

def generate_all_samples():
    """Generates all 10 sample documents (2 for each of the 5 categories)."""
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating 10 demonstration sample documents across 5 categories...")
    
    # 1. Aadhaar
    f1 = generate_clean_aadhaar()
    f2 = generate_tampered_aadhaar()
    
    # 2. PAN
    f3 = generate_clean_pan()
    f4 = generate_tampered_pan()
    
    # 3. Driving Licence
    f5 = generate_clean_dl()
    f6 = generate_blurry_dl()
    
    # 4. Voter ID
    f7 = generate_clean_voter()
    f8 = generate_tampered_voter()
    
    # 5. Passport
    f9 = generate_clean_passport()
    f10 = generate_passport_mismatch()
    
    # Organize in dedicated demo_samples directory
    demo_mapping = [
        ("1_Aadhaar_Card", "1_Aadhaar_Authentic.png", f1),
        ("1_Aadhaar_Card", "2_Aadhaar_Tampered.png", f2),
        ("2_PAN_Card", "1_PAN_Authentic.png", f3),
        ("2_PAN_Card", "2_PAN_Tampered.png", f4),
        ("3_Driving_Licence", "1_Driving_Licence_Authentic.png", f5),
        ("3_Driving_Licence", "2_Driving_Licence_Blurry.png", f6),
        ("4_Voter_ID_Card", "1_Voter_ID_Authentic.png", f7),
        ("4_Voter_ID_Card", "2_Voter_ID_Tampered.png", f8),
        ("5_Passport", "1_Passport_Authentic.png", f9),
        ("5_Passport", "2_Passport_Corrupt_MRZ.png", f10),
    ]
    
    import shutil
    for folder, name, src in demo_mapping:
        dest_dir = DEMO_DIR / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest_dir / name)
        
    print(f"All 10 sample documents generated in:\n  - {SAMPLES_DIR}\n  - {DEMO_DIR}")

if __name__ == "__main__":
    generate_all_samples()
