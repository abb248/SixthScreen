-- ============================================================
-- SixthScreen — SORU VERİLERİ (SEED DATA)
-- ============================================================
-- Her sorunun 4 seçeneği var. Her seçenek 6 boyutlu mood vektörüne
-- farklı etki eder:
-- [enerji, karanlık, zeka, duygusallık, macera, sosyallik]
-- Değerler 0-10 arası.
-- ============================================================


-- ============================================================
-- BİLİNÇALTI SORULAR (film dışı — asıl sihir burada!)
-- ============================================================

INSERT INTO questions (question_text, question_type, option_a_text, option_a_vector, option_b_text, option_b_vector, option_c_text, option_c_vector, option_d_text, option_d_vector) VALUES

-- Soru 1: Renk
('Şu an bir renk seçsen, hangisi olurdu?',
 'subconscious',
 '🔴 Kırmızı — ateş, tutku, güç',        ARRAY[8, 6, 3, 5, 7, 5],
 '🔵 Mavi — huzur, derinlik, düşünce',    ARRAY[3, 4, 8, 7, 4, 3],
 '🟡 Sarı — enerji, neşe, iyimserlik',    ARRAY[9, 1, 3, 4, 5, 9],
 '🟣 Mor — gizem, yaratıcılık, bilinmeyen', ARRAY[5, 7, 7, 5, 8, 3]),

-- Soru 2: Hava durumu
('Şu an pencereden baktığında hangi havayı görmek isterdin?',
 'subconscious',
 '☀️ Güneşli ve sıcak',                   ARRAY[8, 1, 3, 4, 5, 8],
 '🌧️ Yağmurlu ve sakin',                  ARRAY[3, 6, 6, 8, 3, 2],
 '⛈️ Fırtınalı ve kaotik',                ARRAY[7, 8, 4, 3, 8, 3],
 '❄️ Karlı ve sessiz',                     ARRAY[2, 5, 7, 7, 4, 2]),

-- Soru 3: Süper güç
('Bir süper gücün olsaydı hangisini seçerdin?',
 'subconscious',
 '⏰ Zaman yolculuğu',                     ARRAY[5, 4, 9, 5, 9, 4],
 '👻 Görünmezlik',                          ARRAY[4, 7, 5, 3, 7, 2],
 '🦅 Uçabilmek',                            ARRAY[9, 2, 3, 4, 9, 5],
 '🧠 Zihin okuma',                           ARRAY[4, 5, 8, 7, 5, 6]),

-- Soru 4: Masada ne var?
('Bir masaya oturuyorsun. Masada ne olmasını isterdin?',
 'subconscious',
 '📚 Kitap ve kahve',                       ARRAY[3, 4, 9, 5, 5, 1],
 '🍻 Arkadaşlar ve içecekler',             ARRAY[8, 2, 3, 5, 4, 10],
 '📝 Boş kağıt ve kalem',                  ARRAY[4, 5, 7, 6, 7, 2],
 '🕯️ Mum ışığı ve müzik',                 ARRAY[3, 6, 4, 9, 3, 4]),

-- Soru 5: Müzik
('Şu an hangi müzik türü ruhunu anlatır?',
 'subconscious',
 '🎸 Rock / Metal — sert, enerjik',        ARRAY[9, 6, 4, 3, 7, 5],
 '🎹 Klasik / Jazz — zarif, derin',        ARRAY[3, 4, 9, 7, 4, 3],
 '🎤 Pop / Dans — neşeli, sosyal',         ARRAY[8, 1, 2, 4, 4, 9],
 '🎧 Lo-fi / Ambient — sakin, düşünceli',  ARRAY[2, 5, 6, 7, 3, 2]),

-- Soru 6: Yolculuk
('Sihirli bir kapı seni bir yere götürecek. Nereyi seçersin?',
 'subconscious',
 '🏔️ Issız bir dağ tepesi',                ARRAY[5, 5, 6, 6, 8, 1],
 '🌃 Neon ışıklı gece şehri',              ARRAY[8, 6, 5, 3, 7, 7],
 '🏖️ Sakin bir sahil kasabası',            ARRAY[4, 1, 3, 7, 4, 6],
 '🏚️ Terk edilmiş eski bir kale',          ARRAY[4, 9, 7, 4, 9, 2]),

