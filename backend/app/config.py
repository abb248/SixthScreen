# ============================================================
# SixthScreen — Application Settings
# ============================================================
# Reads environment variables from the .env file.
# This keeps passwords and API keys OUT of the codebase.
# ============================================================

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    Automatically reads from .env file.
    """

    # Database connection string
    # Format: postgresql://user:password@host:port/database_name
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/sixthscreen_db"

    # TMDB API key — get from https://www.themoviedb.org/settings/api
    TMDB_API_KEY: str = ""

    # TMDB API base URL
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"

    # TMDB image base URL for posters
    TMDB_IMAGE_BASE_URL: str = "https://image.tmdb.org/t/p/w500"

    # App settings
    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    # Quiz settings
    QUIZ_QUESTION_COUNT: int = 8           # How many questions per quiz
    RECOMMENDATION_COUNT: int = 5          # How many movies to recommend
    MATCH_WEIGHT: float = 0.6              # Match score weight (60%)
    QUALITY_WEIGHT: float = 0.4            # Quality score weight (40%)

    class Config:
        env_file = ".env"                  # Read from .env file
        env_file_encoding = "utf-8"


# Create a single settings instance — the whole app uses this
settings = Settings()
