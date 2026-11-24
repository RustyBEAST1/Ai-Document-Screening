import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import io
from typing import Dict, Any, List, Tuple
from pathlib import Path

def compute_ela(
    image_path: Path,
    output_ela_path: Path,
    quality: int = 90,
    scale: float = 20.0
) -> Tuple[float, float, float, bool]:
    """
    Computes Error Level Analysis (ELA).
    Detects localized compression disparities (signatures of splicing/editing).
    """
    try:
        orig = Image.open(image_path).convert("RGB")
        
        buffer = io.BytesIO()
        orig.save(buffer, "JPEG", quality=quality)
        buffer.seek(0)
        resaved = Image.open(buffer)
        
        ela_diff = ImageChops.difference(orig, resaved)
        
        extrema = ela_diff.getextrema()
        max_diff = max([ex[1] for ex in extrema]) if extrema else 1
        if max_diff == 0:
            max_diff = 1
        
        scale_factor = 255.0 / max_diff if max_diff < 12 else scale
        enhancer = ImageEnhance.Brightness(ela_diff)
        ela_image = enhancer.enhance(scale_factor)
        
        ela_image.save(output_ela_path, "JPEG")
        
        diff_arr = np.array(ela_diff, dtype=np.float32)
        gray_diff = np.mean(diff_arr, axis=2)
        
        mean_err = float(np.mean(gray_diff))
        max_err = float(np.max(gray_diff))
        std_err = float(np.std(gray_diff))
        
        # Split into 8x8 patches and measure patch variance disparity
        h, w = gray_diff.shape
        ph, pw = max(h // 8, 1), max(w // 8, 1)
        patch_means = []
        for r in range(8):
            for c in range(8):
                p = gray_diff[r*ph:(r+1)*ph, c*pw:(c+1)*pw]
                if p.size > 0:
                    patch_means.append(float(np.mean(p)))
                    
        p_arr = np.array(patch_means)
        p_max = float(np.max(p_arr)) if len(p_arr) else 0.0
        p_median = float(np.median(p_arr)) + 1e-4
        disparity_ratio = p_max / p_median
        
        # Suspicious if one localized patch has > 4.5x higher error than the rest
        has_suspicious_zones = (disparity_ratio > 4.5 and p_max > 18.0) or (max_err > 65.0 and std_err > 18.0)
        
        return mean_err, max_err, std_err, has_suspicious_zones
    except Exception:
        return 0.0, 0.0, 0.0, False

def analyze_tampering_and_forgery(
    img_bgr: np.ndarray,
    image_path: Path,
    ela_output_path: Path
) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    
    mean_err, max_err, std_err, has_ela_hotspots = compute_ela(image_path, ela_output_path)
    
    if has_ela_hotspots:
        issues.append({
            "id": "forensic_ela_mismatch",
            "severity": "high",
            "category": "Forensics",
            "title": "Digital Manipulation Detected (ELA Anomaly)",
            "description": (
                f"Error Level Analysis identified localized compression disparities (peak local error: {max_err:.1f}). "
                "Consistent with pasted text, spliced dates, or photo editing."
            )
        })

    # Local noise variance analysis (Splicing / Clone detection)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    high_pass = cv2.Laplacian(gray, cv2.CV_32F)
    patch_size = 64
    noise_variances = []
    for y in range(0, h - patch_size, patch_size):
        for x in range(0, w - patch_size, patch_size):
            patch = high_pass[y:y+patch_size, x:x+patch_size]
            noise_variances.append(float(np.var(patch)))
            
    noise_ratio = 1.0
    if len(noise_variances) >= 8:
        nv_arr = np.array(noise_variances)
        p95 = np.percentile(nv_arr, 95)
        p05 = np.percentile(nv_arr, 5) + 1e-4
        noise_ratio = float(p95 / p05)
        
        # In natural documents with text and background, ratio can be high due to sharp text.
        # Splicing / cut-and-paste is flagged when elevated noise disparity coincides with ELA hotspots
        if noise_ratio > 100.0 and has_ela_hotspots:
            issues.append({
                "id": "forensic_noise_discrepancy",
                "severity": "high",
                "category": "Forensics",
                "title": "Severe Noise Inconsistency (Splicing Signature)",
                "description": f"Abnormal sensor noise variance disparity ({noise_ratio:.1f}) correlating with localized compression anomalies. Indicates spliced content."
            })
        elif noise_ratio > 180.0:
            issues.append({
                "id": "forensic_moderate_noise",
                "severity": "medium",
                "category": "Forensics",
                "title": "Irregular Background Noise Profile",
                "description": f"Noticeable variance disparity ({noise_ratio:.1f}) between background and detail zones."
            })

    return {
        "ela_mean_error": round(mean_err, 2),
        "ela_max_error": round(max_err, 2),
        "ela_std_error": round(std_err, 2),
        "ela_suspicious": has_ela_hotspots,
        "noise_disparity_ratio": round(noise_ratio, 1),
        "issues": issues
    }
