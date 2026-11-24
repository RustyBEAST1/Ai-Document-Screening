import cv2
import numpy as np
from typing import Dict, Any, List

def analyze_image_quality(img_bgr: np.ndarray) -> Dict[str, Any]:
    """
    Analyzes blur, glare hotspots, lighting uniformity, shadows, resolution, and document boundaries.
    """
    h, w = img_bgr.shape[:2]
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    issues: List[Dict[str, Any]] = []
    
    # 1. Blur detection using Laplacian variance
    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    is_blurry = False
    blur_level = "sharp"
    if laplacian_var < 50.0:
        is_blurry = True
        blur_level = "severe"
        issues.append({
            "id": "qual_severe_blur",
            "severity": "high",
            "category": "Quality",
            "title": "Severe Image Blurriness",
            "description": f"The document image is out of focus (sharpness score: {laplacian_var:.1f}). Text and security features cannot be reliably verified."
        })
    elif laplacian_var < 100.0:
        is_blurry = True
        blur_level = "moderate"
        issues.append({
            "id": "qual_moderate_blur",
            "severity": "medium",
            "category": "Quality",
            "title": "Moderate Blurriness Detected",
            "description": f"Fine details appear softened (sharpness score: {laplacian_var:.1f}). Verification confidence is reduced."
        })

    # 2. Glare and specular hotspot detection (localized flash washout)
    # Instead of counting all light pixels (which includes white paper),
    # find localized clusters of saturated pixels (>252) with high circularity or compactness
    saturated = (gray >= 253).astype(np.uint8)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(saturated)
    
    glare_hotspots = 0
    max_glare_area = 0
    total_glare_pixels = 0
    
    # Filter connected components that look like flash/glare blobs
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        bw = stats[i, cv2.CC_STAT_WIDTH]
        bh = stats[i, cv2.CC_STAT_HEIGHT]
        # Flash glare typically forms a cluster of at least 800-1500 pixels with compact aspect ratio
        if area > 1200 and (0.3 < (bw / max(bh, 1)) < 3.0):
            glare_hotspots += 1
            total_glare_pixels += area
            if area > max_glare_area:
                max_glare_area = area
                
    glare_pct = (total_glare_pixels / float(h * w)) * 100.0
    
    if glare_hotspots >= 1 and (glare_pct > 4.0 or max_glare_area > 8000):
        issues.append({
            "id": "qual_severe_glare",
            "severity": "high",
            "category": "Quality",
            "title": "Severe Glare / Flash Washout",
            "description": f"Camera flash or specular reflection detected ({glare_pct:.1f}% surface area obscured), washing out document details."
        })
    elif glare_hotspots >= 1 and glare_pct > 1.5:
        issues.append({
            "id": "qual_moderate_glare",
            "severity": "medium",
            "category": "Quality",
            "title": "Moderate Glare Detected",
            "description": f"Specular reflections detected across localized areas of the document."
        })

    # 3. Shadows and uneven lighting across 4x4 grid
    grid_h = max(h // 4, 1)
    grid_w = max(w // 4, 1)
    grid_means = []
    for r in range(4):
        for c in range(4):
            patch = gray[r*grid_h:(r+1)*grid_h, c*grid_w:(c+1)*grid_w]
            if patch.size > 0:
                grid_means.append(float(np.mean(patch)))
    lighting_std = float(np.std(grid_means)) if grid_means else 0.0
    if lighting_std > 65.0:
        issues.append({
            "id": "qual_heavy_shadows",
            "severity": "medium",
            "category": "Quality",
            "title": "Uneven Lighting & Harsh Shadows",
            "description": f"High exposure variance ({lighting_std:.1f}) across document quadrants."
        })

    # 4. Low resolution check
    total_pixels = h * w
    if w < 500 or h < 350 or total_pixels < 200000:
        issues.append({
            "id": "qual_low_resolution",
            "severity": "high",
            "category": "Quality",
            "title": "Low Resolution Image",
            "description": f"Document resolution is only {w}x{h}. High-resolution scan or photo required for tamper screening."
        })

    # 5. Cropped / perspective / boundary check
    aspect_ratio = float(w) / float(h)
    if aspect_ratio < 0.7 or aspect_ratio > 2.6:
        issues.append({
            "id": "qual_bad_aspect_ratio",
            "severity": "medium",
            "category": "Quality",
            "title": "Irregular Document Dimensions / Aspect Ratio",
            "description": f"Document aspect ratio is {aspect_ratio:.2f}, suggesting heavy cropping or skew."
        })

    return {
        "width": w,
        "height": h,
        "sharpness_score": round(laplacian_var, 1),
        "blur_level": blur_level,
        "glare_percentage": round(glare_pct, 1),
        "lighting_uniformity_std": round(lighting_std, 1),
        "aspect_ratio": round(aspect_ratio, 2),
        "issues": issues
    }
