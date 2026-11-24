import hashlib
import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, List, Dict, Any

def compute_sha256(file_path: Path) -> str:
    """Computes exact cryptographic SHA-256 hash."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def compute_dhash(img_bgr: np.ndarray, hash_size: int = 8) -> str:
    """
    Computes 64-bit Difference Hash (dHash).
    Resizes image to (hash_size + 1, hash_size), converts to gray,
    compares adjacent columns to form binary hash string.
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hash_size + 1, hash_size), interpolation=cv2.INTER_AREA)
    diff = resized[:, 1:] > resized[:, :-1]
    # Convert bool array to hex string
    bit_string = "".join(["1" if b else "0" for b in diff.flatten()])
    # Convert binary to hex
    hex_hash = f"{int(bit_string, 2):0{hash_size * hash_size // 4}x}"
    return hex_hash

def hamming_distance(hex1: str, hex2: str) -> int:
    """Calculates bit difference (Hamming distance) between two hex hashes."""
    if not hex1 or not hex2 or len(hex1) != len(hex2):
        return 999
    try:
        val1 = int(hex1, 16)
        val2 = int(hex2, 16)
        xor_val = val1 ^ val2
        return bin(xor_val).count("1")
    except:
        return 999

def check_duplicate_image(
    file_hash: str,
    perceptual_hash: str,
    recent_records: List[Dict[str, Any]],
    current_screening_id: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """
    Checks if this image is an exact or near duplicate of a previously screened document.
    Returns: (is_duplicate, match_type, matched_record)
    """
    for rec in recent_records:
        rec_id = rec.get("id")
        if current_screening_id and rec_id == current_screening_id:
            continue
            
        rec_sha = rec.get("file_hash")
        rec_phash = rec.get("perceptual_hash")
        
        # 1. Exact SHA-256 duplicate
        if rec_sha and rec_sha == file_hash:
            return True, "Exact File Duplicate", rec
            
        # 2. Perceptual near-duplicate (dHash distance <= 3)
        if rec_phash and perceptual_hash:
            dist = hamming_distance(perceptual_hash, rec_phash)
            if dist <= 3:
                return True, f"Perceptual Visual Match (Distance: {dist})", rec
                
    return False, None, None
