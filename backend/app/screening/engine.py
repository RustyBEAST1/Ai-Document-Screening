import cv2
import numpy as np
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..config import (
    UPLOAD_DIR,
    RISK_THRESHOLD_LOW,
    RISK_THRESHOLD_MEDIUM,
    DISCLAIMER_TEXT
)
from ..forensics.quality import analyze_image_quality
from ..forensics.tampering import analyze_tampering_and_forgery
from ..forensics.face_analyzer import analyze_photo_and_face
from ..forensics.hasher import compute_sha256, compute_dhash, check_duplicate_image
from ..ocr.engine import extract_document_ocr
from ..validators.aadhaar import validate_aadhaar_document
from ..validators.pan import validate_pan_document
from ..validators.driving_licence import validate_driving_licence_document
from ..validators.voter_id import validate_voter_id_document
from ..validators.passport import validate_passport_document
from ..validators.cross_checker import perform_cross_checks
from ..database import find_duplicate_hashes, save_screening

def calculate_risk_and_recommendation(
    issues: List[Dict[str, Any]],
    format_valid: bool,
    has_critical_fail: bool
) -> tuple[int, str, int, str, str]:
    """
    Computes:
    - risk_score (0-100)
    - risk_level ("Low", "Medium", "High")
    - confidence (0-100)
    - short_message
    - recommendation
    """
    score = 5  # Baseline noise
    
    high_count = 0
    medium_count = 0
    low_count = 0
    
    for iss in issues:
        sev = iss.get("severity", "info").lower()
        cat = iss.get("category", "")
        
        if sev == "high":
            high_count += 1
            if cat in ("Forensics", "Format", "Cross-Check"):
                score += 32
            else:
                score += 24
        elif sev == "medium":
            medium_count += 1
            score += 15
        elif sev == "low":
            low_count += 6

    if has_critical_fail:
        score = max(score, 75)

    # Clamp 0-100
    risk_score = min(max(score, 0), 100)
    
    # Classify Risk Level
    if risk_score <= RISK_THRESHOLD_LOW:
        risk_level = "Low"
        recommendation = "Proceed for further verification"
        short_message = "No major tampering or format anomalies detected. Document appears consistent with standard templates."
    elif risk_score <= RISK_THRESHOLD_MEDIUM:
        risk_level = "Medium"
        recommendation = "Verify manually"
        if high_count > 0:
            short_message = f"Moderate risk: {issues[0]['title']} detected. Manual visual check recommended."
        else:
            short_message = "Quality artifacts or minor layout deviations detected. Secondary review advised."
    else:
        risk_level = "High"
        recommendation = "Verify manually"
        primary_issue = issues[0]["title"] if issues else "Severe tampering detected"
        short_message = f"High risk: {primary_issue}. Possible forgery or tampered document. Do not approve automatically."

    # Confidence calculation: quality penalty
    confidence = 94
    if any(i["id"] in ("qual_severe_blur", "qual_severe_glare", "qual_low_resolution") for i in issues):
        confidence -= 18
    elif any(i.get("severity") == "high" for i in issues):
        confidence = 91
        
    confidence = min(max(confidence, 65), 98)
    
    return risk_score, risk_level, confidence, short_message, recommendation

