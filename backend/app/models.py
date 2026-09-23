# ============================================================
# SixthScreen — Database Models (SQLAlchemy)
# ============================================================
# This file defines Python representations of database tables.
# Each class = one table. Work with Python objects instead of SQL.
# ============================================================

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float,
    DateTime, Date, ARRAY, DECIMAL, ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# ── USERS ──
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships — a user can have many quiz sessions and watch history entries
    quiz_sessions = relationship("QuizSession", back_populates="user")
    watch_history = relationship("WatchHistory", back_populates="user")


# ── QUESTIONS ──
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)  # 'movie', 'subconscious', 'abstract'

    option_a_text = Column(Text, nullable=False)
    option_a_vector = Column(ARRAY(DECIMAL), nullable=False)  # [energy, darkness, intellect, emotion, adventure, social]

    option_b_text = Column(Text, nullable=False)
    option_b_vector = Column(ARRAY(DECIMAL), nullable=False)

    option_c_text = Column(Text, nullable=False)
    option_c_vector = Column(ARRAY(DECIMAL), nullable=False)

    option_d_text = Column(Text, nullable=False)
    option_d_vector = Column(ARRAY(DECIMAL), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


# ── QUIZ SESSIONS ──
class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    mood_vector = Column(ARRAY(DECIMAL), nullable=True)
    question_count = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="quiz_sessions")
    answers = relationship("QuizAnswer", back_populates="session")
    recommendations = relationship("Recommendation", back_populates="session")


# ── QUIZ ANSWERS ──
class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("quiz_sessions.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    selected_option = Column(String(1), nullable=False)  # 'a', 'b', 'c', 'd'
    answer_vector = Column(ARRAY(DECIMAL), nullable=False)
    answered_at = Column(DateTime, server_default=func.now())

    # Relationships
    session = relationship("QuizSession", back_populates="answers")
    question = relationship("Question")


# ── MOVIE/TV SHOW CACHE ──
class MovieCache(Base):
    __tablename__ = "movies_cache"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    original_title = Column(String(500))
    overview = Column(Text)
    poster_path = Column(String(300))
    backdrop_path = Column(String(300))
    genres = Column(ARRAY(Text))
    mood_vector = Column(ARRAY(DECIMAL), nullable=False)
    tmdb_rating = Column(DECIMAL(4, 2), default=0)
    vote_count = Column(Integer, default=0)
    release_date = Column(Date)
    media_type = Column(String(10), default="movie")  # 'movie' or 'tv'
    popularity = Column(DECIMAL(10, 3), default=0)
    cached_at = Column(DateTime, server_default=func.now())


# ── RECOMMENDATIONS ──
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("quiz_sessions.id", ondelete="CASCADE"))
    movie_id = Column(Integer, ForeignKey("movies_cache.id"))
    match_score = Column(DECIMAL(5, 2), nullable=False)
    quality_score = Column(DECIMAL(5, 2), nullable=False)
    final_score = Column(DECIMAL(5, 2), nullable=False)
    rank_position = Column(Integer, nullable=False)
    explanation = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    session = relationship("QuizSession", back_populates="recommendations")
    movie = relationship("MovieCache")


# ── WATCH HISTORY ──
class WatchHistory(Base):
    __tablename__ = "watch_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    movie_id = Column(Integer, ForeignKey("movies_cache.id"))
    user_rating = Column(Integer)
    watched = Column(Boolean, default=False)
    watchlist = Column(Boolean, default=True)
    added_at = Column(DateTime, server_default=func.now())
    watched_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="watch_history")
    movie = relationship("MovieCache")

    __table_args__ = (UniqueConstraint("user_id", "movie_id"),)


# ── GENRE → MOOD VECTOR MAP ──
class GenreMoodMap(Base):
    __tablename__ = "genre_mood_map"

    id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String(50), unique=True, nullable=False)
    tmdb_genre_id = Column(Integer, unique=True)
    mood_vector = Column(ARRAY(DECIMAL), nullable=False)