-- Soru 7: Hayvan
('Ruhunu temsil eden hayvan hangisi?',
 'subconscious',
 '🐺 Kurt — bağımsız, güçlü',              ARRAY[7, 6, 5, 3, 8, 2],
 '🦉 Baykuş — bilge, gizemli',             ARRAY[3, 6, 9, 4, 5, 2],
 '🐬 Yunus — neşeli, sosyal',              ARRAY[7, 1, 4, 6, 5, 9],
 '🐈‍⬛ Kara kedi — bağımsız, gizemli',     ARRAY[4, 8, 6, 4, 7, 3]),

-- Soru 8: Zaman dilimi
('Hangi zaman diliminde yaşamak isterdin?',
 'subconscious',
 '⚔️ Ortaçağ — şövalyeler, kaleler',       ARRAY[7, 7, 4, 5, 9, 5],
 '🚀 Gelecek — uzay, teknoloji',           ARRAY[7, 4, 9, 3, 9, 4],
 '🎩 1920''ler — caz, gizemli geceler',     ARRAY[6, 6, 6, 6, 6, 7],
 '🌸 Şimdiki an — bu an güzel',            ARRAY[5, 3, 4, 7, 3, 6]),


-- ============================================================
-- FİLM İLİŞKİLİ SORULAR
-- ============================================================

-- Soru 9: Film karakteri
('Şu an bir film karakteri olsaydın hangisi olurdun?',
 'movie',
 '🔍 Sherlock Holmes — zeki, analitik',     ARRAY[6, 5, 10, 2, 7, 3],
 '🏃 Forrest Gump — saf, duygusal',         ARRAY[5, 3, 3, 10, 6, 7],
 '💀 John Wick — kararlı, tehlikeli',        ARRAY[9, 9, 4, 2, 7, 2],
 '🎨 Amélie — hayal gücü, romantik',         ARRAY[5, 3, 6, 9, 7, 5]),

-- Soru 10: Son izlediğinde ne etkiledi?
('Bir filmi izlerken seni en çok ne etkiler?',
 'movie',
 '💥 Aksiyon sahneleri ve görsel efektler',  ARRAY[9, 5, 2, 2, 7, 6],
 '🧩 Hikaye derinliği ve plot twist''ler',   ARRAY[4, 5, 10, 4, 8, 3],
 '😢 Duygusal sahneler ve müzik',           ARRAY[3, 4, 4, 10, 4, 5],
 '😂 Komik anlar ve diyaloglar',            ARRAY[7, 1, 4, 4, 3, 9]),

-- Soru 11: Nasıl izlersin?
('Film/dizi izlerken genelde nasılsın?',
 'movie',
 '🍿 Arkadaşlarla, gülüp eğlenerek',       ARRAY[8, 2, 3, 4, 4, 10],
 '🛋️ Yalnız, battaniyeye sarılıp',         ARRAY[3, 5, 5, 7, 4, 1],
 '🤔 Analiz ederek, detaylara dikkat ederek', ARRAY[4, 5, 9, 3, 6, 2],
 '📱 Arka planda, yarım yamalak',            ARRAY[5, 3, 2, 2, 3, 5]),

-- Soru 12: Finale ne dersin?
('Bir filmin/dizinin finali nasıl olsun?',
 'movie',
 '🎉 Mutlu son — herkes kazansın',           ARRAY[6, 1, 3, 7, 3, 7],
 '💔 Acı son — gerçekçi olsun',             ARRAY[3, 8, 6, 8, 5, 2],
 '❓ Açık uçlu — ben karar vereyim',        ARRAY[4, 5, 9, 4, 8, 3],
 '🤯 Beklenmedik twist — kafam karışsın',   ARRAY[7, 6, 9, 3, 9, 4]),

-- Soru 13: Hangi dünya?
('Hangi film/dizi evreninde yaşamak isterdin?',
 'movie',
 '⚡ Harry Potter — büyü, macera',           ARRAY[7, 4, 5, 6, 9, 7],
 '🤖 Matrix — simülasyon, felsefe',          ARRAY[5, 7, 10, 3, 8, 3],
 '🧟 The Walking Dead — hayatta kalma',      ARRAY[8, 9, 4, 3, 8, 4],
 '👑 Bridgerton — aşk, zarafet',             ARRAY[4, 2, 3, 10, 4, 8]),


-- ============================================================
-- SOYUT / YARATICI SORULAR
-- ============================================================

