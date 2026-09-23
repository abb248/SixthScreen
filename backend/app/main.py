# ============================================================
# SixthScreen — Main Application (FastAPI)
# ============================================================
# This file starts the entire application.
# Run: uvicorn app.main:app --reload
# Swagger UI: http://localhost:8000/docs
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import quiz, movies
from app.config import settings

# ── Create the FastAPI application ──
app = FastAPI(
    title="SixthScreen API",
    description="What does your subconscious want to watch? Mood-based movie & TV show recommendations.",
    version="1.0.0",
    docs_url="/docs",           # Swagger UI address
    redoc_url="/redoc",         # ReDoc address
)

# ── CORS settings ──
# Required for frontend (Next.js) to communicate with backend.
# Browser security policy blocks requests from different ports/domains.
# CORS lifts this restriction.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Development: allow all. Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routes (endpoints) ──
app.include_router(quiz.router)
app.include_router(movies.router)


# ── Root endpoint ──
@app.get("/", tags=["Root"])
def root():
    """Check if the API is running."""
    return {
        "app": "SixthScreen",
        "status": "running ✅",
        "version": "1.0.0",
        "docs": "/docs",
        "description": "What does your subconscious want to watch?",
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check — for deployment monitoring."""
    return {"status": "healthy"}
