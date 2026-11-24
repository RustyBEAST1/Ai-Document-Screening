# AI Fake Identity & Document Screening System

A clean, beginner-friendly, mobile-first preliminary identity document screening application. Designed to help authorized verifiers quickly screen uploaded documents for signs of tampering, forgery, low-quality manipulation, mismatched details, and suspicious formatting.

> **Disclaimer:** This tool provides an AI-based preliminary screening only. It does not replace official government verification, KYC checks, or human review.

---

## 🎯 Supported Document Types (v1.0)

Strictly limited to the 5 authorized Indian identity document types:
1. **Aadhaar Card** (12-digit UIDAI sequence + Verhoeff checksum validation + QR detection)
2. **PAN Card** (10-character alphanumeric format `[A-Z]{5}[0-9]{4}[A-Z]` + Entity status code)
3. **Driving Licence** (State RTO standard format validation)
4. **Voter ID Card (EPIC)** (3-letter uppercase prefix + 7 digits standard)
5. **Passport** (1 letter + 7 digits + ICAO Doc 9303 MRZ checksum validation)

---

## 🧠 What the AI Checks

| Category | Forensic Check | Technique / Logic |
| :--- | :--- | :--- |
| **Image Quality** | Focus Sharpness & Blur | Laplacian variance ($<50$ severe, $<100$ moderate blur) |
| | Flash Washout & Glare | Connected component analysis on specular reflections ($>252$ brightness) |
| | Shadows & Lighting | $4 \times 4$ quadrant variance analysis |
| | Resolution & Dimensions | Width/height DPI checks, aspect ratio vs standard ID-1 format |
| | Crop & Truncation | Canny border edge density analysis |
| **Digital Forensics** | Digital Splicing & Forgery | Error Level Analysis (ELA) at 90% JPEG re-compression |
| | Clone Stamping / Erasure | High-frequency sensor noise disparity across image patches |
| | Face Photo Integrity | Haar Cascade frontal face detection + bounding seam gradient check |
| | Document Reuse | SHA-256 cryptographic hash + 64-bit difference hash (dHash) |
| **OCR & Layout** | Text Extraction | Windows Native OCR engine + fallback preprocessed OCR |
| | Aadhaar Verhoeff Check | Dihedral group $D_5$ mathematical checksum calculation |
| | PAN Syntax & Entity Type | Validates 4th character (P, C, H, A, B, G, J, L, F, T) |
| | Passport MRZ Checksum | ICAO Doc 9303 weighted (7-3-1) checksum algorithm |
| | Official Keywords | Header text checks (e.g., "Income Tax Department", "UIDAI", "Republic of India") |
| **Cross-Checks** | Optional Verifier Inputs | Fuzzy name matching (Levenshtein), normalized DOB & ID equality checks |

---

## 🔒 Privacy & Safety Compliance

- **Masked Previews**: Sensitive Aadhaar numbers (`XXXX-XXXX-1234`), PAN numbers (`ABCDE****F`), and addresses are masked by default. Verifiers can toggle visibility if needed.
- **Immediate Data Purge**: Verifiers can click **"Delete Document & Purge Scan"** to permanently delete the uploaded scan from disk and mark the database record as purged.
- **No False Claims**: The application does not claim official government verification.

---

## 🚀 Quick Setup Instructions

### 1. Requirements
- Python 3.10+
- (Optional for React dev) Node.js 18+

### 2. Run the Application
Open a terminal in the project directory and run:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the application
python run.py
```

The system will:
- Initialize the local SQLite database (`screening.db`)
- Verify and generate mock test sample documents in `backend/samples/`
- Start the server and automatically open **http://127.0.0.1:8000** in your default browser!

---

## 💻 Sample API Request and Response

### `POST /api/screen` (Multipart Form Data)

#### Sample Request (curl):
```bash
curl -X POST "http://127.0.0.1:8000/api/screen" \
  -F "file=@/path/to/aadhaar_card.png" \
  -F "document_type=Aadhaar Card" \
  -F "user_name=Arun Kumar Sharma" \
  -F "user_dob=15/08/1992" \
  -F "user_number=548291043723"
```

#### Sample Response (JSON):
```json
{
  "id": "e4b6c31a-98df-4ef3-92b0-8772a11b64a3",
  "document_type": "Aadhaar Card",
  "filename": "aadhaar_card.png",
  "risk_level": "Low",
  "risk_score": 18,
  "confidence": 94,
  "short_message": "No major tampering or format anomalies detected. Document appears consistent with standard templates.",
  "recommendation": "Proceed for further verification",
  "issues": [],
  "extracted_details": {
    "document_number_masked": "XXXX-XXXX-3723",
    "full_name": "ARUN KUMAR SHARMA",
    "dob": "15/08/1992",
    "gender": "MALE",
    "address_masked": "Protected / Masked",
    "format_valid": true,
    "format_notes": "12-digit UIDAI sequence (Verhoeff checksum passed)",
    "qr_detected": true,
    "mrz_detected": false,
    "detected_keywords": ["GOVERNMENT OF INDIA", "UNIQUE IDENTIFICATION", "AADHAAR"]
  },
  "cross_checks": {
    "checked": true,
    "name_match": true,
    "name_score": 95,
    "dob_match": true,
    "number_match": true,
    "notes": [
      "Holder name verified with 95% match confidence.",
      "Date of birth verified (15/08/1992).",
      "Document identification number matched."
    ]
  },
  "has_ela": true,
  "preview_url": "/api/files/e4b6c31a_aadhaar_card.png",
  "ela_url": "/api/files/e4b6c31a-98df-4ef3-92b0-8772a11b64a3_ela.jpg",
  "disclaimer": "This tool provides an AI-based preliminary screening only. It does not replace official government verification, KYC checks, or human review.",
  "created_at": "2026-11-22T14:15:30.124892"
}
```

---

## 🛡️ Minimal Admin Audit History

Verifiers can view past screening audits at any time:
- In the Web UI: Click the **"History"** button in the header.
- Via API: `GET /api/history?limit=30`
- Purge an entry: `DELETE /api/screening/{screening_id}`
