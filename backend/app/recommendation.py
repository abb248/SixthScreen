# ============================================================
# SixthScreen — Recommendation Engine
# ============================================================
# This module is the heart of the project — Cosine Similarity
# algorithm lives here.
#
# What it does:
#   1. Takes the user's mood vector
#   2. Compares it with every movie's mood vector
#   3. Finds the closest 5 movies (cosine similarity)
#   4. Weights with TMDB global rating
#   5. Calculates final score and ranks
# ============================================================

import numpy as np
from sqlalchemy.orm import Session

from app.models import MovieCache, Recommendation, QuizSession
from app.config import settings


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Calculates cosine similarity between two vectors.

    What is Cosine Similarity?
        Measures the angle between two arrows.
        Same direction → 1 (very similar)
        Perpendicular  → 0 (unrelated)
        Opposite       → -1 (completely opposite)

    Formula:
        cos(θ) = (A · B) / (|A| × |B|)

    Args:
        vec_a: First vector (user mood)
        vec_b: Second vector (movie mood)

    Returns:
        Similarity score between -1 and 1
    """
    a = np.array(vec_a, dtype=float)
    b = np.array(vec_b, dtype=float)

    dot_product = np.dot(a, b)           # A · B (dot product)
    norm_a = np.linalg.norm(a)           # |A| (magnitude)
    norm_b = np.linalg.norm(b)           # |B| (magnitude)

    # Division by zero protection
    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def similarity_to_score(similarity: float) -> float:
    """
    Converts cosine similarity to a 0-10 score.

    similarity: -1 to 1 → score: 0 to 10
    Formula: score = (similarity + 1) × 5

    Examples:
        similarity = 1.0  → score = 10.0 (perfect match)
        similarity = 0.5  → score = 7.5
        similarity = 0.0  → score = 5.0 (neutral)
        similarity = -1.0 → score = 0.0 (complete opposite)
    """
    return round((similarity + 1) * 5, 2)


def calculate_final_score(match_score: float, tmdb_rating: float) -> float:
    """
    Match score + quality score = final score.

    Formula:
        final = (match × 0.6) + (quality × 0.4)

    Why 60%-40%?
        60% match: "Does this movie FIT YOU?"
        40% quality: "Is this movie GOOD globally?"
        This way you get both personal AND quality recommendations.

    Args:
        match_score: Match score (0-10)
        tmdb_rating: TMDB global rating (0-10)

    Returns:
        Final score (0-10)
    """
    final = (match_score * settings.MATCH_WEIGHT) + (tmdb_rating * settings.QUALITY_WEIGHT)
    return round(final, 2)


def generate_explanation(
    mood_labels: dict[str, float],
    movie_genres: list[str],
    match_score: float,
    quality_score: float
) -> str:
    """
    Generates a "Why we recommend this" explanation.

    Args:
        mood_labels: {"energy": 7.2, "darkness": 3.1, ...}
        movie_genres: ["Action", "Sci-Fi"]
        match_score: Match score
        quality_score: Quality score

    Returns:
        Explanation text
    """
    # Find top 2 mood dimensions
    top_moods = sorted(mood_labels.items(), key=lambda x: x[1], reverse=True)[:2]
    mood_desc = " and ".join([f"high {m[0]}" for m in top_moods])

    genre_str = ", ".join(movie_genres[:3]) if movie_genres else "various genres"

    if match_score >= 8:
        match_text = "Perfectly matches your mood"
    elif match_score >= 6:
        match_text = "Strongly matches your mood"
    else:
        match_text = "Partially matches your mood"

    if quality_score >= 7.5:
        quality_text = "a highly acclaimed production"
    elif quality_score >= 6:
        quality_text = "a well-rated production"
    else:
        quality_text = "a hidden gem worth discovering"

    return f"{match_text}. Your {mood_desc} mood aligns well with this {genre_str} {quality_text}."


def get_recommendations(
    db: Session,
    session: QuizSession,
    mood_vector: list[float],
    count: int = None
) -> list[dict]:
    """
    Main recommendation function.

    1. Fetch all movies from database
    2. Calculate cosine similarity with each movie's mood vector
    3. Match + quality = final score
    4. Return top 5 movies

    Args:
        db: Database session
        session: Quiz session
        mood_vector: User's mood vector
        count: How many recommendations (default: from settings)

    Returns:
        Sorted list of recommendations
    """
    if count is None:
        count = settings.RECOMMENDATION_COUNT

    # Fetch all cached movies
    movies = db.query(MovieCache).filter(
        MovieCache.vote_count > 50  # Filter out movies with too few votes (unreliable rating)
    ).all()

    if not movies:
        return []

    # Mood labels
    from app.quiz_engine import mood_vector_to_labels
    mood_labels = mood_vector_to_labels(mood_vector)

    # Calculate score for each movie
    scored_movies = []
    for movie in movies:
        movie_vector = [float(v) for v in movie.mood_vector]

        # Cosine similarity
        similarity = cosine_similarity(mood_vector, movie_vector)
        match_score = similarity_to_score(similarity)

        # TMDB quality score
        quality_score = float(movie.tmdb_rating) if movie.tmdb_rating else 5.0

        # Final score
        final_score = calculate_final_score(match_score, quality_score)

        # Explanation
        genres = movie.genres if movie.genres else []
        explanation = generate_explanation(mood_labels, genres, match_score, quality_score)

        scored_movies.append({
            "movie": movie,
            "match_score": match_score,
            "quality_score": quality_score,
            "final_score": final_score,
            "explanation": explanation,
        })

    # Sort by final score (highest first)
    scored_movies.sort(key=lambda x: x["final_score"], reverse=True)

    # Take top N
    top_movies = scored_movies[:count]

    # Save to database
    for rank, item in enumerate(top_movies, start=1):
        rec = Recommendation(
            session_id=session.id,
            movie_id=item["movie"].id,
            match_score=item["match_score"],
            quality_score=item["quality_score"],
            final_score=item["final_score"],
            rank_position=rank,
            explanation=item["explanation"],
        )
        db.add(rec)
        item["rank"] = rank

    db.commit()

    return top_movies
