-- ============================================================
-- SixthScreen — VERİTABANI ŞEMASI
-- ============================================================
-- "Bilinçaltın ne izlemek istiyor?" uygulamasının veritabanı.
--
-- MOOD VEKTÖRÜ = 6 boyutlu dizi:
-- [enerji, karanlık, zeka, duygusallık, macera, sosyallik]
-- Her boyut 0-10 arası bir değer alır.
-- ============================================================


-- ============================================================
-- 1. KULLANICILAR
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(50) UNIQUE NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- 2. SORULAR
-- Quiz motorunun temel tablosu. Her sorunun 4 seçeneği var
-- ve her seçenek mood vektörüne farklı etki eder.
--
-- question_type:
--   'movie'       → Filmlerle doğrudan ilgili sorular
--   'subconscious'→ Bilinçaltı sorular (renk, hava, süper güç)
--   'abstract'    → Soyut/yaratıcı sorular
-- ============================================================
CREATE TABLE IF NOT EXISTS questions (
    id              SERIAL PRIMARY KEY,
    question_text   TEXT NOT NULL,
    question_type   VARCHAR(20) NOT NULL
                    CHECK (question_type IN ('movie', 'subconscious', 'abstract')),

    option_a_text   TEXT NOT NULL,
    option_a_vector DECIMAL[] NOT NULL,  -- [enerji, karanlık, zeka, duygusal, macera, sosyal]

    option_b_text   TEXT NOT NULL,
    option_b_vector DECIMAL[] NOT NULL,

    option_c_text   TEXT NOT NULL,
    option_c_vector DECIMAL[] NOT NULL,

    option_d_text   TEXT NOT NULL,
    option_d_vector DECIMAL[] NOT NULL,

    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- 3. QUIZ OTURUMLARI
-- Her quiz bir "oturum". Aynı kullanıcı farklı zamanlarda
-- farklı mood vektörleri üretir — bu uzun vadeli keşfi sağlar.
-- ============================================================
CREATE TABLE IF NOT EXISTS quiz_sessions (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,
    mood_vector     DECIMAL[] NOT NULL,          -- Hesaplanan final vektör
    question_count  INTEGER NOT NULL DEFAULT 0,  -- Kaç soru soruldu
    completed       BOOLEAN DEFAULT false,
    created_at      TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- 4. VERİLEN CEVAPLAR
-- Her soruya verilen cevap ve o cevabın vektörü.
-- Sonradan analiz için saklanır.
-- ============================================================
CREATE TABLE IF NOT EXISTS quiz_answers (
    id              SERIAL PRIMARY KEY,
    session_id      INTEGER REFERENCES quiz_sessions(id) ON DELETE CASCADE,
    question_id     INTEGER REFERENCES questions(id),
    selected_option CHAR(1) NOT NULL CHECK (selected_option IN ('a', 'b', 'c', 'd')),
    answer_vector   DECIMAL[] NOT NULL,
    answered_at     TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- 5. FİLM/DİZİ CACHE
-- TMDB API'den çekilen filmler burada saklanır.
-- Her seferinde API'ye istek atmamak için cache mekanizması.
-- ============================================================
CREATE TABLE IF NOT EXISTS movies_cache (
    id              SERIAL PRIMARY KEY,
    tmdb_id         INTEGER UNIQUE NOT NULL,
    title           VARCHAR(500) NOT NULL,
    original_title  VARCHAR(500),
    overview        TEXT,
    poster_path     VARCHAR(300),
    backdrop_path   VARCHAR(300),
    genres          TEXT[],                        -- {'Action', 'Comedy', 'Drama'}
    mood_vector     DECIMAL[] NOT NULL,            -- Otomatik hesaplanan [6 boyut]
    tmdb_rating     DECIMAL(4,2) DEFAULT 0,       -- TMDB puanı (0-10)
    vote_count      INTEGER DEFAULT 0,
    release_date    DATE,
    media_type      VARCHAR(10) DEFAULT 'movie'   -- 'movie' veya 'tv'
                    CHECK (media_type IN ('movie', 'tv')),
    popularity      DECIMAL(10,3) DEFAULT 0,
    cached_at       TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- 6. ÖNERİLER
-- Her quiz sonrası üretilen Top 5 öneri.
-- ============================================================
CREATE TABLE IF NOT EXISTS recommendations (
    id              SERIAL PRIMARY KEY,
    session_id      INTEGER REFERENCES quiz_sessions(id) ON DELETE CASCADE,
    movie_id        INTEGER REFERENCES movies_cache(id),
    match_score     DECIMAL(5,2) NOT NULL,        -- Eşleşme puanı (0-10)
    quality_score   DECIMAL(5,2) NOT NULL,        -- Global kalite (0-10)
    final_score     DECIMAL(5,2) NOT NULL,        -- Final puan (0-10)
    rank_position   INTEGER NOT NULL,             -- 1-5 sıralama
    explanation     TEXT,                          -- Neden öneriyoruz?
    created_at      TIMESTAMP DEFAULT NOW()
);


-- ============================================================
-- 7. İZLEME GEÇMİŞİ & DEĞERLENDİRME
-- Kullanıcının izlediği/izlemek istediği filmler.
-- ============================================================
CREATE TABLE IF NOT EXISTS watch_history (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,
    movie_id        INTEGER REFERENCES movies_cache(id),
    user_rating     INTEGER CHECK (user_rating BETWEEN 1 AND 10),
    watched         BOOLEAN DEFAULT false,
    watchlist       BOOLEAN DEFAULT true,          -- İzleme listesinde mi?
    added_at        TIMESTAMP DEFAULT NOW(),
    watched_at      TIMESTAMP,
    UNIQUE (user_id, movie_id)
);


-- ============================================================
-- 8. TÜR → MOOD VEKTÖR HARİTASI
-- Her film türünün varsayılan mood vektörü.
-- Film vektörü = türlerinin vektörlerinin ortalaması.
-- ============================================================
CREATE TABLE IF NOT EXISTS genre_mood_map (
    id              SERIAL PRIMARY KEY,
    genre_name      VARCHAR(50) UNIQUE NOT NULL,
    tmdb_genre_id   INTEGER UNIQUE,
    mood_vector     DECIMAL[] NOT NULL             -- [enerji, karanlık, zeka, duygusal, macera, sosyal]
);


-- ============================================================
-- INDEX'LER
-- ============================================================
CREATE INDEX idx_quiz_sessions_user ON quiz_sessions(user_id);
CREATE INDEX idx_quiz_answers_session ON quiz_answers(session_id);
CREATE INDEX idx_recommendations_session ON recommendations(session_id);
CREATE INDEX idx_watch_history_user ON watch_history(user_id);
CREATE INDEX idx_movies_cache_tmdb_id ON movies_cache(tmdb_id);
CREATE INDEX idx_movies_cache_media_type ON movies_cache(media_type);


-- ============================================================
-- ✅ Tablolar başarıyla oluşturuldu!
-- Sıradaki: 02_seed_questions.sql
-- ============================================================
