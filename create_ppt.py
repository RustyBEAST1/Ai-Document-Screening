import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUT_DIR = Path("C:/Users/user/AG01")
OUT_DIR_MUSIC = Path("C:/Users/user/Music/AG01")
DIAGRAM_PATH = OUT_DIR / "system_architecture_diagram.png"

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    c_navy = RGBColor(15, 23, 42)      # Slate 900
    c_blue = RGBColor(37, 99, 235)     # Blue 600
    c_dark_blue = RGBColor(30, 58, 138)
    c_white = RGBColor(255, 255, 255)
    c_slate_dark = RGBColor(51, 65, 85)
    c_slate_light = RGBColor(241, 245, 249)
    c_emerald = RGBColor(16, 185, 129)
    c_amber = RGBColor(245, 158, 11)
    c_red = RGBColor(239, 68, 68)
    c_purple = RGBColor(124, 58, 237)

    def add_header(slide, title, category="COLLEGE MINOR PROJECT"):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
        p_c = cat_box.text_frame.paragraphs[0]
        r_c = p_c.add_run()
        r_c.text = category.upper()
        r_c.font.size = Pt(11)
        r_c.font.bold = True
        r_c.font.color.rgb = c_blue

        # Main Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        p_t = t_box.text_frame.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.size = Pt(24)
        r_t.font.bold = True
        r_t.font.color.rgb = c_navy

    def add_card(slide, left, top, width, height, title, items, bg_color=c_white, border_color=c_blue):
        # Card background
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        # Title
        t_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.5))
        p = t_box.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = c_navy

        # Items
        b_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), width - Inches(0.4), height - Inches(0.8))
        tf = b_box.text_frame
        tf.word_wrap = True
        for idx, item in enumerate(items):
            p_item = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p_item.space_before = Pt(6)
            if isinstance(item, tuple):
                r_lead = p_item.add_run()
                r_lead.text = "• " + item[0] + ": "
                r_lead.font.bold = True
                r_lead.font.size = Pt(11.5)
                r_lead.font.color.rgb = c_blue

                r_body = p_item.add_run()
                r_body.text = item[1]
                r_body.font.size = Pt(11)
                r_body.font.color.rgb = c_slate_dark
            else:
                r_lead = p_item.add_run()
                r_lead.text = "• " + item
                r_lead.font.size = Pt(11)
                r_lead.font.color.rgb = c_slate_dark

    # ==================== SLIDE 1: Title Slide ====================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.fill.background()

    # Title container
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(2.2))
    p1 = t_box.text_frame.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "AI Fake Identity & Document\nScreening System"
    r1.font.size = Pt(36)
    r1.font.bold = True
    r1.font.color.rgb = c_white

    p2 = t_box.text_frame.add_paragraph()
    p2.space_before = Pt(14)
    r2 = p2.add_run()
    r2.text = "A Multi-Pillar Forensic & Regulatory Checksum Verification Platform"
    r2.font.size = Pt(18)
    r2.font.color.rgb = RGBColor(147, 197, 253) # Light Blue 300

    # Meta card
    meta_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.5), Inches(10.9), Inches(1.8))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = RGBColor(30, 41, 59) # Slate 800
    meta_box.line.color.rgb = c_blue
    meta_box.line.width = Pt(1.5)

    mtf = meta_box.text_frame
    mtf.word_wrap = True
    mp1 = mtf.paragraphs[0]
    mp1.text = "College Minor Project Evaluation | Department of Computer Science & Engineering"
    mp1.font.size = Pt(13)
    mp1.font.bold = True
    mp1.font.color.rgb = c_white

    mp2 = mtf.add_paragraph()
    mp2.space_before = Pt(6)
    mp2.text = "Scope: Automated Preliminary Tampering Screening & Mathematical Format Verification"
    mp2.font.size = Pt(11)
    mp2.font.color.rgb = RGBColor(203, 213, 225)

    mp3 = mtf.add_paragraph()
    mp3.space_before = Pt(6)
    mp3.text = "Presented by: Student Project Team | Guided by: Project Coordinator / Faculty Guide"
    mp3.font.size = Pt(11)
    mp3.font.color.rgb = RGBColor(148, 163, 184)

    # ==================== SLIDE 2: Problem Statement ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Industry Motivation")
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "The Identity Fraud Challenge", [
                 ("Explosion of Digital Tampering", "Readily available digital editors (Photoshop, mobile apps) allow fraudsters to easily modify names, dates of birth, and identity numbers on scanned IDs."),
                 ("Manual Verification Bottlenecks", "Human KYC verifiers process hundreds of documents daily, suffering visual fatigue and failing to notice subtle pixel-level font inconsistencies."),
                 ("High Cost of Official APIs", "Direct live government verification APIs (such as NSDL for PAN or UIDAI OTP) carry financial costs per query and require user consent for every preliminary lead."),
                 ("Syndicate Document Reuse", "Fraudulent syndicates submit identical recycled scans across multiple applications with slight crops to evade detection.")
             ])
    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Our Proposed Solution", [
                 ("Automated Preliminary Screening", "Acts as a fast first-line defense filter that triages clean documents from manipulated ones before costly manual or API verification."),
                 ("Objective Risk Score (0-100)", "Replaces subjective human guesswork with standardized mathematical scoring and risk tiers (Low, Medium, High)."),
                 ("Zero Cloud Exposure", "Entire computer vision and OCR pipeline executes locally, guaranteeing applicant data confidentiality."),
                 ("Multi-Angle Verification", "Combines Error Level Analysis (ELA), camera sensor noise consistency, Haar facial biometrics, and dihedral group D5 checksums.")
             ], border_color=c_emerald)

    # ==================== SLIDE 3: Project Objectives & Scope ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Project Objectives & Scope (Version 1.0)")
    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Primary Engineering Objectives", [
                 ("Zero-Friction User Experience", "Designed for non-technical verifiers: 1 upload zone, 1 document type selector, 1 action button, and an immediate visual result card."),
                 ("Multi-Pillar Image Forensics", "Simultaneous analysis of focus sharpness, flash washout glare, quadrant lighting, JPEG re-compression error, and sensor noise consistency."),
                 ("Official Format & Checksum Parsing", "Mathematical syntax validation enforcing Indian UIDAI, Income Tax Department, Sarathi Transport, and ICAO standards."),
                 ("Privacy by Design", "Automated client-side masking of sensitive identity numbers (XXXX-XXXX-1234) and a permanent 1-click file purge API.")
             ])
    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Strictly Supported Documents (v1.0)", [
                 ("1. Aadhaar Card", "12-digit UIDAI format + Dihedral group D5 Verhoeff checksum algorithm + QR pattern detection."),
                 ("2. PAN Card", "10-character alphanumeric regex + 4th-char entity validation (Individual 'P', Company 'C', Firm 'F')."),
                 ("3. Driving Licence", "Indian Sarathi standard format + verification against all 36 Indian State/UT transport codes."),
                 ("4. Voter ID Card (EPIC)", "Standard Election Commission 3-letter uppercase prefix + 7-digit serial number format."),
                 ("5. Passport", "Standard Indian booklet 1-letter + 7-digit format + 2-line ICAO Doc 9303 weighted (7-3-1) MRZ checksum.")
             ], border_color=c_emerald)

    # ==================== SLIDE 4: Architecture Diagram Slide ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Architecture & End-to-End Pipeline")
    if DIAGRAM_PATH.exists():
        s4.shapes.add_picture(str(DIAGRAM_PATH), Inches(0.8), Inches(1.5), width=Inches(11.7))

    # ==================== SLIDE 5: Forensic Screening Engine ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Multi-Pillar Computer Vision & Forensic Engine")
    add_card(s5, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "A. Quality & Capture", [
                 ("Laplacian Blur", "Second-order derivative variance across luminance. Variance < 50 indicates severe out-of-focus blur."),
                 ("Specular Glare", "Connected-component analysis on saturated pixels (>252 lux) flags flash washout clusters > 1,200 px."),
                 ("Shadows / Exposure", "4x4 spatial grid variance. Standard deviation > 65 indicates harsh shadow angles."),
                 ("Geometry & Crop", "Validates ISO/IEC 7810 ID-1 aspect ratio (~1.58). Flags truncated boundaries.")
             ], border_color=c_blue)

    add_card(s5, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "B. Splicing & ELA", [
                 ("Error Level Analysis", "Saves image at 90% JPEG quality, calculates difference |orig - resaved| scaled 20x. Spikes reveal altered regions."),
                 ("Sensor Noise Disparity", "High-pass Laplacian filtering measures noise across 64x64 patches. Disparities indicate mixed source files."),
                 ("Smudge & Erasure", "Detects unnaturally flat gradient patches where micro-security printing is erased."),
                 ("Clone Stamp Detection", "Flags repetitive pixel patches used to cover original text.")
             ], border_color=c_amber)

    add_card(s5, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "C. Face & Re-use", [
                 ("Haar Face Detection", "OpenCV frontal face cascade ensures portrait presence on cards requiring one."),
                 ("Photo Seam Analysis", "Edge gradient density along the photo border detects physical cut-and-paste seams."),
                 ("SHA-256 Hashing", "Cryptographic fingerprinting catches exact duplicate file resubmissions."),
                 ("64-bit dHash", "Perceptual difference hashing catches visually identical, slightly resized recycled IDs.")
             ], border_color=c_emerald)

    # ==================== SLIDE 6: Mathematical Validation ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Mathematical Syntax & Regulatory Checksums")
    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Aadhaar Verhoeff Algorithm (Dihedral Group D5)", [
                 ("Mathematical Foundation", "UIDAI uses the Verhoeff algorithm utilizing permutations and multiplication tables over dihedral group D5 (symmetries of a regular pentagon)."),
                 ("12th-Digit Checksum", "The 12th digit is calculated from the first 11 digits: c = sum(d[c][p[i % 8][digit]]). A valid number yields c == 0."),
                 ("Error Detection Capability", "Catches 100% of single-digit transcription errors and 100% of adjacent transposition errors (e.g., swapping 45 to 54)."),
                 ("Forgery Prevention", "Randomly typed or artificially generated 12-digit numbers fail with over 99% probability.")
             ])
    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Regulatory Standards & Passport MRZ", [
                 ("PAN Entity Classification", "Validates 4th character against official Income Tax Act categories: P (Individual), C (Company), H (HUF), F (Firm), T (Trust)."),
                 ("Driving Licence Sarathi Standard", "Validates 2-letter state code + 2-digit RTO + 4-digit year + 7-digit serial against Parivahan database rules."),
                 ("Voter ID (EPIC) Syntax", "Validates 3 uppercase alphabetic prefix + 7 numeric digits established by Election Commission of India."),
                 ("Passport ICAO Doc 9303 MRZ", "Computes weighted modulo-10 checksums using cyclic weighting factors [7, 3, 1] on passport number and birthdate.")
             ], border_color=c_emerald)

    # ==================== SLIDE 7: Privacy & Security ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Privacy by Design & Compliance Architecture")
    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Data Minimization & Preview Masking", [
                 ("Default Identity Masking", "Aadhaar numbers masked to 'XXXX-XXXX-1234' (only last 4 digits displayed). PAN masked to 'ABCDE****F'."),
                 ("Address Redaction", "Residential addresses are masked by default to protect applicant privacy in shared verifier environments."),
                 ("Authorized Reveal Toggle", "Verifier can explicitly toggle unmasking if audit verification requires cross-checking."),
                 ("Zero Persistent Public Transmission", "Scans remain within the isolated server runtime and are never shared with third-party public cloud APIs.")
             ])
    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Lifecycle Control & Compliance", [
                 ("1-Click Permanent File Purge", "The result view includes 'Delete Document & Purge Scan', immediately executing DELETE /api/screening/{id}."),
                 ("Disk & Database Purge", "Permanently unlinks the uploaded image file, deletes the ELA heatmap visualization, and flags the DB record as purged."),
                 ("Mandatory Legal Disclaimer", "Rendered prominently: 'This tool provides an AI-based preliminary screening only. It does not replace official government verification, KYC checks, or human review.'"),
                 ("Immutable Audit Log", "SQLite database maintains screening timestamp, document type, risk score, and tamper findings for compliance review.")
             ], border_color=c_red)

    # ==================== SLIDE 8: Tech Stack & Implementation ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Technical Stack & Software Architecture")
    add_card(s8, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Frontend Architecture", [
                 ("Dual Delivery Modes", "1. Standalone zero-build HTML5/CSS3/JS app (instant execution).\n2. Modular React 18 + Tailwind CSS + Lucide Icons."),
                 ("Clean Minimal Design", "White card-based layout, large readable text, responsive on mobile & desktop."),
                 ("Interactive Visualizations", "Circular SVG risk score gauge, animated scanning laser, ELA heatmap tab."),
                 ("Audit History Modal", "Slide-over history inspector.")
             ], border_color=c_blue)

    add_card(s8, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Backend API Framework", [
                 ("FastAPI (Python 3.10+)", "Asynchronous high-throughput ASGI framework with automatic OpenAPI/Swagger documentation."),
                 ("Pydantic Schemas", "Strict input validation for multipart file uploads and cross-check metadata."),
                 ("Stateless REST Endpoints", "Clean separation of upload, history, sample screening, and deletion routes."),
                 ("One-Command Launcher", "python run.py bootstraps database, checks samples, and launches browser.")
             ], border_color=c_purple)

    add_card(s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "AI & Data Layer", [
                 ("OpenCV & NumPy", "Laplacian filters, thresholding, connected components, Haar cascades."),
                 ("PIL & ImageChops", "High-precision Error Level Analysis difference computation."),
                 ("Multi-Engine OCR", "Windows Native Media OCR bridge + fallback image preprocessing."),
                 ("SQLite Database", "Indexed audit storage on file_hash, perceptual_hash, and created_at.")
             ], border_color=c_emerald)

    # ==================== SLIDE 9: Results & Case Studies ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Empirical Results & Test Case Evaluations")
    add_card(s9, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Case 1: Clean Aadhaar (Genuine)", [
                 ("Document Type", "Aadhaar Card (UIDAI Layout)"),
                 ("Forensic Findings", "Sharp focus (Laplacian > 150), no glare, uniform 4x4 lighting."),
                 ("Checksum Status", "Valid 12-digit number (Verhoeff checksum passed)."),
                 ("Risk Score", "Score: 20/100 -> LOW RISK (Green)."),
                 ("System Recommendation", "'Proceed for further verification'.")
             ], border_color=c_emerald)

    add_card(s9, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Case 2: Tampered PAN (Spliced)", [
                 ("Document Type", "PAN Card (Altered Date of Birth)"),
                 ("Forensic Findings", "Localized ELA patch variance spike > 4.5x over DOB; sensor noise mismatch."),
                 ("Syntax Status", "Invalid 4th-char entity code 'X'."),
                 ("Risk Score", "Score: 78/100 -> HIGH RISK (Red)."),
                 ("System Recommendation", "'Verify manually: Splicing detected'.")
             ], border_color=c_red)

    add_card(s9, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Case 3: Blurry Driving Licence", [
                 ("Document Type", "Driving Licence (Capture Defect)"),
                 ("Forensic Findings", "Laplacian variance < 40 (severe blur), specular flash washout > 6%."),
                 ("OCR Status", "Text unreadable; transport keywords missing."),
                 ("Risk Score", "Score: 88/100 -> HIGH RISK (Red)."),
                 ("System Recommendation", "'Verify manually: Image quality insufficient'.")
             ], border_color=c_amber)

    # ==================== SLIDE 10: Conclusion & Future Scope ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Conclusion & Future Research Directions")
    add_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Key Contributions & Achievements", [
                 ("Lightweight & Practical", "Operates entirely on standard CPU hardware without demanding expensive cloud GPU resources."),
                 ("Hybrid Forensic Pipeline", "Integrates physical image quality, digital compression physics, face biometrics, and mathematical checksums."),
                 ("Privacy & Governance", "Fully aligned with data protection principles through client-side masking and instant file deletion."),
                 ("Immediate Academic & Industry Utility", "Provides an automated preliminary triage layer for fintechs, banks, and academic institutions.")
             ])
    add_card(s10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Future Scope & Enhancements", [
                 ("DigiLocker / NSDL API Bridge", "Integrating sanctioned government API lookups for documents marked as Low Risk."),
                 ("Holographic / Microprint Analysis", "Adding multi-spectral flash reflection models to verify optical variable ink (OVI) and holograms."),
                 ("Deep Splicing Transformers", "Incorporating lightweight MobileNet-based deep forensic models for edge tampering detection."),
                 ("Mobile SDK Deployment", "Packaging forensic algorithms into a native Android/iOS camera SDK with real-time glare feedback.")
             ], border_color=c_blue)

    ppt_path = OUT_DIR / "AI_Identity_Screening_Presentation.pptx"
    prs.save(str(ppt_path))
    print("Saved PPTX to:", ppt_path)
    return ppt_path

if __name__ == "__main__":
    create_presentation()
