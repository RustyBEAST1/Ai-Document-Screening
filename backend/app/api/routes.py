import os
import shutil
import uuid
from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query, Response
from fastapi.responses import FileResponse

from ..config import (
    UPLOAD_DIR,
    SAMPLES_DIR,
    SUPPORTED_DOCUMENT_TYPES,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    DISCLAIMER_TEXT
)
from ..schemas import ScreeningResponse, ScreeningSummary, SampleDocument
from ..screening.engine import run_document_screening
from ..database import list_screenings, get_screening_by_id, mark_screening_deleted

router = APIRouter(prefix="/api")

SAMPLE_DEFINITIONS = [
    # 1. Aadhaar Card (2 samples)
    {
        "id": "sample-aadhaar-clean",
        "title": "Clean Aadhaar Card (Genuine)",
        "document_type": "Aadhaar Card",
        "description": "Standard UIDAI layout with valid Verhoeff 12-digit checksum and portrait.",
        "expected_risk": "Low",
        "filename": "sample_aadhaar_clean.png"
    },
    {
        "id": "sample-aadhaar-tampered",
        "title": "Tampered Aadhaar (Invalid Checksum)",
        "document_type": "Aadhaar Card",
        "description": "Spliced Aadhaar number with high compression noise failing Verhoeff checksum.",
        "expected_risk": "High",
        "filename": "sample_aadhaar_tampered.png"
    },
    # 2. PAN Card (2 samples)
    {
        "id": "sample-pan-clean",
        "title": "Clean PAN Card (Genuine)",
        "document_type": "PAN Card",
        "description": "Valid 10-char PAN format with 4th char 'P' (Individual) and official headers.",
        "expected_risk": "Low",
        "filename": "sample_pan_clean.png"
    },
    {
        "id": "sample-pan-tampered",
        "title": "Tampered PAN Card (Altered DOB)",
        "document_type": "PAN Card",
        "description": "Spliced date-of-birth patch with high ELA variance and invalid PAN entity code 'X'.",
        "expected_risk": "High",
        "filename": "sample_pan_tampered.png"
    },
    # 3. Driving Licence (2 samples)
    {
        "id": "sample-dl-clean",
        "title": "Clean Driving Licence (Genuine)",
        "document_type": "Driving Licence",
        "description": "Valid Sarathi RTO format (DL04 2021 0012345) with sharp portrait and chip graphic.",
        "expected_risk": "Low",
        "filename": "sample_dl_clean.png"
    },
    {
        "id": "sample-dl-blurry",
        "title": "Blurry Driving Licence (Quality Defect)",
        "document_type": "Driving Licence",
        "description": "Heavy blur and high glare washout preventing reliable verification.",
        "expected_risk": "Medium",
        "filename": "sample_dl_blurry.png"
    },
    # 4. Voter ID Card (2 samples)
    {
        "id": "sample-voter-clean",
        "title": "Clean Voter ID Card (Genuine)",
        "document_type": "Voter ID Card",
        "description": "Valid ECI EPIC format (WBF1948273: 3 letters + 7 digits) with official headers.",
        "expected_risk": "Low",
        "filename": "sample_voter_clean.png"
    },
    {
        "id": "sample-voter-tampered",
        "title": "Irregular Voter ID (Format Error)",
        "document_type": "Voter ID Card",
        "description": "Non-standard EPIC format (VTR9874X2) and mismatched photo border seam.",
        "expected_risk": "High",
        "filename": "sample_voter_tampered.png"
    },
    # 5. Passport (2 samples)
    {
        "id": "sample-passport-clean",
        "title": "Clean Passport Page (Genuine)",
        "document_type": "Passport",
        "description": "Valid Republic of India passport with 2-line ICAO Doc 9303 MRZ and correct checksums.",
        "expected_risk": "Low",
        "filename": "sample_passport_clean.png"
    },
    {
        "id": "sample-passport-mismatch",
        "title": "Passport with Corrupt MRZ (Fraud)",
        "document_type": "Passport",
        "description": "Passport page missing photo and failing ICAO Doc 9303 MRZ checksum.",
        "expected_risk": "High",
        "filename": "sample_passport_mismatch.png"
    }
]

@router.get("/samples", response_model=List[SampleDocument])
def get_sample_documents():
    """Lists available built-in mock sample documents for 1-click testing."""
    return SAMPLE_DEFINITIONS

@router.post("/screen-sample/{sample_id}", response_model=ScreeningResponse)
def screen_sample_document(
    sample_id: str,
    user_name: Optional[str] = None,
    user_dob: Optional[str] = None,
    user_number: Optional[str] = None
):
    """Executes screening immediately on a pre-loaded sample document."""
    matched = next((s for s in SAMPLE_DEFINITIONS if s["id"] == sample_id), None)
    if not matched:
        raise HTTPException(status_code=404, detail="Sample document not found.")
        
    src_path = SAMPLES_DIR / matched["filename"]
    if not src_path.exists():
        raise HTTPException(status_code=500, detail="Sample file missing from disk.")
        
    # Copy to uploads with unique name
    unique_name = f"sample_{uuid.uuid4().hex[:8]}_{matched['filename']}"
    target_path = UPLOAD_DIR / unique_name
    shutil.copyfile(src_path, target_path)
    
    try:
        result = run_document_screening(
            image_path=target_path,
            original_filename=matched["filename"],
            document_type=matched["document_type"],
            user_name=user_name,
            user_dob=user_dob,
            user_number=user_number,
            is_pdf=False
        )
        return result
    except Exception as e:
        if target_path.exists():
            target_path.unlink()
        raise HTTPException(status_code=500, detail=f"Screening error: {str(e)}")

