from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ScreeningIssue(BaseModel):
    id: str
    severity: str = Field(..., description="high, medium, low, or info")
    category: str = Field(..., description="Quality, Forensics, Format, Cross-Check, Integrity")
    title: str
    description: str

class ExtractedDetails(BaseModel):
    document_number_masked: Optional[str] = None
    full_name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    address_masked: Optional[str] = None
    format_valid: bool = False
    format_notes: str = ""
    qr_detected: bool = False
    mrz_detected: bool = False
    detected_keywords: List[str] = []

class CrossCheckResult(BaseModel):
    checked: bool = False
    name_match: Optional[bool] = None
    name_score: Optional[int] = None
    dob_match: Optional[bool] = None
    number_match: Optional[bool] = None
    notes: List[str] = []

class ScreeningResponse(BaseModel):
    id: str
    document_type: str
    filename: str
    risk_level: str
    risk_score: int
    confidence: int
    short_message: str
    recommendation: str
    issues: List[ScreeningIssue] = []
    extracted_details: ExtractedDetails
    cross_checks: CrossCheckResult
    has_ela: bool = False
    preview_url: Optional[str] = None
    ela_url: Optional[str] = None
    disclaimer: str
    created_at: str

class ScreeningSummary(BaseModel):
    id: str
    document_type: str
    filename: str
    risk_level: str
    risk_score: int
    confidence: int
    recommendation: str
    created_at: str

class SampleDocument(BaseModel):
    id: str
    title: str
    document_type: str
    description: str
    expected_risk: str
    filename: str
