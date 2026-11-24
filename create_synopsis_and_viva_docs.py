import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

OUT_DIR = Path("C:/Users/user/AG01")
OUT_DIR_MUSIC = Path("C:/Users/user/Music/AG01")
DIAGRAM_PATH = OUT_DIR / "system_architecture_diagram.png"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text, title="NOTE", border_color="2563EB", bg_color="EFF6FF"):
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

def add_code_block(doc, code_str):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, "0F172A")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(241, 245, 249)

# ==============================================================================
# DOCUMENT 2: Official College Project Synopsis
# ==============================================================================
def create_synopsis_doc():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # Title Section
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = title_p.add_run("PROJECT SYNOPSIS")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(20)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(37, 99, 235)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = sub_p.add_run("AI Fake Identity & Document Screening System\n(A Multi-Pillar Forensic & Regulatory Format Validation Platform)")
    r_s.font.size = Pt(13)
    r_s.font.bold = True
    r_s.font.color.rgb = RGBColor(15, 23, 42)

    # Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.columns[0].width = Inches(2.2)
    meta_table.columns[1].width = Inches(4.3)
    
    meta_rows = [
        ("Project Category:", "Minor Project / Capstone Project"),
        ("Department & Degree:", "Department of Computer Science & Engineering (B.Tech / BCA / MCA)"),
        ("Domain:", "Artificial Intelligence, Computer Vision, Digital Image Forensics, Full-Stack Web"),
        ("Project Status:", "Fully Designed, Implemented & Verified (v1.0 Ready)")
    ]
    for idx, (label, val) in enumerate(meta_rows):
        row = meta_table.rows[idx]
        set_cell_background(row.cells[0], "F8FAFC")
        set_cell_background(row.cells[1], "FFFFFF")
        set_cell_margins(row.cells[0], 60, 60, 100, 100)
        set_cell_margins(row.cells[1], 60, 60, 100, 100)
        p0 = row.cells[0].paragraphs[0]
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(71, 85, 105)
        p1 = row.cells[1].paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph()

    # Mandatory Disclaimer
    add_callout(
        doc,
        "This tool provides an AI-based preliminary screening only. It does not replace official government verification, KYC checks, or human review. Do not use as a sole legal determination.",
        title="MANDATORY REGULATORY DISCLAIMER",
        border_color="DC2626",
        bg_color="FEF2F2"
    )

    doc.add_paragraph()

    # 1. Abstract
    h1 = doc.add_heading(level=1)
    h1.add_run("1. Abstract")
    doc.add_paragraph(
        "Digital identity verification is a foundational pillar of modern banking, e-governance, and telecom onboarding. However, the proliferation of accessible graphic editing software has made identity document manipulation—such as altering birth dates, names, and photograph cutouts—alarmingly simple. This project presents the 'AI Fake Identity & Document Screening System', a lightweight, mobile-responsive web platform designed for authorized verifiers. The system acts as a rapid, preliminary forensic triage filter that evaluates uploaded identity documents across physical image acquisition quality, digital re-compression physics (Error Level Analysis), sensor noise consistency, facial biometrics, and official mathematical checksums (including the Dihedral Group D5 Verhoeff algorithm for Aadhaar and ICAO Doc 9303 for Passports). Rather than making legally binding judgments, the system outputs an objective Risk Score (0–100) and structured recommendations ('Verify manually' vs 'Proceed for further verification')."
    )

    # 2. Problem Statement
    h1 = doc.add_heading(level=1)
    h1.add_run("2. Problem Statement & Motivation")
    doc.add_paragraph(
        "In current KYC (Know Your Customer) workflows, organizations face three severe challenges:\n"
        "1. Human Visual Fatigue: Human verifiers reviewing hundreds of scans per day cannot detect micro-level font discrepancies, subtle cloning patches, or slight compression discontinuities.\n"
        "2. Expensive Direct Government APIs: Pinging official government databases (e.g., NSDL, UIDAI) incurs financial charges per query and requires active user consent, making exhaustive pre-screening cost-prohibitive.\n"
        "3. Syndicated Document Recycling: Fraud syndicates repeatedly submit identical stolen or altered documents with minor borders to bypass basic checks.\n"
        "There is an acute need for a fast, automated, cost-free preliminary screening system that immediately detects tampered or forged submissions before they reach downstream verification pipelines."
    )

    # 3. Objectives & Scope
    h1 = doc.add_heading(level=1)
    h1.add_run("3. Project Objectives & Scope")
    doc.add_paragraph("The primary objectives of this project are:")
    objs = [
        "Develop an extremely simple, mobile-friendly interface requiring zero training: Select document -> Upload scan -> View simple risk report.",
        "Implement non-destructive digital image forensics including Error Level Analysis (ELA at 90% JPEG quality) and sensor noise variance disparity.",
        "Build a robust quality assessment module to flag focus blurriness (Laplacian variance), specular flash glare clusters (>252 lux), and harsh 4x4 spatial shadows.",
        "Formulate and encode official mathematical syntax validators: Verhoeff algorithm (Aadhaar), Income Tax entity codes (PAN), Sarathi transport codes (DL), EPIC syntax (Voter ID), and ICAO Doc 9303 checksums (Passport).",
        "Enforce strict Privacy by Design: Automated client-side masking of sensitive identity numbers and addresses with a 1-click permanent file purge API."
    ]
    for o in objs:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(o)

    doc.add_paragraph("Scope Constraint: In Version 1.0, the application strictly accepts only 5 authorized Indian identity documents: Aadhaar Card, PAN Card, Driving Licence, Voter ID Card, and Passport.")

    # 4. Existing System vs Proposed System
    h1 = doc.add_heading(level=1)
    h1.add_run("4. Existing Systems vs. Proposed System")
    table_comp = doc.add_table(rows=5, cols=3)
    table_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_comp.columns[0].width = Inches(1.8)
    table_comp.columns[1].width = Inches(2.3)
    table_comp.columns[2].width = Inches(2.4)
    comp_headers = ["Evaluation Metric", "Conventional KYC / Manual", "Proposed AI Screening System"]
    for i, h in enumerate(comp_headers):
        cell = table_comp.cell(0, i)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)
    comp_rows = [
        ("Tamper Detection", "Visual human inspection; easily misses pixel-level ELA splicing.", "Multi-pillar ELA + localized sensor noise variance analysis."),
        ("Aadhaar Checksum", "Checks 12 digits; unable to verify Verhoeff parity manually.", "Exact mathematical Dihedral D5 Verhoeff checksum algorithm."),
        ("Verification Cost", "Requires billable API calls or manual human hours.", "100% free, local CPU processing; zero API charges."),
        ("Duplicate Detection", "Difficult to detect across large visual archives.", "Cryptographic SHA-256 + 64-bit dHash perceptual hashing.")
    ]
    for r_idx, (c1, c2, c3) in enumerate(comp_rows, start=1):
        row = table_comp.rows[r_idx]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate([c1, c2, c3]):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(9)
            if c_idx == 0:
                run.bold = True

    doc.add_paragraph()

    # 5. System Architecture & Diagram
    h1 = doc.add_heading(level=1)
    h1.add_run("5. System Architecture & Diagram")
    doc.add_paragraph(
        "The system follows a modern multi-tier decoupled architecture comprising the Presentation Layer, FastAPI Asynchronous Gateway, Multi-Pillar Forensic Engine, Mathematical Syntax Layer, and SQLite Audit Store:"
    )
    if DIAGRAM_PATH.exists():
        doc.add_picture(str(DIAGRAM_PATH), width=Inches(6.5))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc = cap.add_run("Figure 1: End-to-End System Architecture of AI Fake Identity & Document Screening System")
        rc.font.size = Pt(9)
        rc.font.italic = True
        rc.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph()

    # 6. Hardware & Software Requirements
    h1 = doc.add_heading(level=1)
    h1.add_run("6. Hardware & Software Requirements")
    doc.add_paragraph("Software Requirements:")
    sw = [
        "Operating System: Windows 10/11, Linux (Ubuntu 20.04+), or macOS",
        "Runtime Environment: Python 3.10 or higher",
        "Web Framework: FastAPI 0.110+ with Uvicorn ASGI Server",
        "Computer Vision & Forensics: OpenCV (opencv-python-headless 4.9+), Pillow 10.2+, NumPy",
        "Frontend: HTML5/CSS3/JavaScript (Production static build) + React 18 / Tailwind CSS",
        "Database: SQLite 3 with index-optimized tables"
    ]
    for s in sw:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(s)

    doc.add_paragraph("Hardware Requirements:")
    hw = [
        "Processor: Dual-core Intel Core i3 / AMD Ryzen 3 or higher (runs entirely on CPU)",
        "RAM: 4 GB minimum (8 GB recommended for concurrent multi-page PDF processing)",
        "Disk Space: 500 MB free storage for dependencies and local temporary cache"
    ]
    for h in hw:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(h)

    # 7. Expected Outcomes & Project Deliverables
    h1 = doc.add_heading(level=1)
    h1.add_run("7. Expected Outcomes & Deliverables")
    outs = [
        "Fully functional responsive web application accessible on desktop and mobile browsers.",
        "Accurate risk scoring (0-100) and color-coded risk assessment for all 5 document types.",
        "Interactive Error Level Analysis (ELA) heatmap viewer allowing verifiers to visually see tampering spikes.",
        "Comprehensive screening audit history panel with immediate file purge capability.",
        "Ready-to-run 1-click startup script (run.py) requiring zero manual environment configuration."
    ]
    for o in outs:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(o)

    synopsis_path = OUT_DIR / "Project_Synopsis.docx"
    doc.save(str(synopsis_path))
    print("Saved Synopsis to:", synopsis_path)
    return synopsis_path

