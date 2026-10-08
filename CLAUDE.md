# Loyiha qoidalari

Bu repoda ikki narsa bor:
- **Telegram bot** (`bot.py`, `database.py`, `questions.py`) — oilaviy bot.
- **Yuksalish Instagram reels** — ilm olishga targ'ib qiluvchi qisqa videolar (`yuksalish_*.mp4`, skriptlar `reels/` papkasida).

Quyidagi qoidalar Yuksalish videolari uchun. Foydalanuvchi bilan o'zbek tilida (lotin) gaplashing.

## Har bir video bilan birga taqdim etiladi (majburiy)

Video faylni yuborganda xabarda doim shular bo'lsin:

1. **Yuklash sanasi** — videoning Instagram'ga yuklanadigan kuni (quyidagi jadvaldan), format `DD.MM.YYYY`, hafta kuni bilan.
2. **Izoh (caption)** — nusxa ko'chirishga tayyor, alohida kod blokida. Tuzilishi: hook savol, qisqa ro'yxat yoki xulosa, saqlash/ulashish chaqirig'i, oxirgi qator `Yuksalish ilm bilan boshlanadi.` yoki mavzuga mos qisqa xulosa.
3. **Hashtaglar — roppa-rosa 3 ta** (ko'p emas). Doim `#yuksalish` birinchi, qolgan ikkitasi mavzuga mos.
4. **Fon musiqasi** — qaysi musiqa shabloni (pastdagi ro'yxatdan) ishlatilgani yoki kerakligi.

## Yuklash jadvali (kunlik, 1 video = 1 kun)

Birinchi video **09.10.2026 (juma)** da yuklanadi, qolganlari har kuni ketma-ket. Foydalanuvchi o'zgartirsa, shu jadvalni yangilang.

| # | Sana | Mavzu | Holat |
|---|---|---|---|
| 1 | 09.10.2026 (juma) | Ilm olishning 5 ta samarali usuli | tayyor: `yuksalish_5_usul.mp4` |
| 2 | 10.10.2026 (shanba) | Diqqatni jamlashning 5 yo'li | kutilmoqda |
| 3 | 11.10.2026 (yakshanba) | Kitob o'qishni odatga aylantirish | kutilmoqda |
| 4 | 12.10.2026 (dushanba) | Ertalabki 5 ta odat (ilm uchun) | kutilmoqda |
| 5 | 13.10.2026 (seshanba) | Imtihonga tayyorgarlik: 5 ta maslahat | kutilmoqda |
| 6 | 14.10.2026 (chorshanba) | Yangi til o'rganish: 5 ta sodda usul | kutilmoqda |
| 7 | 15.10.2026 (payshanba) | Vaqtni to'g'ri taqsimlash | kutilmoqda |
| 8 | 16.10.2026 (juma) | Charchaganda ham o'qishni davom ettirish | kutilmoqda |

Eslatma: `yuksalish_ilm.mp4` va `yuksalish_ilm_v2.mp4` — oyat/hadis bilan eski tajriba variantlari, jadvalga kirmaydi.

## Kontent uslubi

- Auditoriya: 15–40 yosh. **Faqat maslahatlar** formati.
- Ohang: yumshoq tavsiya ("shu usullar ko'proq samara beradi"), buyruq ohangi emas.
- Format: 1080×1920 (9:16), 25–35 soniya, o'zbek lotin, ekrandagi matn. TTS ishlatilmaydi (Microsoft TTS hosti tarmoq siyosati bilan bloklangan).
- Tuzilma: hook (3–4s) → 5 ta maslahat (har biri ~5s) → CTA (5–6s).
- Matn pastki-markazda yarim shaffof qora panelda, sarlavha oq, "N-usul" va manba/urg'u oltin (`0xFFD54F`). Instagram interfeysi yopadigan pastki ~250px va yuqori qismni bo'sh qoldiring.
- Oxirgi CTA animatsiyali piktogrammalar bilan, videoga qarab tartibi: maslahat ro'yxati → **Saqlash** birinchi; hikoya/ilhom → **Ulashish** birinchi; doim **Obuna** ham bor. Piktogrammalar Pillow bilan chiziladi (sakrab chiqish + yengil pulsatsiya).
- **Instagram belgisi:** keyingi videolardan boshlab oxirgi kadrda `YUKSALISH` yozuvining yonida Instagram piktogrammasi bo'lsin (gradientli yumaloq kvadrat ichida kamera belgisi, Pillow bilan chiziladi, tashqi logo fayl kerak emas). Foydalanuvchi Instagram nomini (`@...`) bersa, yozuvni shunga almashtiring.
- Ilmiy da'volarni umumiy tavsiya sifatida yozing; manbasiz aniq raqam/foiz yozmang.
- Oyat va hadisni faqat foydalanuvchi matn va manbani tasdiqlagandagina qo'shing; xotiradan qo'shmang. Manbani kichik yozuv bilan ko'rsating.

## Fon musiqasi

Foydalanuvchi musiqani o'zi Pixabay Music'dan yuklab beradi (Pixabay musiqa API'si ochiq emas). Mavzuga mos 6 ta shablon:

| Shablon | Pixabay Music'da qidiruv | Qaysi mavzularga |
|---|---|---|
| 1. Ilhom | `inspiring cinematic piano`, `motivational` | alloma hikoyalari, ilhomlantiruvchi videolar |
| 2. Fokus | `lofi study`, `calm focus` | diqqat, o'qish, imtihon |
| 3. Ertalab | `morning acoustic`, `uplifting guitar` | ertalabki odatlar |
| 4. Sokin | `soft ambient piano`, `peaceful` | charchoq, sabr, ma'naviy mavzular |
| 5. Tezkor | `upbeat positive`, `happy corporate` | tezkor maslahatlar, vaqt boshqaruvi |
| 6. Vlog | `vlog background`, `light chill` | umumiy, til o'rganish |

Talab: so'zsiz (instrumental), kamida 40 soniya, `.mp3`. Berilgan musiqa: `echoes_of_lumen-vlog-background-music-596303.mp3` (57s, 6-shablon).

## Texnik eslatmalar

- Klip manbai: Pixabay Videos API. Kalit `PIXABAY_API_KEY` muhit o'zgaruvchisida (hech qachon commit qilmang).
- Python `urllib` Pixabay'da 403 beradi; `curl` ishlaydi.
- Yig'ish: `ffmpeg` (drawtext, DejaVu Sans Bold — `'` va `–` belgilari to'g'ri chiqadi) + Pillow (CTA animatsiyasi). Skriptlar: `reels/fetch_clips.py` (nomzod klip qidirish va ko'rinishlar to'ri), `reels/build_tips_reel.py` (5 maslahatli video yig'ish). Skript ichidagi yo'llar (`../clips/e.mp4`, musiqa fayli) sessiyaga qarab moslashtiriladi.
- Gorizontal klipni 9:16 ga kesishda `crop x` ulushini klipga qarab sozlang (markaz ko'pincha kerakli obyektni kesib tashlaydi). Tayyor kadrni ko'rib tekshiring.
- Proksi CA: `/root/.ccr/ca-bundle.crt`. TLS tekshiruvini o'chirmang.
- Tayyor videoni yuborishdan oldin kamida bir nechta kadrni ko'zdan kechiring; faylni `SendUserFile` bilan yuboring va branchga commit/push qiling.
