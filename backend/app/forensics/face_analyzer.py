import cv2
import numpy as np
import os
from typing import Dict, Any, List

def detect_photo_frame(gray: np.ndarray) -> tuple[bool, Dict[str, int]]:
    """
    Looks for a rectangular portrait photo frame (approx 35mm x 45mm, ratio 1.2 - 1.45).
    """
    h, w = gray.shape
    edges = cv2.Canny(gray, 40, 120)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        if cw < 60 or ch < 75:
            continue
        # Portrait photo ratio typically 1.15 to 1.55, occupies reasonable card area
        ratio = ch / float(cw)
        area_pct = (cw * ch) / float(w * h)
        if 1.1 <= ratio <= 1.6 and 0.03 <= area_pct <= 0.28:
            # Check if interior has texture/entropy (not plain empty white box)
            roi = gray[y:y+ch, x:x+cw]
            if float(np.std(roi)) > 15.0:
                return True, {"x": int(x), "y": int(y), "width": int(cw), "height": int(ch)}
                
    return False, {}

def analyze_photo_and_face(img_bgr: np.ndarray, doc_type: str) -> Dict[str, Any]:
    """
    Detects face presence, count, and checks for photo box tampering/splicing seams.
    Uses Haar cascades and fallback photo-box frame detection.
    """
    issues: List[Dict[str, Any]] = []
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    # 1. Haar Cascade Frontal Face Detector
    cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.08,
        minNeighbors=3,
        minSize=(int(h * 0.08), int(w * 0.08))
    )
    
    num_faces = len(faces)
    face_detected = num_faces > 0
    face_tamper_detected = False
    primary_face_box = None
    
    if num_faces == 0:
        # Fallback to photo frame detector
        has_frame, frame_box = detect_photo_frame(gray)
        if has_frame:
            face_detected = True
            primary_face_box = frame_box
        else:
            issues.append({
                "id": "forensic_no_face_detected",
                "severity": "high",
                "category": "Forensics",
                "title": "No Portrait Photograph Detected",
                "description": f"Standard {doc_type} requires a clearly visible holder photo. No human face or photo frame was detected in expected regions."
            })
    elif num_faces > 1:
        issues.append({
            "id": "forensic_multiple_faces",
            "severity": "medium",
            "category": "Forensics",
            "title": f"Multiple Faces Detected ({num_faces})",
            "description": "More than one face was detected on the document surface. May indicate a collage, watermark anomaly, or wrong document."
        })
    else:
        (fx, fy, fw, fh) = faces[0]
        primary_face_box = {"x": int(fx), "y": int(fy), "width": int(fw), "height": int(fh)}
        
        # Check boundary edge gradient to detect paste-in lines
        pad = 6
        x1 = max(0, fx - pad)
        y1 = max(0, fy - pad)
        x2 = min(w, fx + fw + pad)
        y2 = min(h, fy + fh + pad)
        
        face_roi = gray[y1:y2, x1:x2]
        if face_roi.size > 0:
            edges = cv2.Canny(face_roi, 80, 200)
            b_pixels = np.concatenate([edges[0, :], edges[-1, :], edges[:, 0], edges[:, -1]])
            border_density = float(np.count_nonzero(b_pixels)) / float(len(b_pixels)) if len(b_pixels) > 0 else 0
            
            if border_density > 0.65:
                face_tamper_detected = True
                issues.append({
                    "id": "forensic_photo_border_seam",
                    "severity": "high",
                    "category": "Forensics",
                    "title": "Suspected Photo Replacement / Border Seam",
                    "description": "Sharp artificial boundary discontinuity detected around the identity photo, indicating possible photo pasting or digital insertion."
                })

    return {
        "face_detected": face_detected,
        "face_count": int(num_faces),
        "primary_face_box": primary_face_box,
        "face_tamper_detected": face_tamper_detected,
        "issues": issues
    }