@router.post("/screen", response_model=ScreeningResponse)
async def screen_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    user_name: Optional[str] = Form(None),
    user_dob: Optional[str] = Form(None),
    user_number: Optional[str] = Form(None)
):
    """
    Main screening endpoint:
    - Accepts uploaded photo/scan/PDF
    - Enforces document type constraint
    - Analyzes tampering, quality, layout, text & formats
    - Returns structured risk score and recommendations
    """
    # 1. Enforce supported document types strictly
    if document_type not in SUPPORTED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported document type '{document_type}'. Supported: {', '.join(SUPPORTED_DOCUMENT_TYPES)}"
        )

    # 2. Check file extension
    file_ext = Path(file.filename or "").suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Supported extensions: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 3. Read content and verify size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB."
        )

    # 4. Save file to secure upload directory
    stored_name = f"{uuid.uuid4().hex}_{Path(file.filename).name}"
    target_path = UPLOAD_DIR / stored_name
    
    with open(target_path, "wb") as f:
        f.write(contents)

    is_pdf = file_ext == ".pdf"
    image_to_analyze = target_path

    # Auto-orient smartphone photos with EXIF tags to prevent sideways orientation
    if not is_pdf:
        try:
            from PIL import Image, ImageOps
            with Image.open(target_path) as pil_img:
                transposed = ImageOps.exif_transpose(pil_img)
                transposed.save(target_path)
        except Exception:
            pass

    # If PDF, extract first page image or render
    if is_pdf:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(target_path))
            first_page = reader.pages[0]
            if first_page.images:
                # Save extracted image
                extracted_img = first_page.images[0]
                converted_img_path = UPLOAD_DIR / f"{uuid.uuid4().hex}_page1.png"
                with open(converted_img_path, "wb") as img_f:
                    img_f.write(extracted_img.data)
                image_to_analyze = converted_img_path
        except Exception:
            pass

    # 5. Run full screening pipeline
    try:
        result = run_document_screening(
            image_path=image_to_analyze,
            original_filename=file.filename or "uploaded_document",
            document_type=document_type,
            user_name=user_name,
            user_dob=user_dob,
            user_number=user_number,
            is_pdf=is_pdf
        )
        return result
    except Exception as e:
        if target_path.exists():
            try:
                target_path.unlink()
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Screening processing failure: {str(e)}")

@router.get("/history", response_model=List[ScreeningSummary])
def get_screening_history(
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Returns minimal screening audit history."""
    records = list_screenings(limit=limit, offset=offset)
    return [
        ScreeningSummary(
            id=r["id"],
            document_type=r["document_type"],
            filename=r["filename"],
            risk_level=r["risk_level"],
            risk_score=r["risk_score"],
            confidence=r["confidence"],
            recommendation=r["recommendation"],
            created_at=r["created_at"]
        )
        for r in records
    ]

@router.get("/screening/{screening_id}")
def get_screening_details(screening_id: str):
    """Retrieves full details for a previous screening."""
    rec = get_screening_by_id(screening_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Screening record not found.")
    
    # Add URLs
    rec["preview_url"] = f"/api/files/{rec.get('stored_filename')}" if rec.get("stored_filename") else None
    rec["ela_url"] = f"/api/files/{screening_id}_ela.jpg" if rec.get("has_ela") else None
    rec["disclaimer"] = DISCLAIMER_TEXT
    return rec

@router.delete("/screening/{screening_id}")
def delete_screening_record(screening_id: str):
    """
    Privacy & Safety compliance:
    Permanently purges document image from disk and marks record as deleted.
    """
    rec = get_screening_by_id(screening_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Screening record not found.")

    # 1. Delete stored image file
    stored = rec.get("stored_filename")
    if stored:
        file_path = UPLOAD_DIR / stored
        if file_path.exists():
            try:
                file_path.unlink()
            except:
                pass
                
    # 2. Delete ELA visualization file
    ela_path = UPLOAD_DIR / f"{screening_id}_ela.jpg"
    if ela_path.exists():
        try:
            ela_path.unlink()
        except:
            pass

    # 3. Soft/hard delete in database
    mark_screening_deleted(screening_id)

    return {
        "success": True,
        "message": f"Screening #{screening_id[:8]} and associated document files were permanently purged."
    }

@router.get("/files/{filename}")
def serve_file(filename: str):
    """Safely serves uploaded preview and ELA images."""
    # Prevent directory traversal
    clean_name = Path(filename).name
    file_path = UPLOAD_DIR / clean_name
    if not file_path.exists():
        # Check samples dir
        file_path = SAMPLES_DIR / clean_name
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found.")
            
    return FileResponse(file_path)
