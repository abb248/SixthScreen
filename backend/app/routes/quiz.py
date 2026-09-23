# ============================================================
# SixthScreen — Quiz API Endpoints
# ============================================================

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Question, QuizSession, QuizAnswer
from app.schemas import (
    QuestionOut, QuizStartResponse,
    AnswerRequest, MessageResponse,
    QuizCompleteRequest, RecommendationResponse, RecommendationOut, MovieOut
)
from app.quiz_engine import select_questions, get_option_vector, calculate_mood_vector, mood_vector_to_labels
from app.recommendation import get_recommendations
from app.config import settings

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])


@router.post("/start", response_model=QuizStartResponse)
def start_quiz(db: Session = Depends(get_db)):
    """
    Starts a new quiz.

    1. Selects 8 random questions from the pool
    2. Creates a new quiz session
    3. Returns questions and session ID

    Usage:
        POST /api/quiz/start
        → { session_id: 42, questions: [...], total_questions: 8 }
    """
    # Select questions
    questions = select_questions(db)

    if not questions:
        raise HTTPException(status_code=500, detail="No active questions in the pool!")

    # Create new session
    session = QuizSession(
        question_count=len(questions),
        completed=False,
        mood_vector=[5.0] * 6  # Starting point: neutral
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Return formatted questions (vectors are HIDDEN from the user!)
    questions_out = [
        QuestionOut(
            id=q.id,
            question_text=q.question_text,
            question_type=q.question_type,
            option_a=q.option_a_text,
            option_b=q.option_b_text,
            option_c=q.option_c_text,
            option_d=q.option_d_text,
        )
        for q in questions
    ]

    return QuizStartResponse(
        session_id=session.id,
        questions=questions_out,
        total_questions=len(questions),
    )


@router.post("/answer", response_model=MessageResponse)
def submit_answer(answer: AnswerRequest, db: Session = Depends(get_db)):
    """
    Saves an answer to a question.

    Usage:
        POST /api/quiz/answer
        Body: { session_id: 42, question_id: 5, selected_option: "b" }
        → { message: "Answer saved", success: true }
    """
    # Does the session exist?
    session = db.query(QuizSession).filter(QuizSession.id == answer.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Quiz session not found")
    if session.completed:
        raise HTTPException(status_code=400, detail="This quiz is already completed")

    # Does the question exist?
    question = db.query(Question).filter(Question.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Get the selected option's vector
    vector = get_option_vector(question, answer.selected_option)

    # Save the answer
    quiz_answer = QuizAnswer(
        session_id=answer.session_id,
        question_id=answer.question_id,
        selected_option=answer.selected_option,
        answer_vector=vector,
    )
    db.add(quiz_answer)
    db.commit()

    return MessageResponse(message="Answer saved", success=True)


@router.post("/complete", response_model=RecommendationResponse)
def complete_quiz(request: QuizCompleteRequest, db: Session = Depends(get_db)):
    """
    Completes the quiz and returns recommendations.

    1. Calculates mood vector from all answers
    2. Matches with movies
    3. Returns top 5 recommendations

    Usage:
        POST /api/quiz/complete
        Body: { session_id: 42 }
        → { mood_vector: [...], recommendations: [...] }
    """
    session = db.query(QuizSession).filter(QuizSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Quiz session not found")
    if session.completed:
        raise HTTPException(status_code=400, detail="This quiz is already completed")

    # Get all answers
    answers = db.query(QuizAnswer).filter(QuizAnswer.session_id == session.id).all()
    if not answers:
        raise HTTPException(status_code=400, detail="No answers submitted")

    # Calculate mood vector
    mood_vector = calculate_mood_vector(answers)
    mood_labels = mood_vector_to_labels(mood_vector)

    # Update session
    session.mood_vector = mood_vector
    session.completed = True
    db.commit()

    # Calculate recommendations
    from app.tmdb_client import tmdb_client
    top_movies = get_recommendations(db, session, mood_vector)

    # Format response
    recommendations_out = []
    for item in top_movies:
        movie = item["movie"]
        recommendations_out.append(RecommendationOut(
            rank=item["rank"],
            movie=MovieOut(
                tmdb_id=movie.tmdb_id,
                title=movie.title,
                original_title=movie.original_title,
                overview=movie.overview,
                poster_url=tmdb_client.get_poster_url(movie.poster_path),
                backdrop_url=tmdb_client.get_backdrop_url(movie.backdrop_path),
                genres=movie.genres or [],
                tmdb_rating=float(movie.tmdb_rating) if movie.tmdb_rating else 0,
                vote_count=movie.vote_count or 0,
                release_date=str(movie.release_date) if movie.release_date else None,
                media_type=movie.media_type,
            ),
            match_score=item["match_score"],
            quality_score=item["quality_score"],
            final_score=item["final_score"],
            explanation=item["explanation"],
        ))

    return RecommendationResponse(
        session_id=session.id,
        mood_vector=mood_vector,
        mood_labels=mood_labels,
        recommendations=recommendations_out,
        generated_at=datetime.now(),
    )
