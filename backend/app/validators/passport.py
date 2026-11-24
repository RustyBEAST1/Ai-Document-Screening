import re
from typing import Dict, Any, List, Optional

PASSPORT_KEYWORDS = [
    "PASSPORT", "REPUBLIC OF INDIA", "BHARAT GANRAJYA", "TYPE P",
    "CODE IND", "NATIONALITY INDIAN", "GIVEN NAME", "SURNAME"
]

def mask_passport(ppt_str: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9]", "", ppt_str).upper()
    if len(clean) == 8:
        return f"{clean[:3]}****{clean[-1]}"
    elif len(clean) > 4:
        return f"{clean[:2]}****{clean[-2:]}"
    return "P****XXXX"

def compute_mrz_checksum(data: str) -> int:
    """Calculates ICAO Doc 9303 MRZ checksum with weights 7, 3, 1."""
    weights = [7, 3, 1]
    total = 0
    for i, ch in enumerate(data):
        w = weights[i % 3]
        if ch.isdigit():
            val = int(ch)
        elif ch.isalpha():
            val = ord(ch.upper()) - 55  # A=10, B=11 ... Z=35
        elif ch == "<":
            val = 0
        else:
            val = 0
        total += val * w
    return total % 10

def parse_mrz(lines: List[str]) -> Dict[str, Any]:
    """Detects and parses 2-line ICAO Doc 9303 MRZ strings if visible."""
    mrz_lines = []
    for line in lines:
        clean = re.sub(r"\s+", "", line).upper()
        # Look for ICAO MRZ lines with '<' fillers
        if ("<" in clean) and len(clean) >= 20 and (clean.startswith("P<") or re.search(r"[A-Z0-9<]{20,}", clean)):
            mrz_lines.append(clean)
            
    if len(mrz_lines) >= 2:
        line1 = mrz_lines[0]
        line2 = mrz_lines[1]
        
        # Check passport number from line 2
        ppt_candidate = line2[:9].replace("<", "")
        chk_digit = line2[9] if len(line2) > 9 and line2[9].isdigit() else None
        
        checksum_valid = False
        if chk_digit and len(line2) >= 10:
            calc_chk = compute_mrz_checksum(line2[:9])
            checksum_valid = (str(calc_chk) == str(chk_digit))
            
        return {
            "mrz_detected": True,
            "line1": line1,
            "line2": line2,
            "passport_candidate": ppt_candidate,
            "checksum_valid": checksum_valid
        }
    return {"mrz_detected": False}

def validate_passport_document(raw_text: str, lines: List[str]) -> Dict[str, Any]:
    text_upper = raw_text.upper()
    issues: List[Dict[str, Any]] = []
    
    # Check for MRZ
    mrz_data = parse_mrz(lines)
    mrz_detected = mrz_data.get("mrz_detected", False)
    
    # Indian passport number regex: 1 letter + 7 digits
    ppt_matches = re.findall(r"\b([A-PR-WYa-pr-wy][0-9]{7})\b", text_upper)
    
    extracted_ppt = None
    is_valid_format = False
    
    if ppt_matches:
        extracted_ppt = ppt_matches[0]
        is_valid_format = True
    elif mrz_detected and mrz_data.get("passport_candidate"):
        cand = mrz_data["passport_candidate"]
        if re.match(r"^[A-Z][0-9]{7}$", cand):
            extracted_ppt = cand
            is_valid_format = True
            
    if not extracted_ppt:
        issues.append({
            "id": "format_ppt_missing_number",
            "severity": "high",
            "category": "Format",
            "title": "Passport Number Not Identified",
            "description": "Standard 8-character Indian passport number (1 letter + 7 digits) was not found."
        })
        
    # Check MRZ integrity if present
    if mrz_detected:
        if not mrz_data.get("checksum_valid", True):
            issues.append({
                "id": "format_ppt_mrz_checksum_error",
                "severity": "high",
                "category": "Integrity",
                "title": "MRZ Checksum Failure",
                "description": "The Machine Readable Zone (MRZ) failed the ICAO Doc 9303 weighted checksum calculation. High probability of forgery or digital tampering."
            })
    else:
        issues.append({
            "id": "format_ppt_no_mrz",
            "severity": "low",
            "category": "Integrity",
            "title": "MRZ Not Visible or Low Contrast",
            "description": "Machine Readable Zone was not clearly identified at the bottom of the booklet page."
        })

    # Check official Passport keywords
    matched_kws = [kw for kw in PASSPORT_KEYWORDS if kw in text_upper]
    if len(matched_kws) < 2:
        issues.append({
            "id": "format_ppt_missing_headers",
            "severity": "high",
            "category": "Format",
            "title": "Missing Republic of India Passport Headers",
            "description": "Standard phrases like 'Republic of India', 'Passport', or 'Nationality: Indian' were missing."
        })

    # Extract DOB
    dob = None
    dob_match = re.search(r"\b([0-3]\d[/-][01]\d[/-][12]\d{3})\b", raw_text)
    if dob_match:
        dob = dob_match.group(1)

    # Name extraction
    full_name = None
    for line in lines:
        u = line.strip().upper()
        if "GIVEN NAME" in u or "SURNAME" in u:
            parts = line.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                full_name = parts[1].strip()
                break

    masked_no = mask_passport(extracted_ppt) if extracted_ppt else None

    return {
        "document_type": "Passport",
        "document_number_masked": masked_no,
        "document_number_raw": extracted_ppt,
        "format_valid": is_valid_format and (len(matched_kws) >= 2),
        "format_notes": "Standard Indian Passport (Type P / IND)" if is_valid_format else "Format unverified",
        "full_name": full_name,
        "dob": dob,
        "gender": None,
        "qr_detected": False,
        "mrz_detected": mrz_detected,
        "detected_keywords": matched_kws,
        "issues": issues
    }
