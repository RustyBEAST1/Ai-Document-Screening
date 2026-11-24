import os
import cv2
import numpy as np
import subprocess
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

WIN_OCR_SCRIPT = Path(__file__).resolve().parent / "win_ocr.ps1"

def preprocess_image_for_ocr(img_bgr: np.ndarray) -> np.ndarray:
    """Enhance contrast and sharpness for optimal OCR character recognition."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # Resize if too small
    h, w = gray.shape
    if w < 1200:
        scale = 1200.0 / w
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        
    # Contrast Limited Adaptive Histogram Equalization (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Mild bilateral filter to reduce noise while preserving edges
    denoised = cv2.bilateralFilter(enhanced, 7, 50, 50)
    return denoised

def run_windows_ocr(image_path: Path) -> Dict[str, Any]:
    """Runs native Windows OCR engine via PowerShell helper."""
    if not WIN_OCR_SCRIPT.exists():
        return {"success": False, "text": "", "lines": [], "error": "Script missing"}
        
    try:
        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(WIN_OCR_SCRIPT),
            "-ImagePath",
            str(image_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
        out = res.stdout.strip()
        if out:
            data = json.loads(out)
            return data
    except Exception as e:
        return {"success": False, "text": "", "lines": [], "error": str(e)}
        
    return {"success": False, "text": "", "lines": []}

def detect_qr_and_barcodes(img_bgr: np.ndarray) -> Dict[str, Any]:
    """Scans for 2D QR codes and linear barcodes on the document."""
    qr_detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(img_bgr)
    
    qr_found = False
    qr_contents = []
    if retval:
        for info in decoded_info:
            if info and info.strip():
                qr_found = True
                qr_contents.append(info.strip())
                
    if not qr_found:
        val, pts, _ = qr_detector.detectAndDecode(img_bgr)
        if val and val.strip():
            qr_found = True
            qr_contents.append(val.strip())
        elif pts is not None and len(pts) > 0:
            # QR geometric marker detected even if text decoding fails
            qr_found = True

    # Visual finder pattern contour search as fallback
    if not qr_found:
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if hierarchy is not None and len(hierarchy[0]) > 0:
            # Look for 3 nested contours (the signature of QR corner position markers)
            nested_count = 0
            for i, h_info in enumerate(hierarchy[0]):
                child = h_info[2]
                if child != -1 and hierarchy[0][child][2] != -1:
                    nested_count += 1
            if nested_count >= 2:
                qr_found = True

    return {
        "qr_detected": qr_found,
        "qr_contents": qr_contents
    }

def extract_text_from_pdf(pdf_path: Path) -> Tuple[str, List[str]]:
    """Extracts embedded text from a PDF document using pypdf."""
    text_content = ""
    lines = []
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            t = page.extract_text() or ""
            text_content += t + "\n"
            for line in t.splitlines():
                clean_l = line.strip()
                if clean_l:
                    lines.append(clean_l)
    except Exception:
        pass
    return text_content.strip(), lines

def extract_document_ocr(
    img_bgr: np.ndarray,
    image_path: Path,
    is_pdf: bool = False
) -> Dict[str, Any]:
    """
    Main OCR extraction pipeline combining Windows OCR, QR detection, and image preprocessing.
    """
    raw_text = ""
    lines: List[str] = []
    
    # 1. If PDF, first extract embedded text
    if is_pdf:
        pdf_text, pdf_lines = extract_text_from_pdf(image_path)
        if pdf_text:
            raw_text += pdf_text + " "
            lines.extend(pdf_lines)
            
    # 2. Run Windows Native OCR on the preprocessed image
    temp_enhanced = None
    try:
        prep = preprocess_image_for_ocr(img_bgr)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            temp_enhanced = Path(tf.name)
            cv2.imwrite(str(temp_enhanced), prep)
            
        win_res = run_windows_ocr(temp_enhanced)
        if win_res.get("success"):
            ocr_text = win_res.get("text", "")
            raw_text += " " + ocr_text
            lines.extend(win_res.get("lines", []))
    except Exception:
        pass
    finally:
        if temp_enhanced and temp_enhanced.exists():
            try:
                os.remove(temp_enhanced)
            except:
                pass

    # 3. QR / Barcode detection
    qr_res = detect_qr_and_barcodes(img_bgr)
    
    # Clean deduplicated lines
    cleaned_lines = []
    seen = set()
    for l in lines:
        s = l.strip()
        if s and s not in seen:
            seen.add(s)
            cleaned_lines.append(s)

    return {
        "raw_text": raw_text.strip(),
        "lines": cleaned_lines,
        "qr_detected": qr_res["qr_detected"],
        "qr_contents": qr_res["qr_contents"]
    }
