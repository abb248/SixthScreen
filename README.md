# 🎬 SixthScreen

> A mood-based movie & TV show recommendation engine that analyzes your subconscious through creative questions.

**Full documentation:** [PROJECT-GUIDE.md](PROJECT-GUIDE.md)

## How It Works
8 creative questions → 6-dimensional mood vector → cosine similarity matching → top 5 personalized recommendations

## Tech Stack
`Python` · `FastAPI` · `PostgreSQL` · `Next.js` · `NumPy` · `TMDB API` · `Cosine Similarity`

## Quick Start
```bash
cd backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
→ API docs: http://localhost:8000/docs

## Algorithm
```
final_score = (cosine_similarity_match × 0.6) + (tmdb_global_rating × 0.4)
```

## License
MIT
