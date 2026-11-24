# Sample Documents for Demonstration & Testing

This folder contains **10 realistic mock identity documents** (**two for each of the 5 authorized categories**) specifically crafted to demonstrate both **authentic document passes** and **AI tampering/fraud detection algorithms**.

---

## 📁 Folder Structure

```
demo_samples/
├── 1_Aadhaar_Card/
│   ├── 1_Aadhaar_Authentic.png          # Passes Verhoeff checksum & UIDAI layout
│   └── 2_Aadhaar_Tampered.png           # Fails Verhoeff checksum + spliced number
├── 2_PAN_Card/
│   ├── 1_PAN_Authentic.png              # Valid entity code 'P' & Income Tax layout
│   └── 2_PAN_Tampered.png               # Invalid entity code 'X' + altered DOB patch
├── 3_Driving_Licence/
│   ├── 1_Driving_Licence_Authentic.png  # Valid Sarathi RTO format & clear portrait
│   └── 2_Driving_Licence_Blurry.png     # Heavy Gaussian blur & specular flash glare
├── 4_Voter_ID_Card/
│   ├── 1_Voter_ID_Authentic.png         # Standard ECI EPIC format (3 letters + 7 digits)
│   └── 2_Voter_ID_Tampered.png          # Irregular EPIC code + missing ECI headers
└── 5_Passport/
    ├── 1_Passport_Authentic.png         # Valid ICAO Doc 9303 MRZ checksums & portrait
    └── 2_Passport_Corrupt_MRZ.png       # Corrupt MRZ checksum + missing photo box
```

---

## 🎯 Demonstration Guide (What Each Sample Tests)

| Category | Sample File | Status | Expected Risk | What the AI Tests & Detects |
| :--- | :--- | :--- | :--- | :--- |
| **1. Aadhaar Card** | `1_Aadhaar_Authentic.png` | **Authentic** | **Low** | Valid 12-digit number (`5482 9104 3723`) satisfying Dihedral group $D_5$ Verhoeff checksum, scannable QR pattern, portrait frame, UIDAI headers. |
| | `2_Aadhaar_Tampered.png` | **Fraud** | **High** | Fails mathematical Verhoeff check (`...3729`), spliced number box detected by Error Level Analysis (ELA). |
| **2. PAN Card** | `1_PAN_Authentic.png` | **Authentic** | **Low** | Valid PAN syntax (`ABCPS2345F`), 4th char `P` = Individual, 5th char `S` = Sharma, Father's Name, DOB, signature band. |
| | `2_PAN_Tampered.png` | **Fraud** | **High** | Invalid entity code `ABCXE9874F` (4th char `X` is non-existent), digital copy-paste splice over DOB with high ELA compression noise. |
| **3. Driving Licence** | `1_Driving_Licence_Authentic.png` | **Authentic** | **Low** | Valid Sarathi format (`DL04 2021 0012345`), recognized State RTO code (`DL`), high Laplacian focus sharpness ($>200$), valid classes (`LMV, MCWG`). |
| | `2_Driving_Licence_Blurry.png` | **Defect** | **Medium / High** | Severe camera defocus blur (Laplacian variance $<30$), specular flash glare hotspot ($>252$ brightness), unreadable text. |
| **4. Voter ID Card** | `1_Voter_ID_Authentic.png` | **Authentic** | **Low** | Standard Election Commission EPIC format (`WBF2345678`: 3 uppercase letters + 7 digits), ECI seal, Elector's name, age, gender. |
| | `2_Voter_ID_Tampered.png` | **Fraud** | **High** | Malformed EPIC syntax (`VTR9874X2`), missing English ECI official header, spliced photo frame seam. |
| **5. Passport** | `1_Passport_Authentic.png` | **Authentic** | **Low** | Valid Indian Passport format (`A2094851`), Type P, Code IND, 2-line ICAO Doc 9303 MRZ with verified 7-3-1 weighted checksums, portrait detected. |
| | `2_Passport_Corrupt_MRZ.png` | **Fraud** | **High** | Missing portrait photo (`[Photo Missing]`), corrupted MRZ check digit failing ICAO Doc 9303 mathematical verification. |

---

## 💡 How to Demonstrate

### Method 1: 1-Click Interactive Demo (Fastest)
1. Open the web interface at **`http://localhost:8000`** (or access from your smartphone via the local IP).
2. Scroll to the **"Quick Test Cases (1-Click Demo)"** section at the bottom of the scanner page.
3. Click any of the **10 test cards** to run an immediate end-to-end analysis without needing to upload files manually!

### Method 2: Drag & Drop / File Upload
1. Open the web interface.
2. Select the document category from the dropdown (e.g. *Aadhaar Card*, *PAN Card*, etc.).
3. Drag and drop any image from the `demo_samples/` folder into the upload zone.
4. (Optional) Enter cross-check fields to demonstrate identity verification matching.
5. Click **"Verify Document"** to view forensic tampering heatmaps, extracted fields, and audit score!
