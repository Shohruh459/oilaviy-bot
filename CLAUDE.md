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
| 2 | 10.10.2026 (shanba) | Diqqatni jamlashning 5 yo'li | tayyor: `yuksalish_diqqat.mp4` (2-shablon musiqa) |
| 3 | 11.10.2026 (yakshanba) | Kitob o'qishni odatga aylantirish | tayyor: `yuksalish_kitob.mp4` (3-shablon musiqa) |
| 4 | 12.10.2026 (dushanba) | Ertalabki 5 ta odat (ilm uchun) | TEST (ovozli, MMS-TTS): `yuksalish_ertalab.mp4`, foydalanuvchi ovoz sifatini tasdiqlaydi |
| 5 | 13.10.2026 (seshanba) | Imtihonga tayyorgarlik: 5 ta maslahat | kutilmoqda |
| 6 | 14.10.2026 (chorshanba) | Yangi til o'rganish: 5 ta sodda usul | kutilmoqda |
| 7 | 15.10.2026 (payshanba) | Vaqtni to'g'ri taqsimlash | kutilmoqda |
| 8 | 16.10.2026 (juma) | Charchaganda ham o'qishni davom ettirish | kutilmoqda |

Eslatma: `yuksalish_ilm.mp4` va `yuksalish_ilm_v2.mp4` — oyat/hadis bilan eski tajriba variantlari, jadvalga kirmaydi.

## Kontent uslubi

- Auditoriya: 15–40 yosh. **Faqat maslahatlar** formati.
- Ohang: yumshoq tavsiya ("shu usullar ko'proq samara beradi"), buyruq ohangi emas.
- Format: 1080×1920 (9:16), 25–35 soniya, o'zbek lotin, ekrandagi matn. Ovoz (TTS) hozircha faqat TEST rejimida (pastdagi "Ovoz (TTS)" bo'limi); foydalanuvchi sifatni tasdiqlamaguncha jadvaldagi videolar ovozsiz (faqat musiqa) tayyorlanadi.
- Tuzilma: hook (3–4s) → 5 ta maslahat (har biri ~5s) → CTA (5–6s).
- Matn pastki-markazda yarim shaffof qora panelda, sarlavha oq, "N-usul" va manba/urg'u oltin (`0xFFD54F`). Instagram interfeysi yopadigan pastki ~250px va yuqori qismni bo'sh qoldiring.
- Oxirgi CTA animatsiyali piktogrammalar bilan, videoga qarab tartibi: maslahat ro'yxati → **Saqlash** birinchi; hikoya/ilhom → **Ulashish** birinchi; doim **Obuna** ham bor. Piktogrammalar Pillow bilan chiziladi (sakrab chiqish + yengil pulsatsiya).
- **Instagram belgisi:** keyingi videolardan boshlab oxirgi kadrda `YUKSALISH` yozuvining yonida Instagram piktogrammasi bo'lsin (gradientli yumaloq kvadrat ichida kamera belgisi, Pillow bilan chiziladi, tashqi logo fayl kerak emas). Foydalanuvchi Instagram nomini (`@...`) bersa, yozuvni shunga almashtiring.
- **Kiyim va tana qoidasi:** klipda ayollarning yelkasi, qo'li va ko'kragi ochiq bo'lmasin. Yengsiz, ochiq yoki qisqa kiyimdagi ayollar tushgan klipni tanlamang. Yopiq kiyimdagi (kamida qisqa yeng, yopiq yoqa) odamlar, erkaklar, faqat qo'l/predmet, tabiat yoki multfilm kadrlarni tanlang. Har bir tanlangan klipning kadrini ko'rib tekshiring, 9:16 kesishdan keyin ham (kesish kadrni o'zgartiradi).
- **Ijod erkinligi:** foydalanuvchi mavzu, klip va musiqa tanlashda mustaqil ijod qilishga ruxsat bergan. Jadvaldagi mavzuga mos klip va shablonni o'zingiz tanlang, natijani va tanlovni qisqa tushuntiring.
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

Talab: so'zsiz (instrumental), kamida 40 soniya, `.mp3`.

**Musiqani o'zim ham topa olaman:** `freepd.com` (CC0) va `mixkit.co` (Mixkit bepul litsenziyasi, izoh shart emas) ochiq. Mixkit sahifasida (masalan `https://mixkit.co/free-stock-music/mood/calm/`) treklar JSON-LD ichida: nom, janr, davomiylik, to'g'ridan `https://assets.mixkit.co/music/<id>/<id>.mp3`. Tanlashni nom, janr, davomiylik bo'yicha qilaman, eshita olmayman, shuning uchun foydalanuvchi tasdiqlaydi. Pixabay Music sahifalari 403 beradi.

Foydalanuvchi 6 ta shablonning hammasini yuklab bergan, fayllar `reels/music/` da (Pixabay litsenziyasi):

