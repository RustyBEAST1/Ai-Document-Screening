import re
from typing import Dict, Any, List, Optional

DL_KEYWORDS = [
    "DRIVING LICENCE", "DRIVING LICENSE", "UNION OF INDIA", "TRANSPORT",
    "MOTOR VEHICLES", "VALIDITY", "AUTHORISED TO DRIVE", "NON-TRANSPORT", "DOB"
]

INDIAN_STATE_CODES = {
    "AN", "AP", "AR", "AS", "BR", "CH", "CG", "DD", "DL", "DN", "GA", "GJ",
    "HR", "HP", "JH", "JK", "KA", "KL", "LA", "LD", "MP", "MH", "MN", "ML",
    "MZ", "NL", "OD", "OR", "PB", "PY", "RJ", "SK", "TN", "TR", "TS", "UK",
    "UA", "UP", "WB"
}

def mask_dl(dl_str: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9]", "", dl_str).upper()
    if len(clean) >= 10:
        return f"{clean[:4]}-****-{clean[-4:]}"
    elif len(clean) >= 4:
        return f"{clean[:2]}****{clean[-2:]}"
    return "DL****XXXX"

def validate_driving_licence_document(raw_text: str, lines: List[str]) -> Dict[str, Any]:
    text_upper = raw_text.upper()
    issues: List[Dict[str, Any]] = []
    
    # Standard Indian Sarathi DL format regex:
    # 2 letters state + 2 digits RTO + 4 digits issue year + 7 digits serial
    dl_pattern = r"\b([A-Z]{2})[ -]?([0-9]{2})[ -]?([0-9]{4})[ -]?([0-9]{7})\b"
    matches = re.findall(dl_pattern, text_upper)
    
    extracted_dl = None
    state_code = None
    is_valid_format = False
    
    if matches:
        st, rto, yr, ser = matches[0]
        extracted_dl = f"{st}{rto}{yr}{ser}"
        state_code = st
        if st in INDIAN_STATE_CODES:
            is_valid_format = True
        else:
            issues.append({
                "id": "format_dl_unknown_state",
                "severity": "high",
                "category": "Format",
                "title": "Unrecognized State Code in Driving Licence",
                "description": f"The state prefix '{st}' does not correspond to any valid Indian State or Union Territory."
            })
    else:
        # Check alternative or legacy DL formats (e.g. MH-02-2015-1234567 or DL0419980001234)
        alt_matches = re.findall(r"\b([A-Z]{2})[0-9\/-]{8,16}\b", text_upper)
        if alt_matches:
            cand = alt_matches[0]
            st = cand[:2]
            if st in INDIAN_STATE_CODES:
                extracted_dl = cand
                state_code = st
                is_valid_format = True
            else:
                issues.append({
                    "id": "format_dl_invalid_prefix",
                    "severity": "medium",
                    "category": "Format",
                    "title": "Unverified Driving Licence Format",
                    "description": f"Extracted number '{cand}' has an irregular structure for Indian transport registries."
                })
        else:
            issues.append({
                "id": "format_dl_missing_number",
                "severity": "high",
                "category": "Format",
                "title": "Driving Licence Number Not Found",
                "description": "Could not identify a standard state/RTO formatted driving licence number."
            })

    # Check official transport department keywords
    matched_kws = [kw for kw in DL_KEYWORDS if kw in text_upper]
    if len(matched_kws) < 2:
        issues.append({
            "id": "format_dl_missing_headers",
            "severity": "medium",
            "category": "Format",
            "title": "Missing Official Transport Keywords",
            "description": "Expected phrases like 'Driving Licence', 'Transport Department', or 'Union of India' were missing."
        })

    # Extract DOB
    dob = None
    dob_match = re.search(r"\b([0-3]\d[/-][01]\d[/-][12]\d{3})\b", raw_text)
    if dob_match:
        dob = dob_match.group(1)

    # Name extraction heuristic
    full_name = None
    for line in lines:
        u = line.strip().upper()
        if "NAME" in u and ":" in u:
            parts = line.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                full_name = parts[1].strip()
                break

    masked_no = mask_dl(extracted_dl) if extracted_dl else None

    return {
        "document_type": "Driving Licence",
        "document_number_masked": masked_no,
        "document_number_raw": extracted_dl,
        "format_valid": is_valid_format and (len(matched_kws) >= 2),
        "format_notes": f"Driving Licence ({state_code} State Transport)" if state_code else "Format unverified",
        "full_name": full_name,
        "dob": dob,
        "gender": None,
        "qr_detected": False,
        "mrz_detected": False,
        "detected_keywords": matched_kws,
        "issues": issues
    }
