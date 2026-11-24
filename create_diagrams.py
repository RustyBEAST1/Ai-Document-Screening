import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

OUT_DIR = Path("C:/Users/user/AG01")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    # Colors
    c_blue = "#2563EB"
    c_blue_light = "#EFF6FF"
    c_slate = "#1E293B"
    c_slate_light = "#F1F5F9"
    c_emerald = "#059669"
    c_emerald_light = "#ECFDF5"
    c_amber = "#D97706"
    c_amber_light = "#FFFBEB"
    c_purple = "#7C3AED"
    c_purple_light = "#F5F3FF"

    # Title
    ax.text(7, 8.1, "AI Fake Identity & Document Screening System - Architecture", 
            fontsize=16, fontweight="bold", ha="center", color=c_slate)
    ax.text(7, 7.75, "End-to-End Pipeline: Presentation -> API Gateway -> Forensics -> OCR & Checksums -> Risk Engine", 
            fontsize=10, ha="center", color="#64748B")

    # Layer 1: Client Layer
    box_client = patches.FancyBboxPatch((0.5, 5.0), 3.0, 2.2, boxstyle="round,pad=0.2", 
                                        ec=c_blue, fc=c_blue_light, lw=1.8)
    ax.add_patch(box_client)
    ax.text(2.0, 6.9, "1. Client Layer", fontsize=11, fontweight="bold", color=c_blue, ha="center")
    ax.text(2.0, 6.5, "- React + Tailwind UI (Vite)\n- Mobile Responsive Web Client\n- 1-Click Upload & Camera\n- 5-Document Strict Dropdown\n- Real-time Radar Scan UI", 
            fontsize=8.5, color=c_slate, ha="center", va="top")

    # Arrow 1 -> 2
    ax.annotate("", xy=(4.1, 6.1), xytext=(3.5, 6.1),
                arrowprops=dict(arrowstyle="->", color=c_blue, lw=2))

    # Layer 2: API Gateway
    box_api = patches.FancyBboxPatch((4.2, 5.0), 2.8, 2.2, boxstyle="round,pad=0.2", 
                                     ec=c_purple, fc=c_purple_light, lw=1.8)
    ax.add_patch(box_api)
    ax.text(5.6, 6.9, "2. API Gateway (FastAPI)", fontsize=11, fontweight="bold", color=c_purple, ha="center")
    ax.text(5.6, 6.5, "- POST /api/screen\n- POST /api/screen-sample\n- File Size & Type Filter\n- UUID Path Sanitization\n- Privacy Auto-Masking\n- DELETE /api/screening (Purge)", 
            fontsize=8.5, color=c_slate, ha="center", va="top")

    # Arrow 2 -> 3
    ax.annotate("", xy=(7.6, 6.1), xytext=(7.0, 6.1),
                arrowprops=dict(arrowstyle="->", color=c_purple, lw=2))

    # Layer 3: Forensic & Computer Vision Engine
    box_forensic = patches.FancyBboxPatch((7.7, 4.5), 5.8, 2.7, boxstyle="round,pad=0.2", 
                                          ec=c_amber, fc=c_amber_light, lw=1.8)
    ax.add_patch(box_forensic)
    ax.text(10.6, 7.0, "3. Multi-Pillar Forensic Engine", fontsize=11, fontweight="bold", color=c_amber, ha="center")
    
    # Sub-boxes inside Forensics
    f_items = [
        ("Image Quality", "Laplacian Blur (<50/100)\nSpecular Glare (>252 lux)\n4x4 Quadrant Shadows\nAspect Ratio & Border"),
        ("Tampering & ELA", "Error Level Analysis 90%\nPatch Variance Disparity\nSensor Noise Disparity\nClone / Smudge Marks"),
        ("Face Biometrics", "Haar Cascade Frontal Face\nPhoto Presence Verify\nPhoto Seam Gradient\nMissing Photo Check"),
        ("Duplicate Hashing", "SHA-256 Exact Duplicate\n64-bit dHash Perceptual\nHamming Distance <= 4\nRecycled ID Syndicate")
    ]
    for idx, (ftitle, fdesc) in enumerate(f_items):
        fx = 8.0 + (idx % 2) * 2.7
        fy = 5.85 - (idx // 2) * 1.15
        sbox = patches.FancyBboxPatch((fx, fy - 0.75), 2.5, 0.75, boxstyle="round,pad=0.1", 
                                      ec="#CBD5E1", fc="#FFFFFF", lw=1)
        ax.add_patch(sbox)
        ax.text(fx + 1.25, fy - 0.15, ftitle, fontsize=8.5, fontweight="bold", color=c_slate, ha="center")
        ax.text(fx + 1.25, fy - 0.45, fdesc, fontsize=6.5, color="#475569", ha="center")

    # Arrow from Forensics down to Validation
    ax.annotate("", xy=(10.6, 3.7), xytext=(10.6, 4.45),
                arrowprops=dict(arrowstyle="->", color=c_amber, lw=2))

    # Layer 4: OCR & Mathematical Checksums
    box_ocr = patches.FancyBboxPatch((0.5, 1.2), 6.5, 2.8, boxstyle="round,pad=0.2", 
                                     ec=c_emerald, fc=c_emerald_light, lw=1.8)
    ax.add_patch(box_ocr)
    ax.text(3.75, 3.75, "4. OCR & Mathematical Syntax Validation Layer", fontsize=11, fontweight="bold", color=c_emerald, ha="center")
    
    ocr_items = [
        ("Aadhaar Checksum", "Dihedral D5 Verhoeff Matrix\n12-digit UIDAI sequence\nSecure QR Code Scanner"),
        ("PAN Card Syntax", "5 Letters + 4 Digits + 1 Letter\n4th Char Entity (P, C, H, etc.)\nITD Official Headers"),
        ("Driving Licence", "Sarathi Standard Format\n36 State/UT Code Checks\nTransport Ministry Keywords"),
        ("Voter ID & Passport", "ECI EPIC 3-letter + 7-digit\nPassport 1-letter + 7-digit\nICAO 9303 7-3-1 MRZ Check")
    ]
    for idx, (otitle, odesc) in enumerate(ocr_items):
        ox = 0.8 + (idx % 2) * 3.1
        oy = 2.8 - (idx // 2) * 1.15
        sbox = patches.FancyBboxPatch((ox, oy - 0.8), 2.9, 0.8, boxstyle="round,pad=0.1", 
                                      ec="#CBD5E1", fc="#FFFFFF", lw=1)
        ax.add_patch(sbox)
        ax.text(ox + 1.45, oy - 0.15, otitle, fontsize=8.5, fontweight="bold", color=c_slate, ha="center")
        ax.text(ox + 1.45, oy - 0.45, odesc, fontsize=6.8, color="#475569", ha="center")

    # Arrow from OCR to Risk Engine
    ax.annotate("", xy=(7.7, 2.5), xytext=(7.0, 2.5),
                arrowprops=dict(arrowstyle="->", color=c_emerald, lw=2))

    # Layer 5: Unified Risk Engine & Storage
    box_risk = patches.FancyBboxPatch((7.7, 1.2), 5.8, 2.8, boxstyle="round,pad=0.2", 
                                      ec=c_blue, fc="#FFFFFF", lw=1.8)
    ax.add_patch(box_risk)
    ax.text(10.6, 3.75, "5. Unified Risk Scoring & Audit Storage", fontsize=11, fontweight="bold", color=c_blue, ha="center")
    
    # Risk Score Badges
    b_low = patches.FancyBboxPatch((8.0, 2.3), 1.6, 0.9, boxstyle="round,pad=0.1", ec="#A7F3D0", fc="#ECFDF5", lw=1)
    b_med = patches.FancyBboxPatch((9.8, 2.3), 1.6, 0.9, boxstyle="round,pad=0.1", ec="#FDE68A", fc="#FFFBEB", lw=1)
    b_high = patches.FancyBboxPatch((11.6, 2.3), 1.6, 0.9, boxstyle="round,pad=0.1", ec="#FECACA", fc="#FEF2F2", lw=1)
    ax.add_patch(b_low)
    ax.add_patch(b_med)
    ax.add_patch(b_high)
    
    ax.text(8.8, 2.95, "LOW (0-35)", fontsize=7.5, fontweight="bold", color="#065F46", ha="center")
    ax.text(8.8, 2.6, "Proceed for\nverification", fontsize=6.5, color="#047857", ha="center")

    ax.text(10.6, 2.95, "MED (36-69)", fontsize=7.5, fontweight="bold", color="#92400E", ha="center")
    ax.text(10.6, 2.6, "Secondary check\nrecommended", fontsize=6.5, color="#B45309", ha="center")

    ax.text(12.4, 2.95, "HIGH (70-100)", fontsize=7.5, fontweight="bold", color="#991B1B", ha="center")
    ax.text(12.4, 2.6, "Verify manually\nCritical defect", fontsize=6.5, color="#B91C1C", ha="center")

    # DB line
    ax.text(10.6, 1.7, "SQLite Audit Store (screening.db) • Index on Hashes & CreatedAt\nPermanent Purge API (DELETE /api/screening/{id})", 
            fontsize=7.8, color="#475569", ha="center")

    plt.tight_layout()
    diagram_path = OUT_DIR / "system_architecture_diagram.png"
    plt.savefig(str(diagram_path), dpi=300)
    plt.close()
    print("Saved architecture diagram to:", diagram_path)
    return diagram_path

if __name__ == "__main__":
    generate_architecture_diagram()