-- Soru 14: Anahtar
('Gizemli bir anahtar buldun. Neyi açar?',
 'abstract',
 '🚪 Hiç girilmemiş karanlık bir odayı',    ARRAY[5, 9, 7, 3, 9, 2],
 '📦 İçinde mektuplar olan bir sandığı',     ARRAY[3, 5, 5, 9, 6, 3],
 '🗺️ Gizli bir haritayı',                   ARRAY[7, 4, 6, 3, 10, 4],
 '⏰ Zamanı durduran bir saati',             ARRAY[4, 5, 9, 5, 7, 2]),

-- Soru 15: Son gece
('Dünya yarın bitiyor. Bu gece ne yaparsın?',
 'abstract',
 '🎉 En büyük partiyi ver',                  ARRAY[10, 3, 2, 4, 5, 10],
 '💌 Sevdiklerinle sessizce otur',           ARRAY[2, 5, 4, 10, 2, 7],
 '🌌 Yıldızlara bakarak düşün',             ARRAY[2, 6, 8, 7, 4, 1],
 '🏃 Son bir maceraya çık',                  ARRAY[9, 5, 3, 3, 10, 4]),

-- Soru 16: Rüya
('Tekrar eden bir rüya görüyorsun. Ne hakkında?',
 'abstract',
 '🏃 Bir şeyden kaçıyorsun',                ARRAY[7, 8, 4, 5, 7, 2],
 '✈️ Uçuyorsun, özgürsün',                  ARRAY[8, 2, 4, 5, 9, 4],
 '🔮 Geleceği görüyorsun',                  ARRAY[4, 5, 9, 4, 7, 3],
 '👤 Tanımadığın biriyle konuşuyorsun',      ARRAY[4, 5, 5, 7, 6, 6]),

-- Soru 17: Kitap
('Bir kitapçıdasın. Elini hangi kitaba uzatırsın?',
 'abstract',
 '🗡️ Epik fantastik serüven',               ARRAY[7, 5, 5, 4, 9, 5],
 '🔬 Bilim ve evrenin sırları',             ARRAY[4, 4, 10, 3, 7, 2],
 '💕 Aşk hikayesi',                          ARRAY[3, 3, 3, 10, 4, 6],
 '🕵️ Suç / dedektif romanı',               ARRAY[6, 8, 8, 2, 7, 3]),

-- Soru 18: Yemek
('Ruh haline uyan yemek hangisi?',
 'subconscious',
 '🌶️ Acılı, ateşli bir Meksika yemeği',    ARRAY[9, 5, 3, 3, 7, 6],
 '🍣 Zarif, minimal bir Japon yemeği',       ARRAY[4, 3, 7, 5, 6, 4],
 '🍝 Sıcacık, ev yapımı makarna',           ARRAY[4, 2, 3, 8, 2, 7],
 '🍫 Sadece çikolata ve çay',               ARRAY[3, 4, 4, 7, 2, 3]),

-- Soru 19: Sanat
('Bir sanat eserinin önündesin. Ne görüyorsun?',
 'abstract',
 '🌊 Dev bir dalga tablosu (güç, doğa)',     ARRAY[7, 5, 5, 5, 8, 3],
 '🖤 Tamamen siyah bir tuval (gizem)',       ARRAY[3, 9, 8, 4, 6, 1],
 '🌈 Renkli, soyut bir patlama (enerji)',    ARRAY[9, 2, 5, 5, 7, 6],
 '👁️ Seni izleyen bir portre (tedirginlik)', ARRAY[4, 8, 6, 5, 5, 2]),

-- Soru 20: Kapı
('Önünde 4 kapı var. Hangisinden geçersin?',
 'abstract',
 '🚪 Arkasından kahkaha sesi gelen',         ARRAY[7, 1, 3, 5, 4, 9],
 '🚪 Arkasından müzik gelen',                ARRAY[5, 4, 5, 7, 5, 5],
 '🚪 Hiç ses gelmeyen',                      ARRAY[3, 8, 7, 4, 8, 1],
 '🚪 Altından ışık sızan',                   ARRAY[6, 3, 6, 5, 7, 4]);


-- ============================================================
-- ✅ 20 soru başarıyla eklendi!
-- Dağılım: 8 bilinçaltı + 5 film + 7 soyut/yaratıcı
-- Her soru 4 seçenekli, her seçenek 6 boyutlu vektörle
-- ============================================================
