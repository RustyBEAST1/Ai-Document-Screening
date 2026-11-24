# AI Fake Identity & Document Screening System
## Complete System Documentation & Technical Specification

> **Mandatory Disclaimer:** This tool provides an AI-based preliminary screening only. It does not replace official government verification, KYC checks, or human review. Do not use as a sole legal determination.

---

## 1. Executive Summary & Goal
The **AI Fake Identity & Document Screening System** is a clean, simple, mobile-friendly web application designed to help authorized verifiers rapidly screen uploaded identity documents for signs of digital tampering, forgery, low-quality manipulation, mismatched details, and suspicious formatting.

The system provides an automated, objective **preliminary risk assessment (0–100 score with Low/Medium/High risk levels)** and actionable recommendations (such as *"Verify manually"* or *"Proceed for further verification"*), rather than a final legal decision.

---

## 2. Supported Document Types (Version 1.0)
The application strictly supports only the following five Indian identity document types:
1. **Aadhaar Card**: 12-digit UIDAI sequence + official Verhoeff mathematical checksum + QR code detection.
2. **PAN Card**: 10-character alphanumeric `[A-Z]{5}[0-9]{4}[A-Z]` + 4th-character entity code validation.
3. **Driving Licence**: Indian Sarathi format + state transport prefix verification across all 36 Indian States/UTs.
4. **Voter ID Card (EPIC)**: Standard 3-letter uppercase prefix + 7-digit serial number format.
5. **Passport**: Standard Indian passport number + ICAO Doc 9303 weighted (7-3-1) MRZ checksum validation.

---

## 3. Core UI Rules & Simplified User Flow
- **One Main Screen**: Large, intuitive drag-and-drop document upload area with mobile camera capture support.
- **Strict Dropdown**: Only the 5 authorized document types appear in the dropdown.
- **One "Start Screening" Action**: Primary button triggering an animated radar scan indicator during processing.
- **Clear Result Screen**: Shows Risk Level (Low/Medium/High), Risk Score (0-100 gauge), short explanation, detected issues with severity badges, extracted details with privacy masking, and recommendation.
- **Zero Complex Dashboards**: No confusing settings or multi-tier menus. The user flow is strictly:
  $$\text{Select Document} \longrightarrow \text{Upload Photo/Scan/PDF} \longrightarrow \text{Get Risk Result}$$

---

## 4. Comprehensive AI Screening Logic

### A. Image Quality Forensics
- **Focus & Blurriness**: Measures Laplacian variance across grayscale luminance. Values $<50.0$ flag severe blur; values $50.0–100.0$ flag moderate blur.
- **Flash Washout & Glare**: Connected-component analysis on specular saturated clusters ($>252$ brightness) over 1,200 pixels.
- **Shadows & Lighting**: Evaluates standard deviation across a $4 \times 4$ spatial grid. Disparities $>65.0$ flag harsh shadows.
- **Aspect Ratio & Geometry**: Validates geometry against the standard ISO/IEC 7810 ID-1 aspect ratio ($\approx 1.58$). Flags ratios $<0.7$ or $>2.6$.

### B. Digital Tampering & Splicing (ELA)
- **Error Level Analysis (ELA)**: Re-compresses image at 90% JPEG quality, calculates difference $|orig - resaved|$ scaled $20\times$, and evaluates $8 \times 8$ localized patch variance disparities. Spliced patches create significant error spikes.
- **Sensor Noise Consistency**: High-pass Laplacian filtering measures localized noise consistency to catch copy-paste and clone-stamp artifacts.
- **Face & Photo Biometrics**: OpenCV Haar Cascade frontal face detection locates the portrait photo, detects missing or duplicate photos, and analyzes boundary edge gradient density for pasting seams.
- **Cryptographic & Perceptual Re-use**: SHA-256 hash checks for exact duplicate files; 64-bit difference hash (dHash) checks for near-duplicate visual matches across recent submissions.

### C. OCR & Format Validators
- **Multi-Engine OCR**: Windows Native Media OCR with fallback contrast enhancement and regex extraction.
- **Verhoeff Checksum Algorithm**: Dihedral group $D_5$ matrix multiplication verifies the 12th digit of Aadhaar numbers.
- **PAN Entity Verification**: Checks the 4th character against official entity types (`P` = Individual, `C` = Company, `H` = HUF, `F` = Firm, etc.).
- **Passport MRZ Checksum**: Computes weighted $(7, 3, 1)$ ICAO Doc 9303 checksums on the 2-line machine-readable zone.
- **Optional Field Cross-Checking**: Normalized Levenshtein similarity on Name ($\ge 80\%$ match, $50-79\%$ partial, $<50\%$ mismatch), DOB normalization, and Document Number matching.

---

## 5. Risk Scoring & Recommendations

$$\text{Risk Score} = \min\left(100, \max\left(0, \text{Baseline} + \sum \text{Issue Penalties}\right)\right)$$

| Risk Level | Score Range | Indicator Color | Recommendation |
| :--- | :---: | :---: | :--- |
| **Low Risk** | 0 – 35 | Green (`#10B981`) | *Proceed for further verification* |
| **Medium Risk** | 36 – 69 | Yellow / Amber (`#F59E0B`) | *Verify manually* |
| **High Risk** | 70 – 100 | Red (`#EF4444`) | *Verify manually (high probability of tampering)* |

---

## 6. Privacy & Safety Controls
1. **Automated Preview Masking**: Aadhaar numbers masked to `XXXX-XXXX-1234`; PAN numbers masked to `ABCDE****F`. Verifiers can toggle visibility with a single click.
2. **Immediate File Purge**: A **"Delete Document & Purge Scan"** button permanently removes uploaded files and ELA heatmaps from disk.
3. **Local Execution**: Forensics and OCR execute in the local application runtime with no external public transmission.

---

## 7. Setup & Run Instructions
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python run.py
```
- **Web Interface:** http://127.0.0.1:8000
- **Interactive Swagger API Docs:** http://127.0.0.1:8000/docs
