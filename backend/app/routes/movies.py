# ============================================================
# SixthScreen — Movie Cache API Endpoints
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.tmdb_client import fetch_and_cache_movies
from app.schemas import MessageResponse

router = APIRouter(prefix="/api/movies", tags=["Movies"])


@router.post("/sync", response_model=MessageResponse)
def sync_movies(db: Session = Depends(get_db)):
    """
    Fetches popular movies/TV shows from TMDB and caches them in the database.

    Call this endpoint on first setup or periodically to refresh data.

    Usage:
        POST /api/movies/sync
        → { message: "120 movies/shows added", success: true }
    """
    added = fetch_and_cache_movies(db, pages=3)
    return MessageResponse(
        message=f"{added} new movies/shows added",
        success=True
    )
