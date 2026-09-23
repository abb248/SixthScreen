-- ============================================================
-- SixthScreen — TÜR → MOOD VEKTÖR HARİTASI
-- ============================================================
-- Her film türünün varsayılan mood profili.
-- Film birden fazla türe sahipse, vektörlerin ortalaması alınır.
-- Vektör: [enerji, karanlık, zeka, duygusallık, macera, sosyallik]
-- ============================================================

INSERT INTO genre_mood_map (genre_name, tmdb_genre_id, mood_vector) VALUES
    ('Action',          28,    ARRAY[9, 5, 3, 2, 7, 6]),
    ('Adventure',       12,    ARRAY[8, 3, 4, 4, 9, 6]),
    ('Animation',       16,    ARRAY[7, 2, 4, 6, 6, 8]),
    ('Comedy',          35,    ARRAY[7, 1, 3, 4, 4, 9]),
    ('Crime',           80,    ARRAY[6, 8, 7, 3, 6, 4]),
    ('Documentary',     99,    ARRAY[3, 4, 10, 5, 6, 3]),
    ('Drama',           18,    ARRAY[4, 6, 6, 9, 5, 4]),
    ('Family',          10751, ARRAY[6, 1, 3, 6, 4, 9]),
    ('Fantasy',         14,    ARRAY[7, 4, 5, 6, 9, 6]),
    ('History',         36,    ARRAY[4, 5, 8, 6, 5, 4]),
    ('Horror',          27,    ARRAY[6, 10, 4, 2, 6, 5]),
    ('Music',           10402, ARRAY[7, 3, 3, 7, 4, 7]),
    ('Mystery',         9648,  ARRAY[5, 7, 9, 4, 8, 3]),
    ('Romance',         10749, ARRAY[4, 2, 3, 10, 5, 7]),
    ('Science Fiction',  878,  ARRAY[7, 5, 9, 4, 9, 4]),
    ('Thriller',        53,    ARRAY[7, 9, 8, 3, 7, 3]),
    ('TV Movie',        10770, ARRAY[5, 4, 4, 6, 3, 6]),
    ('War',             10752, ARRAY[6, 8, 5, 7, 6, 4]),
    ('Western',         37,    ARRAY[7, 6, 4, 4, 7, 4]),

    -- TV türleri (diziler için)
    ('Action & Adventure',  10759, ARRAY[9, 5, 4, 3, 9, 6]),
    ('Kids',                10762, ARRAY[7, 1, 2, 5, 5, 8]),
    ('News',                10763, ARRAY[4, 5, 7, 3, 3, 5]),
    ('Reality',             10764, ARRAY[6, 3, 2, 4, 4, 8]),
    ('Sci-Fi & Fantasy',    10765, ARRAY[7, 5, 8, 5, 9, 5]),
    ('Soap',                10766, ARRAY[4, 4, 2, 9, 3, 7]),
    ('Talk',                10767, ARRAY[6, 2, 4, 4, 3, 9]),
    ('War & Politics',      10768, ARRAY[5, 7, 7, 5, 5, 4]);


-- ============================================================
-- ✅ 27 tür → mood vektör eşlemesi eklendi!
-- Film vektörü hesaplama:
--   film.mood_vector = AVG(tür1.mood_vector, tür2.mood_vector, ...)
-- ============================================================
