# ============================================================
# SixthScreen — Pydantic Schemas (Request/Response)
# ============================================================
# Defines the input (request) and output (response) formats
# for the API.
#
# Pydantic: Data validation library. Automatically checks
# incoming data and returns error messages if invalid.
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── QUESTION ──

class QuestionOut(BaseModel):
    """Question shown to user. Vectors are HIDDEN."""
    id: int
    question_text: str
    question_type: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True


# ── QUIZ ──

class QuizStartResponse(BaseModel):
    """Response when a quiz is started."""
    session_id: int
    questions: list[QuestionOut]
    total_questions: int


class AnswerRequest(BaseModel):
    """Answer submitted by the user."""
    session_id: int
    question_id: int
    selected_option: str = Field(..., pattern="^[abcd]$")  # Only a, b, c, d


class QuizCompleteRequest(BaseModel):
    """Request to complete a quiz."""
    session_id: int


# ── MOVIE/TV SHOW ──

class MovieOut(BaseModel):
    """Movie/TV show info — shown to user."""
    tmdb_id: int
    title: str
    original_title: Optional[str] = None
    overview: Optional[str] = None
    poster_url: Optional[str] = None       # Full poster URL
    backdrop_url: Optional[str] = None
    genres: list[str] = []
    tmdb_rating: float = 0
    vote_count: int = 0
    release_date: Optional[str] = None
    media_type: str = "movie"


# ── RECOMMENDATION ──

class RecommendationOut(BaseModel):
    """Single recommendation — movie info + scores."""
    rank: int                               # 1-5 ranking
    movie: MovieOut
    match_score: float                      # Match score (0-10)
    quality_score: float                    # Global quality (0-10)
    final_score: float                      # Final score (0-10)
    explanation: Optional[str] = None       # "Why we recommend this"


class RecommendationResponse(BaseModel):
    """Quiz result — mood vector + 5 recommendations."""
    session_id: int
    mood_vector: list[float]                # [energy, darkness, intellect, emotion, adventure, social]
    mood_labels: dict[str, float]           # {"energy": 7.2, "darkness": 3.1, ...}
    recommendations: list[RecommendationOut]
    generated_at: datetime


# ── GENERAL ──

class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    success: bool = True
