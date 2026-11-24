import re
from typing import Dict, Any, List, Optional

PAN_KEYWORDS = [
    "INCOME TAX DEPARTMENT", "GOVT. OF INDIA", "PERMANENT ACCOUNT NUMBER",
    "FATHER'S NAME", "SIGNATURE", "INCOME TAX"
]

PAN_ENTITY_TYPES = {
    "P": "Individual",
    "C": "Company",
    "H": "Hindu Undivided Family (HUF)",
    "A": "Association of Persons (AOP)",
    "B": "Body of Individuals (BOI)",
    "G": "Government Agency",
    "J": "Artificial Juridical Person",
    "L": "Local Authority",
    "F": "Firm / LLP",
    "T": "Trust"
}

def mask_pan(pan_str: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9]", "", pan_str).upper()
    if len(clean) == 10:
        return f"{clean[:5]}****{clean[-1]}"
    return "ABCDE****F"

def validate_pan_document(raw_text: str, lines: List[str]) -> Dict[str, Any]:
    text_upper = raw_text.upper()
    issues: List[Dict[str, Any]] = []
    
    # Standard PAN format regex: 5 letters, 4 digits, 1 letter
    pan_matches = re.findall(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text_upper)
    
    extracted_pan = None
    entity_desc = None
    is_valid_format = False
    
    if pan_matches:
        extracted_pan = pan_matches[0]
        fourth_char = extracted_pan[3]
        if fourth_char in PAN_ENTITY_TYPES:
            entity_desc = PAN_ENTITY_TYPES[fourth_char]
            is_valid_format = True
        else:
            issues.append({
                "id": "format_pan_invalid_4th_char",
                "severity": "high",
                "category": "Format",
                "title": "Invalid PAN Entity Code",
                "description": f"The 4th character '{fourth_char}' is not a valid Income Tax entity type (expected P, C, H, A, B, G, J, L, F, or T)."
            })
    else:
        # Check for near matches (e.g., OCR misreading '0' as 'O' or '1' as 'I')
        loose_matches = re.findall(r"\b[A-Z0-9]{10}\b", text_upper)
        if loose_matches:
            cand = loose_matches[0]
            issues.append({
                "id": "format_pan_deformed_syntax",
                "severity": "high",
                "category": "Format",
                "title": "Malformed PAN Syntax",
                "description": f"Found candidate '{cand}' but it does not conform to the 5 letters + 4 digits + 1 letter PAN standard."
            })
        else:
            issues.append({
                "id": "format_pan_missing_number",
                "severity": "high",
                "category": "Format",
                "title": "PAN Number Not Found",
                "description": "Could not identify a 10-character alphanumeric Permanent Account Number."
            })

    # Check official Income Tax keywords
    matched_kws = [kw for kw in PAN_KEYWORDS if kw in text_upper]
    if len(matched_kws) < 2:
        issues.append({
            "id": "format_pan_missing_headers",
            "severity": "high",
            "category": "Format",
            "title": "Missing Official Income Tax Department Headers",
            "description": "Standard phrases like 'Income Tax Department' or 'Govt. of India' were absent from the document."
        })

    # Extract DOB
    dob = None
    dob_match = re.search(r"\b([0-3]\d[/-][01]\d[/-][12]\d{3})\b", raw_text)
    if dob_match:
        dob = dob_match.group(1)

    # Extract Name & Father's Name heuristic
    full_name = None
    for i, line in enumerate(lines):
        clean_l = line.strip()
        u = clean_l.upper()
        if "INCOME TAX" in u or "GOVT" in u or "PERMANENT" in u:
            continue
        # Names are usually 2 to 4 words of all letters
        words = clean_l.split()
        if 2 <= len(words) <= 4 and all(w.isalpha() for w in words):
            if not full_name:
                full_name = clean_l
                break

    masked_pan = mask_pan(extracted_pan) if extracted_pan else None

    return {
        "document_type": "PAN Card",
        "document_number_masked": masked_pan,
        "document_number_raw": extracted_pan,
        "format_valid": is_valid_format and (len(matched_kws) >= 2),
        "format_notes": f"PAN ({entity_desc or 'Unknown'})" if extracted_pan else "Invalid PAN format",
        "full_name": full_name,
        "dob": dob,
        "gender": None,
        "qr_detected": False,
        "mrz_detected": False,
        "detected_keywords": matched_kws,
        "issues": issues
    }
