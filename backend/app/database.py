# ============================================================
# SixthScreen — Database Connection
# ============================================================
# Uses SQLAlchemy to connect to PostgreSQL.
#
# SQLAlchemy: Bridge between Python and the database.
#   Write Python objects instead of raw SQL.
#
# Session: A "conversation" with the database.
#   Each API request opens a new session, closes when done.
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# ── Create the database engine ──
# The engine manages the connection pool to PostgreSQL.
# pool_pre_ping=True: Checks if connection is still alive before using it
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.APP_DEBUG  # In debug mode, prints SQL queries to console
)

# ── Session factory ──
# Creates a new session for each API request
SessionLocal = sessionmaker(
    autocommit=False,   # Manual commit — you control when changes are saved
    autoflush=False,    # Manual flush — you control performance
    bind=engine
)

# ── Base class for all models ──
# All table models inherit from this class
Base = declarative_base()


def get_db():
    """
    Provides a database session for each API request.
    Automatically closes when the request is done.

    Usage (in FastAPI):
        @app.get("/example")
        def example(db: Session = Depends(get_db)):
            ...

    How "yield" works:
        Function pauses, session is given to the route.
        When request finishes, "finally" block runs and session closes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
