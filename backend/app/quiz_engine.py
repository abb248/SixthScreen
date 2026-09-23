# ============================================================
# SixthScreen — Quiz Engine
# ============================================================
# This module is the "brain" of the quiz.
# 1. Selects random questions from the pool (balanced distribution)
# 2. Calculates mood vector from answers (averaging)
#
# Mood Vector = [energy, darkness, intellect, emotion, adventure, social]
# Each dimension ranges 0-10.
# ============================================================

import random
from sqlalchemy.orm import Session

from app.models import Question, QuizSession, QuizAnswer
from app.config import settings


# Mood dimension names (in order)
MOOD_DIMENSIONS = ["energy", "darkness", "intellect", "emotion", "adventure", "social"]


def select_questions(db: Session, count: int = None) -> list[Question]:
    """
    Selects random questions from the pool with balanced distribution.

    Balance rule:
        - At least 2 subconscious questions
        - At least 2 movie questions
        - At least 2 abstract questions
        - Rest are random

    Args:
        db: Database session
        count: How many questions to select (default: from settings)

    Returns:
        List of selected questions
    """
    if count is None:
        count = settings.QUIZ_QUESTION_COUNT

    # Fetch active questions by category
    subconscious = db.query(Question).filter(
        Question.question_type == "subconscious",
        Question.is_active == True
    ).all()

    movie = db.query(Question).filter(
        Question.question_type == "movie",
        Question.is_active == True
    ).all()

    abstract = db.query(Question).filter(
        Question.question_type == "abstract",
        Question.is_active == True
    ).all()

    # Select at least 2 from each category
    selected = []
    min_per_category = 2
    selected.extend(random.sample(subconscious, min(min_per_category, len(subconscious))))
    selected.extend(random.sample(movie, min(min_per_category, len(movie))))
    selected.extend(random.sample(abstract, min(min_per_category, len(abstract))))

    # Fill remaining slots from all questions (excluding already selected)
    selected_ids = {q.id for q in selected}
    remaining_pool = [
        q for q in (subconscious + movie + abstract)
        if q.id not in selected_ids
    ]

    remaining_count = count - len(selected)
    if remaining_count > 0 and remaining_pool:
        selected.extend(random.sample(remaining_pool, min(remaining_count, len(remaining_pool))))

    # Shuffle order (so questions don't always appear in the same order)
    random.shuffle(selected)

    return selected


def get_option_vector(question: Question, option: str) -> list[float]:
    """
    Returns the mood vector for the selected option.

    Args:
        question: Question object
        option: 'a', 'b', 'c' or 'd'

    Returns:
        6-dimensional mood vector
    """
    vector_map = {
        "a": question.option_a_vector,
        "b": question.option_b_vector,
        "c": question.option_c_vector,
        "d": question.option_d_vector,
    }
    raw = vector_map.get(option, question.option_a_vector)
    return [float(v) for v in raw]


def calculate_mood_vector(answers: list[QuizAnswer]) -> list[float]:
    """
    Calculates the user's mood vector by averaging all answer vectors.

    Example:
        Answer 1: [8, 2, 5, 3, 7, 6]
        Answer 2: [4, 6, 7, 8, 3, 2]
        Answer 3: [6, 4, 6, 5, 5, 4]
        ─────────────────────────────
        Average:  [6, 4, 6, 5.3, 5, 4]

    Args:
        answers: List of QuizAnswer objects

    Returns:
        6-dimensional average mood vector
    """
    if not answers:
        return [5.0] * 6  # Default: neutral

    # Sum each dimension separately
    dimension_count = 6
    totals = [0.0] * dimension_count

    for answer in answers:
        vector = [float(v) for v in answer.answer_vector]
        for i in range(dimension_count):
            totals[i] += vector[i]

    # Calculate average
    count = len(answers)
    mood_vector = [round(totals[i] / count, 2) for i in range(dimension_count)]

    return mood_vector


def mood_vector_to_labels(mood_vector: list[float]) -> dict[str, float]:
    """
    Converts mood vector to readable labels.

    Args:
        mood_vector: [7.2, 3.1, 5.5, 8.0, 4.2, 6.8]

    Returns:
        {"energy": 7.2, "darkness": 3.1, "intellect": 5.5, ...}
    """
    return {
        MOOD_DIMENSIONS[i]: mood_vector[i]
        for i in range(len(MOOD_DIMENSIONS))
    }
