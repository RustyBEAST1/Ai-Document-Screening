import re
from typing import Dict, Any, List, Optional

def normalize_text(text: str) -> str:
    """Removes special characters, collapses whitespace, uppercase."""
    return re.sub(r"[^A-Z0-9]", "", str(text or "").upper())

def levenshtein_similarity(s1: str, s2: str) -> float:
    """Computes normalized Levenshtein similarity (0.0 to 1.0)."""
    s1, s2 = s1.upper().strip(), s2.upper().strip()
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    distance = dp[m][n]
    max_len = max(m, n)
    return 1.0 - (distance / max_len)

def perform_cross_checks(
    user_name: Optional[str],
    user_dob: Optional[str],
    user_number: Optional[str],
    extracted_name: Optional[str],
    extracted_dob: Optional[str],
    extracted_number: Optional[str],
    ocr_raw_text: str
) -> Dict[str, Any]:
    """
    Cross-checks verifier-provided details against extracted OCR and structured fields.
    """
    has_inputs = any([user_name, user_dob, user_number])
    if not has_inputs:
        return {
            "checked": False,
            "name_match": None,
            "name_score": None,
            "dob_match": None,
            "number_match": None,
            "notes": ["No optional cross-check details provided by user."],
            "issues": []
        }

    issues: List[Dict[str, Any]] = []
    notes: List[str] = []
    
    # 1. Name Check
    name_match = None
    name_score = None
    if user_name and user_name.strip():
        u_name = user_name.strip()
        # Compare against structured name if available
        scores = []
        if extracted_name:
            scores.append(int(levenshtein_similarity(u_name, extracted_name) * 100))
            
        # Also check against lines in OCR text
        for line in ocr_raw_text.splitlines():
            clean = line.strip()
            if len(clean) > 3 and any(c.isalpha() for c in clean):
                sim = int(levenshtein_similarity(u_name, clean) * 100)
                scores.append(sim)
                # Token check: if user tokens are contained
                u_tokens = set(u_name.upper().split())
                c_tokens = set(clean.upper().split())
                if u_tokens and u_tokens.issubset(c_tokens):
                    scores.append(95)
                    
        best_score = max(scores) if scores else 0
        name_score = best_score
        if best_score >= 80:
            name_match = True
            notes.append(f"Holder name verified with {best_score}% match confidence.")
        elif best_score >= 50:
            name_match = False
            notes.append(f"Name partial match ({best_score}%): Possible minor typo or middle name omission.")
            issues.append({
                "id": "cross_name_partial_mismatch",
                "severity": "medium",
                "category": "Cross-Check",
                "title": "Minor Name Discrepancy",
                "description": f"Provided name '{u_name}' partially matches extracted document text (match score: {best_score}%)."
            })
        else:
            name_match = False
            notes.append(f"Name mismatch: Provided '{u_name}' not found on document.")
            issues.append({
                "id": "cross_name_severe_mismatch",
                "severity": "high",
                "category": "Cross-Check",
                "title": "Document Name Mismatch",
                "description": f"The provided name '{u_name}' does not match the name printed on the document."
            })

    # 2. DOB Check
    dob_match = None
    if user_dob and user_dob.strip():
        u_dob_clean = re.sub(r"[^0-9]", "", user_dob.strip())
        doc_dob_clean = re.sub(r"[^0-9]", "", extracted_dob or "")
        
        # Check direct or substring in raw text
        if doc_dob_clean and (u_dob_clean in doc_dob_clean or doc_dob_clean in u_dob_clean):
            dob_match = True
            notes.append(f"Date of birth verified ({user_dob}).")
        elif u_dob_clean in re.sub(r"[^0-9]", "", ocr_raw_text):
            dob_match = True
            notes.append(f"Date of birth verified in document text ({user_dob}).")
        else:
            dob_match = False
            notes.append(f"Date of birth mismatch: Provided '{user_dob}' vs extracted '{extracted_dob or 'None'}'.")
            issues.append({
                "id": "cross_dob_mismatch",
                "severity": "high",
                "category": "Cross-Check",
                "title": "Date of Birth Mismatch",
                "description": f"The provided Date of Birth '{user_dob}' does not match the date printed on the document."
            })

    # 3. Document Number Check
    number_match = None
    if user_number and user_number.strip():
        u_num_norm = normalize_text(user_number)
        doc_num_norm = normalize_text(extracted_number or "")
        ocr_norm = normalize_text(ocr_raw_text)
        
        if doc_num_norm and (u_num_norm == doc_num_norm or u_num_norm in doc_num_norm or doc_num_norm in u_num_norm):
            number_match = True
            notes.append("Document identification number matched.")
        elif u_num_norm in ocr_norm:
            number_match = True
            notes.append("Document identification number located in document text.")
        else:
            number_match = False
            notes.append("Document identification number mismatch.")
            issues.append({
                "id": "cross_doc_number_mismatch",
                "severity": "high",
                "category": "Cross-Check",
                "title": "Document Number Mismatch",
                "description": f"The provided document number '{user_number}' does not match the extracted document number."
            })

    return {
        "checked": True,
        "name_match": name_match,
        "name_score": name_score,
        "dob_match": dob_match,
        "number_match": number_match,
        "notes": notes,
        "issues": issues
    }