def run_document_screening(
    image_path: Path,
    original_filename: str,
    document_type: str,
    user_name: Optional[str] = None,
    user_dob: Optional[str] = None,
    user_number: Optional[str] = None,
    is_pdf: bool = False
) -> Dict[str, Any]:
    """
    Main orchestration function: loads document, runs forensic analysis,
    OCR, format validation, cross-checks, scores risk, saves to DB.
    """
    screening_id = str(uuid.uuid4())
    all_issues: List[Dict[str, Any]] = []
    
    # 1. Read image with OpenCV
    img_bgr = cv2.imread(str(image_path))
    if img_bgr is None:
        raise ValueError("Could not read image file. Unsupported format or corrupted file.")
        
    # 2. Hashes & Duplicate Check
    file_hash = compute_sha256(image_path)
    perceptual_hash = compute_dhash(img_bgr)
    
    recent_records = find_duplicate_hashes(file_hash, perceptual_hash)
    is_dup, dup_type, matched_rec = check_duplicate_image(
        file_hash, perceptual_hash, recent_records, current_screening_id=screening_id
    )
    if is_dup:
        match_id = matched_rec.get("id", "earlier scan")[:8]
        all_issues.append({
            "id": "forensic_duplicate_reuse",
            "severity": "high",
            "category": "Integrity",
            "title": f"Duplicate / Reused Document Detected ({dup_type})",
            "description": f"This exact or visually identical document was previously screened (Record #{match_id}). Potential reuse or syndicate recycling."
        })

    # 3. Image Quality Forensics
    qual_res = analyze_image_quality(img_bgr)
    all_issues.extend(qual_res["issues"])

    # 4. Digital Tampering & Forgery (ELA)
    ela_filename = f"{screening_id}_ela.jpg"
    ela_path = UPLOAD_DIR / ela_filename
    tamp_res = analyze_tampering_and_forgery(img_bgr, image_path, ela_path)
    all_issues.extend(tamp_res["issues"])
    has_ela = ela_path.exists()

    # 5. Face / Portrait Photo Analysis
    face_res = analyze_photo_and_face(img_bgr, document_type)
    all_issues.extend(face_res["issues"])

    # 6. OCR Extraction
    ocr_res = extract_document_ocr(img_bgr, image_path, is_pdf=is_pdf)
    raw_text = ocr_res["raw_text"]
    lines = ocr_res["lines"]
    qr_detected = ocr_res["qr_detected"]
    qr_contents = ocr_res["qr_contents"]

    # 7. Document Specific Validator
    extracted_data = {}
    if document_type == "Aadhaar Card":
        val_res = validate_aadhaar_document(raw_text, lines, qr_detected, qr_contents)
    elif document_type == "PAN Card":
        val_res = validate_pan_document(raw_text, lines)
    elif document_type == "Driving Licence":
        val_res = validate_driving_licence_document(raw_text, lines)
    elif document_type == "Voter ID Card":
        val_res = validate_voter_id_document(raw_text, lines)
    elif document_type == "Passport":
        val_res = validate_passport_document(raw_text, lines)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")

    all_issues.extend(val_res.get("issues", []))
    extracted_data = val_res

    # 8. Cross-Checks (if user entered optional verification details)
    cross_res = perform_cross_checks(
        user_name=user_name,
        user_dob=user_dob,
        user_number=user_number,
        extracted_name=extracted_data.get("full_name"),
        extracted_dob=extracted_data.get("dob"),
        extracted_number=extracted_data.get("document_number_raw"),
        ocr_raw_text=raw_text
    )
    all_issues.extend(cross_res.get("issues", []))

    # 9. Scoring and Recommendation
    format_valid = extracted_data.get("format_valid", False)
    has_critical_fail = any(
        i["id"] in (
            "format_aadhaar_verhoeff_fail",
            "format_ppt_mrz_checksum_error",
            "forensic_ela_mismatch",
            "forensic_photo_border_seam",
            "cross_name_severe_mismatch",
            "cross_doc_number_mismatch"
        )
        for i in all_issues
    )
    
    risk_score, risk_level, confidence, short_msg, rec = calculate_risk_and_recommendation(
        all_issues, format_valid, has_critical_fail
    )

    created_iso = datetime.now().isoformat()
    
    # Store record
    record = {
        "id": screening_id,
        "document_type": document_type,
        "filename": original_filename,
        "stored_filename": image_path.name,
        "file_hash": file_hash,
        "perceptual_hash": perceptual_hash,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "confidence": confidence,
        "short_message": short_msg,
        "recommendation": rec,
        "issues": all_issues,
        "extracted_details": {
            "document_number_masked": extracted_data.get("document_number_masked"),
            "full_name": extracted_data.get("full_name"),
            "dob": extracted_data.get("dob"),
            "gender": extracted_data.get("gender"),
            "address_masked": "Protected / Masked",
            "format_valid": format_valid,
            "format_notes": extracted_data.get("format_notes", ""),
            "qr_detected": qr_detected,
            "mrz_detected": extracted_data.get("mrz_detected", False),
            "detected_keywords": extracted_data.get("detected_keywords", [])
        },
        "cross_checks": cross_res,
        "has_ela": has_ela,
        "created_at": created_iso
    }
    
    save_screening(record)

    return {
        "id": screening_id,
        "document_type": document_type,
        "filename": original_filename,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "confidence": confidence,
        "short_message": short_msg,
        "recommendation": rec,
        "issues": all_issues,
        "extracted_details": record["extracted_details"],
        "cross_checks": cross_res,
        "has_ela": has_ela,
        "preview_url": f"/api/files/{image_path.name}",
        "ela_url": f"/api/files/{ela_filename}" if has_ela else None,
        "disclaimer": DISCLAIMER_TEXT,
        "created_at": created_iso
    }
