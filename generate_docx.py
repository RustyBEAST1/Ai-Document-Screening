import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text, title="IMPORTANT NOTE", border_color="2563EB", bg_color="EFF6FF"):
    """Adds a GitHub / Notion style callout block."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_title = p.add_run(f"📌 {title}: ")
    run_title.bold = True
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = RGBColor.from_string(border_color)
    
    run_text = p.add_run(text)
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = RGBColor(51, 65, 85)

def add_code_block(doc, code_str, language=""):
    """Adds a dark-themed code block."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, "0F172A") # Slate 900
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(241, 245, 249) # Slate 100

def create_document():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(6)

    # Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("AI Fake Identity & Document Screening System")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(24)
    run_title.bold = True
    run_title.font.color.rgb = RGBColor(37, 99, 235) # Blue 600

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    run_sub = sub_p.add_run("Complete System Specification, Forensic Logic, API Reference & Code Architecture")
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(71, 85, 105) # Slate 600

    # Mandatory Legal Disclaimer Callout
    add_callout(
        doc,
        "This tool provides an AI-based preliminary screening only. It does not replace official government verification, KYC checks, or human review. Do not use as a sole legal determination.",
        title="MANDATORY VERIFIER DISCLAIMER",
        border_color="DC2626",
        bg_color="FEF2F2"
    )

    doc.add_paragraph() # Spacing

    # Section 1: Executive Overview & Goal
    h1 = doc.add_heading(level=1)
    r = h1.add_run("1. Executive Overview & Goal")
    r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "The AI Fake Identity & Document Screening System is a lightweight, mobile-friendly web application designed to help authorized verifiers quickly screen uploaded identity documents for signs of digital tampering, forgery, low-quality manipulation, mismatched details, and suspicious formatting. The system computes an automated, objective Risk Score (0–100) and categorizes documents into Low, Medium, or High Risk levels accompanied by an actionable recommendation (such as 'Verify manually' or 'Proceed for further verification')."
    )

    # Section 2: Important UI Rules & User Flow
    h1 = doc.add_heading(level=1)
    r = h1.add_run("2. UI Rules & Simplified User Flow")
    r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "To ensure effortless operation by non-technical operators and field verifiers, the user interface adheres to strict simplicity principles:"
    )

    flow_points = [
        ("Zero Clutter Layout", "Single main screen with a prominent, drag-and-drop document upload area and clear camera upload support on mobile devices."),
        ("Strict 5-Document Dropdown", "A single dropdown containing ONLY the 5 authorized Indian identity document types. No other document types are permitted."),
        ("One-Action Trigger", "One primary 'Start Screening' button with an animated scanning radar visualization during processing."),
        ("Clean Result Screen", "Results presented in simple cards: Document Type, Overall Risk Level, Risk Score Gauge (0-100), Detected Issues list with severity tags, Extracted Details with privacy masking, and System Recommendation."),
        ("No Complex Dashboards", "Eliminates multi-level menus, advanced forensic sliders, and complex settings. The operator flow is strictly: Select document -> Upload -> Get simple risk result.")
    ]

    for title, desc in flow_points:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{title}: ")
        r_b.bold = True
        p.add_run(desc)

    # Section 3: Supported Document Types
    h1 = doc.add_heading(level=1)
    r = h1.add_run("3. Supported Document Types (Version 1.0)")
    r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "For Version 1.0, the application strictly accepts and validates only the following five document types:"
    )

    table_docs = doc.add_table(rows=6, cols=3)
    table_docs.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_docs.columns[0].width = Inches(1.8)
    table_docs.columns[1].width = Inches(2.3)
    table_docs.columns[2].width = Inches(2.4)

    headers = ["Document Type", "Official Format & Syntax", "Mathematical / Integrity Checks"]
    for i, h in enumerate(headers):
        cell = table_docs.cell(0, i)
        set_cell_background(cell, "1E293B") # Slate 800
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(9.5)

    doc_rows = [
        ("1. Aadhaar Card", "12-digit number (spaced 'XXXX XXXX XXXX' or 12 continuous digits)", "Dihedral group D5 Verhoeff checksum algorithm + Secure QR code scanning"),
        ("2. PAN Card", "10-character alphanumeric: 5 letters + 4 digits + 1 letter", "4th-character entity status validation (P, C, H, A, B, G, J, L, F, T)"),
        ("3. Driving Licence", "Indian Sarathi format: 2-letter state code + 2-digit RTO + year + 7 digits", "Validation against 36 Indian State and Union Territory transport codes"),
        ("4. Voter ID Card (EPIC)", "Standard ECI format: 3 uppercase letters + 7 digits", "Election Commission of India alphanumeric prefix verification"),
        ("5. Passport", "Standard Indian booklet: 1 letter + 7 digits", "ICAO Doc 9303 weighted (7-3-1) Machine Readable Zone (MRZ) checksum")
    ]

    for row_idx, (col1, col2, col3) in enumerate(doc_rows, start=1):
        row = table_docs.rows[row_idx]
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate([col1, col2, col3]):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            run = p.add_run(text)
            run.font.size = Pt(9.5)

    doc.add_paragraph() # Spacing

    # Section 4: What the AI Checks
    h1 = doc.add_heading(level=1)
    r = h1.add_run("4. Comprehensive AI Forensic & Verification Pipeline")
    r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "Every uploaded identity document undergoes a multi-layer inspection pipeline combining computer vision, digital image forensics, optical character recognition, and mathematical syntax validation:"
    )

    ai_checks = [
        ("Blur & Focus Analysis", "Calculates Laplacian variance across grayscale luminance. Scores below 50 indicate severe out-of-focus blur; scores between 50 and 100 indicate moderate blur."),
        ("Flash Glare & Specular Reflection", "Performs connected component analysis on saturated pixels (>252 luminance). Localized compact clusters larger than 1,200 pixels trigger glare warnings, detecting flash washout over text."),
        ("Shadows & Uneven Lighting", "Splits the document into a 4x4 spatial grid. Standard deviation of mean block luminance exceeding 65.0 flags harsh shadows or uneven angle exposure."),
        ("Resolution & Aspect Ratio", "Checks if dimensions meet standard ID card geometry (ISO/IEC 7810 ID-1 aspect ratio ~1.58). Flagged if cropped or skewed (<0.7 or >2.6)."),
        ("Error Level Analysis (ELA)", "Resaves the image at 90% JPEG quality and measures absolute pixel difference |original - resaved| scaled 20x. Computes localized 8x8 patch variance disparities. Spliced elements or modified text yield elevated error spikes."),
        ("Sensor Noise Disparity", "High-pass Laplacian filtering across 64x64 grids measures sensor noise consistency. Spliced patches from different sources create abnormal variance disparity ratios."),
        ("Face / Photo Biometrics", "OpenCV Haar Cascade frontal face detector checks for the holder photograph. Detects missing photos, multiple faces, and checks edge gradient density along the photo border to catch physical or digital photo pasting seams."),
        ("Cryptographic & Perceptual Re-use", "Computes SHA-256 for exact duplicate files and 64-bit difference hash (dHash) for near-duplicate resized images, immediately detecting recycled IDs across fraud syndicates."),
        ("Multi-Engine OCR Extraction", "Automated pipeline utilizing Windows Native Media OCR with fallback contrast enhancement and regex extraction for name, date of birth, document number, and official government keywords."),
        ("Mathematical Checksums", "Verhoeff algorithm verification for Aadhaar 12th digit; ICAO Doc 9303 weighted checksum for Passport MRZ."),
        ("Optional Field Cross-Checking", "When the verifier optionally provides Name, Date of Birth, or Document Number, the system performs fuzzy Levenshtein similarity matching (>=80% match, 50-79% partial, <50% mismatch) and date normalization.")
    ]

    for title, desc in ai_checks:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{title}: ")
        r_b.bold = True
        p.add_run(desc)

    # Section 5: Risk Scoring Algorithm & Recommendations
    h1 = doc.add_heading(level=1)
    r = h1.add_run("5. Risk Scoring Engine & Recommendation Logic")
    r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "The risk engine aggregates detected anomalies into a normalized 0–100 integer Risk Score based on weighted severity deductions:"
    )

    table_risk = doc.add_table(rows=4, cols=4)
    table_risk.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_risk.columns[0].width = Inches(1.3)
    table_risk.columns[1].width = Inches(1.2)
    table_risk.columns[2].width = Inches(1.8)
    table_risk.columns[3].width = Inches(2.2)

    risk_headers = ["Risk Level", "Score Range", "Indicator Color", "Standard Recommendation"]
    for i, h in enumerate(risk_headers):
        cell = table_risk.cell(0, i)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(9.5)

    risk_data = [
        ("Low Risk", "0 – 35", "Green (#10B981)", "Proceed for further verification (no major anomalies detected)."),
        ("Medium Risk", "36 – 69", "Yellow / Amber (#F59E0B)", "Verify manually (quality defects, minor blur, or partial syntax deviations)."),
        ("High Risk", "70 – 100", "Red (#EF4444)", "Verify manually (critical checksum failure, ELA splicing, photo seam, or name mismatch).")
    ]

    for row_idx, (col1, col2, col3, col4) in enumerate(risk_data, start=1):
        row = table_risk.rows[row_idx]
        bg = "ECFDF5" if row_idx == 1 else ("FFFBEB" if row_idx == 2 else "FEF2F2")
        for col_idx, text in enumerate([col1, col2, col3, col4]):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            run = p.add_run(text)
            if col_idx == 0:
                run.bold = True
            run.font.size = Pt(9.5)

    doc.add_paragraph() # Spacing

    # Section 6: Privacy and Security Compliance
    h1 = doc.add_heading(level=1)
    r = h1.add_run("6. Privacy, Security & Data Protection Controls")
    r.font.color.rgb = RGBColor(15, 23, 42)

    privacy_points = [
        ("Automated Preview Masking", "Aadhaar numbers are masked by default to 'XXXX-XXXX-1234' (only last 4 digits revealed). PAN numbers are masked to 'ABCDE****F'. Sensitive residential addresses are redacted in previews. Verifiers have an explicit 'Reveal / Mask' toggle button."),
        ("Immediate File Purge API", "The result screen provides a 'Delete Document & Purge Scan' button that invokes DELETE /api/screening/{id}. This permanently deletes the uploaded scan and ELA heatmap from disk and marks the database record as purged."),
        ("No External Cloud Transmission", "Forensics and OCR run entirely in the local application execution environment. Documents are never transmitted to unauthorized third-party public cloud endpoints."),
        ("Disclaimer Display", "Prominently displayed across all application headers and reports: 'This tool provides an AI-based preliminary screening only. It does not replace official government verification, KYC checks, or human review.'")
    ]

    for title, desc in privacy_points:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{title}: ")
        r_b.bold = True
        p.add_run(desc)

    # Section 7: Complete Code Architecture & Files
    h1 = doc.add_heading(level=1)
    r = h1.add_run("7. Key Code Implementation Reference")
    r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "Below are the primary implementation highlights from the application codebase:"
    )

    # Verhoeff Algorithm
    h2 = doc.add_heading(level=2)
    h2.add_run("7.1 Aadhaar Verhoeff Checksum Algorithm (verhoeff.py)")
    add_code_block(doc, """# Dihedral Group D5 tables for official Aadhaar 12th-digit verification
d_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]
p_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

def validate_verhoeff(num_str: str) -> bool:
    clean = "".join(filter(str.isdigit, str(num_str)))
    if not clean or len(clean) != 12:
        return False
    c = 0
    reversed_digits = [int(x) for x in reversed(clean)]
    for i, digit in enumerate(reversed_digits):
        c = d_table[c][p_table[i % 8][digit]]
    return c == 0""")

    # Error Level Analysis
    h2 = doc.add_heading(level=2)
    h2.add_run("7.2 Error Level Analysis & Tamper Detection (tampering.py)")
    add_code_block(doc, """def compute_ela(image_path: Path, output_ela_path: Path, quality: int = 90):
    orig = Image.open(image_path).convert("RGB")
    buffer = io.BytesIO()
    orig.save(buffer, "JPEG", quality=quality)
    buffer.seek(0)
    resaved = Image.open(buffer)
    
    # Calculate difference
    ela_diff = ImageChops.difference(orig, resaved)
    extrema = ela_diff.getextrema()
    max_diff = max([ex[1] for ex in extrema]) if extrema else 1
    scale = 255.0 / max_diff if max_diff < 12 else 20.0
    
    enhancer = ImageEnhance.Brightness(ela_diff)
    ela_image = enhancer.enhance(scale)
    ela_image.save(output_ela_path, "JPEG")
    
    # Measure localized 8x8 patch variance disparity
    diff_arr = np.array(ela_diff, dtype=np.float32)
    gray_diff = np.mean(diff_arr, axis=2)
    mean_err = float(np.mean(gray_diff))
    max_err = float(np.max(gray_diff))
    std_err = float(np.std(gray_diff))
    
    return mean_err, max_err, std_err""")

    # Section 8: Setup Instructions
    h1 = doc.add_heading(level=1)
    r = h1.add_run("8. Setup & Execution Instructions")
    r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "The application includes an all-in-one launcher script (run.py) that initializes the database, verifies pre-loaded sample documents, launches the web server, and opens your default browser:"
    )

    add_code_block(doc, """# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the application
python run.py

# Access Points:
# Web Application: http://127.0.0.1:8000
# Interactive API Docs (Swagger): http://127.0.0.1:8000/docs""")

    # Section 9: Minimal Admin Panel
    h1 = doc.add_heading(level=1)
    r = h1.add_run("9. Minimal Screening Audit History")
    r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "A discreet 'History' button in the header opens the Screening Audit History modal, displaying past screenings with document type, risk level badge, score (0-100), and timestamp. Verifiers can inspect past detailed reports or permanently purge records."
    )

    return doc

if __name__ == "__main__":
    out_dir_1 = Path("C:/Users/user/AG01")
    out_dir_2 = Path("C:/Users/user/Music/AG01")
    
    doc = create_document()
    file_name = "AI_Fake_Identity_Document_Screening_System_Documentation.docx"
    
    target_1 = out_dir_1 / file_name
    doc.save(str(target_1))
    print("Saved DOCX to:", target_1)
    
    target_2 = out_dir_2 / file_name
    try:
        import shutil
        shutil.copyfile(str(target_1), str(target_2))
        print("Copied DOCX to:", target_2)
    except Exception as e:
        print("Could not copy to Music AG01 directly:", e)
