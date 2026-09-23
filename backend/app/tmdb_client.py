# ============================================================
# SixthScreen — TMDB API Client
# ============================================================
# Fetches movie/TV show data from TMDB (The Movie Database) API.
# Fetched data is cached in the database.
#
# TMDB: Free API with 1M+ movies and TV shows.
#   Posters, ratings, genres, descriptions — everything.
#   Get API key: https://www.themoviedb.org/settings/api
# ============================================================

import httpx
from sqlalchemy.orm import Session

from app.models import MovieCache, GenreMoodMap
from app.config import settings


class TMDBClient:
    """Class that communicates with the TMDB API."""

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.image_base = settings.TMDB_IMAGE_BASE_URL

    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """
        Makes a request to the TMDB API.

        Args:
            endpoint: API path (e.g., "/movie/popular")
            params: Additional parameters

        Returns:
            JSON response (dict)
        """
        if not self.api_key:
            raise ValueError(
                "TMDB API key not set! "
                "Add TMDB_API_KEY=... to your .env file. "
                "Get key from: https://www.themoviedb.org/settings/api"
            )

        url = f"{self.base_url}{endpoint}"
        default_params = {
            "api_key": self.api_key,
            "language": "en-US",           # English results
        }
        if params:
            default_params.update(params)

        response = httpx.get(url, params=default_params, timeout=10.0)
        response.raise_for_status()
        return response.json()

    def get_popular_movies(self, page: int = 1) -> list[dict]:
        """Fetch popular movies."""
        data = self._make_request("/movie/popular", {"page": page})
        return data.get("results", [])

    def get_popular_tv(self, page: int = 1) -> list[dict]:
        """Fetch popular TV shows."""
        data = self._make_request("/tv/popular", {"page": page})
        return data.get("results", [])

    def get_top_rated_movies(self, page: int = 1) -> list[dict]:
        """Fetch top rated movies."""
        data = self._make_request("/movie/top_rated", {"page": page})
        return data.get("results", [])

    def get_top_rated_tv(self, page: int = 1) -> list[dict]:
        """Fetch top rated TV shows."""
        data = self._make_request("/tv/top_rated", {"page": page})
        return data.get("results", [])

    def get_movie_details(self, movie_id: int) -> dict:
        """Fetch details for a specific movie."""
        return self._make_request(f"/movie/{movie_id}")

    def get_tv_details(self, tv_id: int) -> dict:
        """Fetch details for a specific TV show."""
        return self._make_request(f"/tv/{tv_id}")

    def get_poster_url(self, poster_path: str) -> str | None:
        """Converts poster path to full URL."""
        if poster_path:
            return f"{self.image_base}{poster_path}"
        return None

    def get_backdrop_url(self, backdrop_path: str) -> str | None:
        """Converts backdrop path to full URL."""
        if backdrop_path:
            return f"{self.image_base}{backdrop_path}"
        return None


def calculate_movie_mood_vector(genre_ids: list[int], db: Session) -> list[float]:
    """
    Calculates a movie's mood vector from its genres.

    Each genre has a mood vector (in genre_mood_map table).
    Movie vector = average of its genres' vectors.

    Example:
        Action  = [9, 5, 3, 2, 7, 6]
        Sci-Fi  = [7, 5, 9, 4, 9, 4]
        Average = [8, 5, 6, 3, 8, 5]

    Args:
        genre_ids: List of TMDB genre IDs
        db: Database session

    Returns:
        6-dimensional mood vector
    """
    if not genre_ids:
        return [5.0] * 6  # Default: neutral

    # Fetch genre vectors from database
    genre_maps = db.query(GenreMoodMap).filter(
        GenreMoodMap.tmdb_genre_id.in_(genre_ids)
    ).all()

    if not genre_maps:
        return [5.0] * 6

    # Calculate average
    dimension_count = 6
    totals = [0.0] * dimension_count

    for gm in genre_maps:
        vector = [float(v) for v in gm.mood_vector]
        for i in range(dimension_count):
            totals[i] += vector[i]

    count = len(genre_maps)
    return [round(totals[i] / count, 2) for i in range(dimension_count)]


def fetch_and_cache_movies(db: Session, pages: int = 3) -> int:
    """
    Fetches popular and top-rated movies/TV shows from TMDB
    and caches them in the database.

    Args:
        db: Database session
        pages: How many pages to fetch from each category

    Returns:
        Total number of movies/shows added
    """
    client = TMDBClient()
    added = 0

    # Collect movie and TV show lists
    all_items = []

    for page in range(1, pages + 1):
        # Popular movies
        for movie in client.get_popular_movies(page):
            movie["_media_type"] = "movie"
            all_items.append(movie)

        # Top rated movies
        for movie in client.get_top_rated_movies(page):
            movie["_media_type"] = "movie"
            all_items.append(movie)

        # Popular TV shows
        for tv in client.get_popular_tv(page):
            tv["_media_type"] = "tv"
            all_items.append(tv)

        # Top rated TV shows
        for tv in client.get_top_rated_tv(page):
            tv["_media_type"] = "tv"
            all_items.append(tv)

    # Add each item to database (skip if already exists)
    for item in all_items:
        tmdb_id = item.get("id")
        if not tmdb_id:
            continue

        # Check if already cached
        exists = db.query(MovieCache).filter(MovieCache.tmdb_id == tmdb_id).first()
        if exists:
            continue

        media_type = item["_media_type"]
        genre_ids = item.get("genre_ids", [])
        mood_vector = calculate_movie_mood_vector(genre_ids, db)

        # Movie or TV show?
        title = item.get("title") or item.get("name", "Unknown")
        original_title = item.get("original_title") or item.get("original_name")
        release_date_str = item.get("release_date") or item.get("first_air_date")

        # Fetch genre names
        genre_names_query = db.query(GenreMoodMap.genre_name).filter(
            GenreMoodMap.tmdb_genre_id.in_(genre_ids)
        ).all()
        genre_names = [g[0] for g in genre_names_query]

        movie = MovieCache(
            tmdb_id=tmdb_id,
            title=title,
            original_title=original_title,
            overview=item.get("overview", ""),
            poster_path=item.get("poster_path"),
            backdrop_path=item.get("backdrop_path"),
            genres=genre_names,
            mood_vector=mood_vector,
            tmdb_rating=item.get("vote_average", 0),
            vote_count=item.get("vote_count", 0),
            release_date=release_date_str if release_date_str else None,
            media_type=media_type,
            popularity=item.get("popularity", 0),
        )
        db.add(movie)
        added += 1

    db.commit()
    return added


# Singleton instance
tmdb_client = TMDBClient()