# ==============================================================================
# DOCUMENT 3: Viva Preparation & Technical Architecture Guide
# ==============================================================================
def create_viva_guide_doc():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = title_p.add_run("VIVA-VOCE PREPARATION & ARCHITECTURE GUIDE")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(20)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(37, 99, 235)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = sub_p.add_run("Top 25 Examiner Questions, Mathematical Formulations, Code Walkthroughs & Demo Scripts")
    r_s.font.size = Pt(12)
    r_s.font.bold = True
    r_s.font.color.rgb = RGBColor(71, 85, 105)

    add_callout(
        doc,
        "This guide is specifically formulated for your college project viva, external examiner evaluation, and technical defense. Review the mathematical derivations and examiner questions carefully before presenting.",
        title="EXAMINER EVALUATION CHEAT SHEET",
        border_color="059669",
        bg_color="ECFDF5"
    )

    doc.add_paragraph()

    # Section 1: Mathematical Derivations & Algorithmic Foundations
    h1 = doc.add_heading(level=1)
    h1.add_run("1. Mathematical Formulations & Algorithms")

    doc.add_paragraph("A. Aadhaar Verhoeff Checksum Algorithm (Dihedral Group D5):")
    doc.add_paragraph(
        "Unlike standard Modulo-10 or Luhn algorithms, the Verhoeff algorithm uses non-commutative dihedral group D5 matrix operations (symmetries of a regular pentagon) paired with a permutation table p. The calculation iterates over the reversed digits:"
    )
    add_code_block(doc, """c = 0
for i, digit in enumerate(reversed_digits):
    c = d_table[c][p_table[i % 8][digit]]
# A valid Aadhaar number strictly satisfies: c == 0""")
    doc.add_paragraph(
        "Why D5? Standard Luhn algorithm misses 100% of transpositions of consecutive digits differing by 9 (e.g., 09 <-> 90). The Verhoeff algorithm catches 100% of all single-digit transcription errors and 100% of all adjacent transposition errors."
    )

    doc.add_paragraph("B. Laplacian Focus / Sharpness Measure:")
    doc.add_paragraph(
        "The discrete Laplacian operator approximates the second spatial derivative of the grayscale image I(x, y):"
    )
    add_code_block(doc, """L(x, y) = d2I/dx2 + d2I/dy2
Laplacian Variance = (1 / (N - 1)) * sum((L(x, y) - mean_L)^2)""")
    doc.add_paragraph(
        "High variance indicates sharp, high-frequency edge transitions. When an image is out-of-focus or blurred, high-frequency details are smoothed away, causing the variance to drop sharply below 50.0."
    )

    doc.add_paragraph("C. Error Level Analysis (ELA) Physics:")
    doc.add_paragraph(
        "JPEG uses lossy 8x8 discrete cosine transform (DCT) quantization. When an image is re-saved at a known quality level Q = 90%:"
    )
    add_code_block(doc, """Delta(x, y) = |Original(x, y) - Recompressed_Q90(x, y)|
Enhanced_ELA(x, y) = min(255, Delta(x, y) * 20.0)""")
    doc.add_paragraph(
        "Unmodified regions that have been compressed repeatedly reach an error equilibrium (low Delta). A digitally pasted patch (saved from a different source or modified with a paint tool) exhibits an abnormally high Delta, appearing as bright glowing anomalies in the ELA visualization."
    )

    # Section 2: Top 25 Examiner Viva Questions & Model Answers
    h1 = doc.add_heading(level=1)
    h1.add_run("2. Top 25 Examiner Viva Questions & Model Answers")

    viva_qa = [
        ("Q1: What is the primary objective of your minor project?",
         "The objective is to provide an automated, preliminary forensic triage system for authorized verifiers to screen identity documents for digital splicing, blur, glare, and mathematical checksum violations before expensive manual review or paid government API queries."),
        
        ("Q2: Why not just use official UIDAI or NSDL APIs directly for all documents?",
         "Direct government APIs have cost per transaction, require user OTP consent, and do not inspect whether an uploaded image was digitally tampered or blurry. Our system acts as an instant, zero-cost preliminary filter."),
         
        ("Q3: What documents does Version 1.0 support?",
         "Strictly 5 Indian identity documents: Aadhaar Card, PAN Card, Driving Licence, Voter ID Card, and Passport. Other documents are rejected."),

        ("Q4: How does Error Level Analysis (ELA) work in your project?",
         "We save the image in-memory at 90% JPEG quality, compute the absolute pixel difference with the original, amplify it 20x, and measure localized 8x8 patch variance. Spliced areas exhibit a disparity ratio > 4.5x over background."),

        ("Q5: How do you detect if a document was blurry or captured poorly?",
         "We compute the Laplacian variance over the grayscale image. Values below 50 indicate severe blur; values below 100 indicate moderate blur."),

        ("Q6: How do you detect camera flash glare?",
         "We perform connected-component labeling on pixels exceeding 252 intensity. Compact clusters larger than 1,200 pixels indicate specular flash washout obscuring document text."),

        ("Q7: How do you verify an Aadhaar number mathematically?",
         "We implement the Dihedral Group D5 Verhoeff checksum algorithm. The 12th digit is calculated from the first 11 digits using multiplication and permutation tables. Random fake numbers fail with over 99% probability."),

        ("Q8: How do you validate a PAN Card?",
         "We check the 10-character alphanumeric syntax [A-Z]{5}[0-9]{4}[A-Z] and validate the 4th character against official Income Tax entity types (P for Individual, C for Company, H for HUF, F for Firm, etc.)."),

        ("Q9: What check is performed on Passports?",
         "We validate the 1-letter + 7-digit format and execute weighted modulo-10 checksum validation (weights 7, 3, 1) on the 2-line ICAO Doc 9303 Machine Readable Zone (MRZ)."),

        ("Q10: How do you verify Driving Licences?",
         "We enforce the Sarathi format (2-letter state code + 2-digit RTO + 4-digit year + 7-digit serial) and check against all 36 Indian State and Union Territory prefixes."),

        ("Q11: How do you verify Voter IDs (EPIC)?",
         "We validate the standard Election Commission format of 3 uppercase alphabetic prefix characters followed by 7 numeric digits."),

        ("Q12: How does the system detect duplicate or reused documents?",
         "Using two-tier hashing: SHA-256 for identical files and 64-bit difference hash (dHash) for near-duplicate resized scans with Hamming distance <= 4."),

        ("Q13: How does face detection work on documents?",
         "We use OpenCV Haar Cascade frontal face detection to confirm a portrait photo is present, flag missing photos, and analyze boundary edge gradient density to detect photo replacement seams."),

        ("Q14: How is OCR performed?",
         "Using an automated multi-engine pipeline: Windows Native Media OCR with CLAHE contrast enhancement, deskewing, and regex pattern parsing."),

        ("Q15: How does the optional cross-check feature work?",
         "If the verifier optionally provides Name, DOB, or Doc Number, we perform fuzzy Levenshtein similarity (>=80% match), date format normalization, and alphanumeric equality checks."),

        ("Q16: How is the final Risk Score (0-100) calculated?",
         "It starts from a baseline of 5 and adds weighted severity penalties: High severity issues (+24 to +35), Medium severity issues (+15), and Low severity issues (+6), clamped between 0 and 100."),

        ("Q17: What are the three Risk Levels?",
         "Low Risk (0-35, Green -> 'Proceed for further verification'), Medium Risk (36-69, Yellow -> 'Verify manually'), and High Risk (70-100, Red -> 'Verify manually: High probability of tampering')."),

        ("Q18: What privacy measures are implemented?",
         "Automated preview masking of Aadhaar (XXXX-XXXX-1234) and PAN (ABCDE****F), address redaction, authorized unmasking toggle, and a permanent 1-click file purge API."),

        ("Q19: How does the file purge API work?",
         "DELETE /api/screening/{id} unlinks the uploaded scan and ELA heatmap from disk and marks the database record as purged, ensuring GDPR/DPDP data minimization."),

        ("Q20: What database is used?",
         "SQLite 3 with indexes on file_hash, perceptual_hash, and created_at. It requires zero external database server setup while maintaining full ACID compliance."),

        ("Q21: What is the backend technology stack?",
         "Python 3.10+, FastAPI (asynchronous ASGI framework), Uvicorn, Pydantic, OpenCV, Pillow, and NumPy."),

        ("Q22: What is the frontend technology stack?",
         "Two options: 1. A standalone zero-build production client served directly by FastAPI; 2. A modular React 18 + Tailwind CSS + Lucide Icons client."),

        ("Q23: How do you test the application without personal ID cards?",
         "We generated 4 realistic pre-loaded test samples accessible with 1-click buttons in the UI: Clean Aadhaar (Genuine), Tampered PAN (Spliced), Blurry DL (Quality Defect), and Fake Passport (Corrupt MRZ)."),

        ("Q24: What is the role of the disclaimer banner?",
         "To maintain strict legal clarity: 'This tool provides an AI-based preliminary screening only. It does not replace official government verification, KYC checks, or human review.'"),

        ("Q25: What are future enhancements for this project?",
         "Integrating official DigiLocker OAuth bridges for Low Risk documents, multi-spectral flash reflection for hologram verification, and packaging the models into an Android/iOS camera SDK.")
    ]

    for q, a in viva_qa:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        rq = p.add_run(q)
        rq.bold = True
        rq.font.color.rgb = RGBColor(30, 58, 138)
        
        pa = doc.add_paragraph()
        pa.paragraph_format.space_after = Pt(6)
        ra = pa.add_run(f"Answer: {a}")
        ra.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph()

    # Section 3: Live Software Demo Script
    h1 = doc.add_heading(level=1)
    h1.add_run("3. Live Demonstration Script for Examiners")
    doc.add_paragraph(
        "Follow this structured sequence when demonstrating the application to your project guide or external examiner:"
    )
    demo_steps = [
        ("Step 1: Open Application", "Show the clean main screen at http://localhost:3000 (or http://127.0.0.1:8000). Highlight the zero-clutter layout, large upload dropzone, and strict 5-document dropdown."),
        ("Step 2: Demonstrate Clean Aadhaar", "Click the 1-click sample button 'Aadhaar Card (Genuine)'. Explain that the animated radar scanner is computing Laplacian blur and running the Verhoeff dihedral D5 checksum. Point out the resulting Green 'Low Risk (Score: ~20)' badge and masked number XXXX-XXXX-3723."),
        ("Step 3: Demonstrate Tampered PAN Card", "Click 'PAN Card (Tampered)'. Show that the system flags High Risk (Score: ~78). Switch to the 'ELA Tamper Heatmap' tab to show the examiner the bright spliced glowing patch over the altered Date of Birth."),
        ("Step 4: Demonstrate Blur & Glare Defect", "Click 'Driving Licence (Blurry / Glare)'. Show how physical capture defects are isolated from digital forgeries, advising the verifier to request a clearer photo."),
        ("Step 5: Demonstrate Privacy Purge", "Click 'Delete Document & Purge Scan'. Confirm the dialog and show that the file and ELA artifacts are permanently purged from server disk for privacy compliance.")
    ]
    for step_title, step_desc in demo_steps:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{step_title}: ")
        r_b.bold = True
        p.add_run(step_desc)

    guide_path = OUT_DIR / "Viva_Preparation_and_Architecture_Guide.docx"
    doc.save(str(guide_path))
    print("Saved Viva Guide to:", guide_path)
    return guide_path

if __name__ == "__main__":
    create_synopsis_doc()
    create_viva_guide_doc()
