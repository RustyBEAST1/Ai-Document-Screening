import re
from typing import Dict, Any, List, Optional

VOTER_KEYWORDS = [
    "ELECTION COMMISSION OF INDIA", "ELECTOR PHOTO IDENTITY CARD", "EPIC",
    "BHARAT NIRVACHAN", "ELECTOR", "FATHER'S NAME", "IDENTITY CARD"
]

def mask_voter_id(voter_str: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9]", "", voter_str).upper()
    if len(clean) >= 8:
        return f"{clean[:3]}****{clean[-3:]}"
    elif len(clean) >= 4:
        return f"{clean[:2]}****{clean[-2:]}"
    return "EPIC****XXXX"

def validate_voter_id_document(raw_text: str, lines: List[str]) -> Dict[str, Any]:
    text_upper = raw_text.upper()
    issues: List[Dict[str, Any]] = []
    
    # Standard EPIC format regex: 3 uppercase letters followed by 7 digits
    epic_matches = re.findall(r"\b([A-Z]{3})([0-9]{7})\b", text_upper)
    
    extracted_epic = None
    is_valid_format = False
    
    if epic_matches:
        pref, num = epic_matches[0]
        extracted_epic = f"{pref}{num}"
        is_valid_format = True
    else:
        # Check slash-formatted state voter IDs (e.g. DL/01/002/123456)
        slash_matches = re.findall(r"\b[A-Z]{2,3}\/[0-9]{1,3}\/[0-9]{1,3}\/[0-9]{4,7}\b", text_upper)
        if slash_matches:
            extracted_epic = slash_matches[0]
            is_valid_format = True
        else:
            # Check any 10-char candidate
            loose = re.findall(r"\b[A-Z0-9]{10}\b", text_upper)
            if loose:
                cand = loose[0]
                issues.append({
                    "id": "format_voter_irregular_code",
                    "severity": "medium",
                    "category": "Format",
                    "title": "Irregular Voter ID (EPIC) Format",
                    "description": f"Found candidate '{cand}' but standard EPIC format requires 3 uppercase letters followed by 7 digits."
                })
            else:
                issues.append({
                    "id": "format_voter_missing_number",
                    "severity": "high",
                    "category": "Format",
                    "title": "Voter ID (EPIC) Number Not Found",
                    "description": "Could not identify an Election Commission EPIC alphanumeric identity number."
                })

    # Check official Election Commission keywords
    matched_kws = [kw for kw in VOTER_KEYWORDS if kw in text_upper]
    if len(matched_kws) < 2:
        issues.append({
            "id": "format_voter_missing_headers",
            "severity": "high",
            "category": "Format",
            "title": "Missing Election Commission Header",
            "description": "Official phrases like 'Election Commission of India' or 'Elector Photo Identity Card' were absent."
        })

    # Extract Age or DOB
    dob = None
    age_match = re.search(r"\b(?:AGE|DOB)[:\s]*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4}|\d{2})\b", text_upper)
    if age_match:
        dob = age_match.group(1)

    # Extract Gender
    gender = None
    if "MALE" in text_upper and "FEMALE" not in text_upper:
        gender = "MALE"
    elif "FEMALE" in text_upper:
        gender = "FEMALE"

    # Name extraction heuristic
    full_name = None
    for line in lines:
        u = line.strip().upper()
        if ("ELECTOR'S NAME" in u or "NAME" in u) and ":" in u:
            parts = line.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                full_name = parts[1].strip()
                break

    masked_no = mask_voter_id(extracted_epic) if extracted_epic else None

    return {
        "document_type": "Voter ID Card",
        "document_number_masked": masked_no,
        "document_number_raw": extracted_epic,
        "format_valid": is_valid_format and (len(matched_kws) >= 2),
        "format_notes": "Standard ECI EPIC Format (3 letters + 7 digits)" if is_valid_format else "Format unverified",
        "full_name": full_name,
        "dob": dob,
        "gender": gender,
        "qr_detected": False,
        "mrz_detected": False,
        "detected_keywords": matched_kws,
        "issues": issues
    }
