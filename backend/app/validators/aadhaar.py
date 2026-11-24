import re
from typing import Dict, Any, List, Optional
from .verhoeff import validate_verhoeff

AADHAAR_KEYWORDS = [
    "GOVERNMENT OF INDIA", "UNIQUE IDENTIFICATION", "AADHAAR",
    "MERA AADHAAR", "UIDAI", "ENROLMENT NO", "YEAR OF BIRTH", "DOB"
]

def mask_aadhaar(number_str: str) -> str:
    clean = re.sub(r"\D", "", number_str)
    if len(clean) == 12:
        return f"XXXX-XXXX-{clean[-4:]}"
    elif len(clean) >= 4:
        return f"XXXX-XXXX-{clean[-4:]}"
    return "XXXX-XXXX-XXXX"

def validate_aadhaar_document(
    raw_text: str,
    lines: List[str],
    qr_detected: bool,
    qr_contents: List[str]
) -> Dict[str, Any]:
    text_upper = raw_text.upper()
    issues: List[Dict[str, Any]] = []
    
    # 1. Look for 12-digit numbers (spaced or continuous)
    # Aadhaar numbers cannot begin with 0 or 1 according to UIDAI rules
    found_numbers = re.findall(r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b", raw_text)
    
    extracted_number = None
    verhoeff_valid = False
    
    if found_numbers:
        # Prioritize one that passes Verhoeff
        for num in found_numbers:
            clean_digits = re.sub(r"\D", "", num)
            if len(clean_digits) == 12:
                extracted_number = clean_digits
                if validate_verhoeff(clean_digits):
                    verhoeff_valid = True
                    break
        if not extracted_number:
            extracted_number = re.sub(r"\D", "", found_numbers[0])
    else:
        # Try finding any 12 digit sequence
        generic_12 = re.findall(r"\b\d{12}\b", raw_text)
        if generic_12:
            extracted_number = generic_12[0]
            verhoeff_valid = validate_verhoeff(extracted_number)
            
    # Check if QR code contains Aadhaar data
    if qr_detected and qr_contents:
        for q in qr_contents:
            if "<PrintLetterBarcodeData" in q or "uid=" in q.lower():
                uid_match = re.search(r'uid=["\']?(\d{12})', q)
                if uid_match:
                    qr_uid = uid_match.group(1)
                    if not extracted_number:
                        extracted_number = qr_uid
                        verhoeff_valid = validate_verhoeff(qr_uid)

    # Issue evaluation
    if not extracted_number:
        issues.append({
            "id": "format_aadhaar_missing_number",
            "severity": "high",
            "category": "Format",
            "title": "Aadhaar Number Not Detected",
            "description": "Could not identify a standard 12-digit Aadhaar number on the document face."
        })
    else:
        if not verhoeff_valid:
            issues.append({
                "id": "format_aadhaar_verhoeff_fail",
                "severity": "high",
                "category": "Format",
                "title": "Invalid Aadhaar Checksum (Verhoeff Check Failed)",
                "description": f"The 12-digit sequence does not satisfy UIDAI's official Verhoeff mathematical checksum algorithm. High indication of a generated or forged number."
            })
            
    # 2. Check UIDAI official keywords
    matched_keywords = [kw for kw in AADHAAR_KEYWORDS if kw in text_upper]
    if len(matched_keywords) < 2:
        issues.append({
            "id": "format_aadhaar_missing_keywords",
            "severity": "high",
            "category": "Format",
            "title": "Missing Official UIDAI Header Text",
            "description": "Standard phrases like 'Government of India', 'Unique Identification Authority', or 'Mera Aadhaar' were not detected."
        })

    # 3. QR Code check
    if not qr_detected:
        issues.append({
            "id": "format_aadhaar_no_qr",
            "severity": "medium",
            "category": "Integrity",
            "title": "No Security QR Code Detected",
            "description": "Genuine Aadhaar cards include a machine-scannable QR code containing demographic data and digital signatures."
        })

    # 4. Extract Name, DOB, Gender
    dob = None
    dob_match = re.search(r"(?:DOB|DATE OF BIRTH|YEAR OF BIRTH)[:\s]*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4}|\b[12][90]\d{2}\b)", text_upper)
    if dob_match:
        dob = dob_match.group(1)
    else:
        generic_date = re.search(r"\b([0-3]\d[/-][01]\d[/-][12]\d{3})\b", raw_text)
        if generic_date:
            dob = generic_date.group(1)

    gender = None
    if "MALE" in text_upper and "FEMALE" not in text_upper:
        gender = "MALE"
    elif "FEMALE" in text_upper:
        gender = "FEMALE"
    elif "TRANSGENDER" in text_upper:
        gender = "TRANSGENDER"

    # Name extraction heuristic: line preceding DOB or near Government of India
    full_name = None
    for i, line in enumerate(lines):
        u = line.upper()
        if "DOB" in u or "YEAR OF BIRTH" in u:
            if i > 0 and len(lines[i-1].split()) in [2, 3, 4] and not any(kw in lines[i-1].upper() for kw in AADHAAR_KEYWORDS):
                full_name = lines[i-1].strip()
                break

    masked_no = mask_aadhaar(extracted_number) if extracted_number else None

    return {
        "document_type": "Aadhaar Card",
        "document_number_masked": masked_no,
        "document_number_raw": extracted_number,
        "format_valid": verhoeff_valid and (len(matched_keywords) >= 2),
        "format_notes": "12-digit UIDAI sequence" + (" (Verhoeff checksum passed)" if verhoeff_valid else " (Checksum failed or unverified)"),
        "full_name": full_name,
        "dob": dob,
        "gender": gender,
        "qr_detected": qr_detected,
        "mrz_detected": False,
        "detected_keywords": matched_keywords,
        "issues": issues
    }
