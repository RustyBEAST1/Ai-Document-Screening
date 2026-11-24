import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import BASE_DIR, DISCLAIMER_TEXT
from .database import init_db
from .api.routes import router as api_router

app = FastAPI(
    title="AI Fake Identity & Document Screening System",
    description="Automated preliminary identity document forensic and tampering screening system.",
    version="1.0.0"
)

# Enable CORS for local dev and embedded clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints
app.include_router(api_router)

# Mount web directories
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"
STATIC_DIR = BASE_DIR.parent / "static"

if FRONTEND_DIST.exists() and (FRONTEND_DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")
    WEB_DIR = FRONTEND_DIST
elif STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    WEB_DIR = STATIC_DIR
else:
    WEB_DIR = None

if STATIC_DIR.exists() and WEB_DIR != STATIC_DIR:
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AI Fake Identity & Document Screening System",
        "version": "1.0.0"
    }

@app.get("/")
def serve_index():
    if WEB_DIR:
        index_file = WEB_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
    return {
        "message": "AI Fake Identity & Document Screening System API is active.",
        "docs_url": "/docs",
        "disclaimer": DISCLAIMER_TEXT
    }