| Shablon | Fayl | Davomiyligi |
|---|---|---|
| 1. Ilhom | `reels/music/1_ilhom_inspiring.mp3` | 2:38 |
| 2. Fokus | `reels/music/2_fokus_lofi_study.mp3` | 2:02 |
| 3. Ertalab | `reels/music/3_ertalab_sunny_morning_walk.mp3` | 2:28 |
| 4. Sokin | `reels/music/4_sokin_relaxing.mp3` | 1:12 |
| 5. Tezkor | `reels/music/5_tezkor_business_corporate.mp3` | 2:19 |
| 6. Vlog | `reels/music/6_vlog_the_vlog.mp3`, `reels/music/6_vlog_echoes_of_lumen.mp3` | 1:16, 0:57 |
| 3. Ertalab (qo'shimcha, Mixkit "Walking in the Park") | `reels/music/7_ertalab_walking_in_the_park_mixkit.mp3` | 1:35 |

Yig'ishda musiqa boshidan olinadi, 1s ichida paydo bo'ladi, oxirgi 3s da so'nadi. Shu bilan 1-video (`yuksalish_5_usul.mp4`) 6-shablon `echoes_of_lumen` bilan yig'ilgan.

## Ovoz (TTS) — o'zbek tili

- **Ishlaydigan yo'l:** Meta MMS-TTS, model `facebook/mms-tts-uzb-script_cyrillic` (Hugging Face). Model faqat **kirill** biladi; lotin matnni `reels/tts_uz.py` (`lat2cyr`) o'giradi. Rasmiy lotin modeli yo'q (`uzb-script_latin` mavjud emas).
- **Litsenziya: CC-BY-NC 4.0** (tijorat emas). Sahifa daromad keltirsa yoki reklama bo'lsa, ishlatishdan oldin foydalanuvchiga eslating.
- **Ishlamaydi:** Microsoft Edge TTS (`edge-tts`, `speech.platform.bing.com`): Microsoft bulut IP'laridan 403 beradi. Zaxira variant: Azure AI Speech (rasmiy API, `uz-UZ-SardorNeural` / `MadinaNeural`), uchun foydalanuvchi kalitni `AZURE_SPEECH_KEY` va `AZURE_SPEECH_REGION` sifatida muhitga qo'shadi va `<region>.tts.speech.microsoft.com` ruxsat etiladi.
- **Ruxsat etilgan domenlar** (muhit sozlamasida): `freepd.com`, `mixkit.co`, `assets.mixkit.co`, `huggingface.co`, `hf.co`, `us.aws.cdn.hf.co`.
- **O'rnatish (har yangi sessiyada qayta kerak bo'lishi mumkin, ~10 daqiqa, ~6 GB):** `pip install torch transformers scipy numpy`. Fonda ishga tushiring, tugashini `pgrep -f` bilan kutmang (buyruq o'zini topib qoladi); log faylga yozib, oxirgi qatorni tekshiring.
- **Model yuklash:** albatta `export HF_HUB_DISABLE_XET=1` (aks holda `cas-server.xethub.hf.co` bloklangani uchun xato). Model bir marta yuklanadi (~100 MB).
- **Ishlatish:** spetsifikatsiyaga har sahnaga `"say"` (matn) va `"voice"` (wav yo'li) qo'shing; `python3 -I reels/make_voice.py spec.json` ovozlarni yaratadi va kirill matnni chop etadi; `python3 -I reels/build_reel.py spec.json` videoni yig'adi (sahna davomiyligi = ovoz uzunligi + kechikish, musiqa ovoz paytida avtomatik pasayadi). `NOVOICE=1` ovozsiz variant beradi.
- **Matn qoidalari:** raqamlarni so'z bilan yozing ("o'ttiz", "o'n"), gaplarni qisqa tuting (har sahna 1 gap, 2–4 soniya; uzun gap videoni 50+ soniyaga cho'zadi), `speaking_rate` 1.1. Ekrandagi matn ovozdan batafsilroq bo'lishi mumkin.
- Talaffuzni men eshita olmayman: foydalanuvchi eshitib xato so'zlarni aytadi. Xatolarni imlo bilan tuzating (masalan so'zni boshqacha yozib) va shu yerga "Talaffuz tuzatishlari" sifatida yozib boring.

### Talaffuz tuzatishlari
(hozircha bo'sh; foydalanuvchi sinov natijasini aytgach to'ldiriladi)

## Texnik eslatmalar

- Klip manbai: Pixabay Videos API. Kalit `PIXABAY_API_KEY` muhit o'zgaruvchisida (hech qachon commit qilmang).
- Python `urllib` Pixabay'da 403 beradi; `curl` ishlaydi.
- Yig'ish: `ffmpeg` (drawtext, DejaVu Sans Bold — `'` va `–` belgilari to'g'ri chiqadi) + Pillow (CTA animatsiyasi). Skriptlar: `reels/fetch_clips.py` (nomzod klip qidirish va ko'rinishlar to'ri; `Q` lug'atidagi qidiruv so'zlarini mavzuga qarab o'zgartiring), `reels/build_reel.py` (umumiy yig'uvchi, matnli sahnalar + animatsiyali CTA + Instagram belgisi). Yangi video uchun `reels/specs/` ga JSON spetsifikatsiya yozing (`video2_diqqat.json` namunasi), klipni to'liq HD sifatda `clips/<nom>.mp4` ga yuklang, so'ng `python3 -I reels/build_reel.py reels/specs/<fayl>.json`. Oxirgi kadr fon klipi `clips/cta_bg.mp4` (quyosh chiqishi, Pixabay 153821).
- Gorizontal klipni 9:16 ga kesishda `crop x` ulushini klipga qarab sozlang (markaz ko'pincha kerakli obyektni kesib tashlaydi). Tayyor kadrni ko'rib tekshiring.
- Proksi CA: `/root/.ccr/ca-bundle.crt`. TLS tekshiruvini o'chirmang.
- Tayyor videoni yuborishdan oldin kamida bir nechta kadrni ko'zdan kechiring; faylni `SendUserFile` bilan yuboring va branchga commit/push qiling.
