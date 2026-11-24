import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from .config import DB_PATH

def get_connection():
    ensure_db()
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

_initialized = False

def ensure_db():
    global _initialized
    if not _initialized:
        _initialized = True
        init_db()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS screenings (
            id TEXT PRIMARY KEY,
            document_type TEXT NOT NULL,
            filename TEXT NOT NULL,
            stored_filename TEXT,
            file_hash TEXT,
            perceptual_hash TEXT,
            risk_level TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            confidence INTEGER NOT NULL,
            short_message TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            issues_json TEXT NOT NULL,
            extracted_details_json TEXT NOT NULL,
            cross_checks_json TEXT,
            has_ela INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            is_deleted INTEGER DEFAULT 0
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_hash ON screenings(file_hash)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_perceptual_hash ON screenings(perceptual_hash)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON screenings(created_at)")
    conn.commit()
    conn.close()

def save_screening(record: Dict[str, Any]) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO screenings (
            id, document_type, filename, stored_filename, file_hash, perceptual_hash,
            risk_level, risk_score, confidence, short_message, recommendation,
            issues_json, extracted_details_json, cross_checks_json, has_ela,
            created_at, is_deleted
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["id"],
        record["document_type"],
        record["filename"],
        record.get("stored_filename"),
        record.get("file_hash"),
        record.get("perceptual_hash"),
        record["risk_level"],
        record["risk_score"],
        record["confidence"],
        record["short_message"],
        record["recommendation"],
        json.dumps(record.get("issues", [])),
        json.dumps(record.get("extracted_details", {})),
        json.dumps(record.get("cross_checks", {})),
        1 if record.get("has_ela") else 0,
        record.get("created_at", datetime.now().isoformat()),
        0
    ))
    conn.commit()
    conn.close()

def get_screening_by_id(screening_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM screenings WHERE id = ? AND is_deleted = 0", (screening_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_dict(row)

def list_screenings(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM screenings WHERE is_deleted = 0 ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (limit, offset)
    )
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_dict(row) for row in rows]

def mark_screening_deleted(screening_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE screenings SET is_deleted = 1 WHERE id = ?", (screening_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def find_duplicate_hashes(file_hash: str, perceptual_hash: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, document_type, filename, risk_level, risk_score, created_at, perceptual_hash
        FROM screenings 
        WHERE is_deleted = 0 AND (file_hash = ? OR perceptual_hash IS NOT NULL)
        ORDER BY created_at DESC LIMIT 10
    """, (file_hash,))
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_dict(row) for row in rows]

def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    d = dict(row)
    if "issues_json" in d:
        try:
            d["issues"] = json.loads(d.pop("issues_json") or "[]")
        except:
            d["issues"] = []
    if "extracted_details_json" in d:
        try:
            d["extracted_details"] = json.loads(d.pop("extracted_details_json") or "{}")
        except:
            d["extracted_details"] = {}
    if "cross_checks_json" in d:
        try:
            d["cross_checks"] = json.loads(d.pop("cross_checks_json") or "{}")
        except:
            d["cross_checks"] = {}
    return d
