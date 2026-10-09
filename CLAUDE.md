# Loyiha qoidalari

Bu repoda ikki narsa bor:
- **Telegram bot** (`bot.py`, `database.py`, `questions.py`): oilaviy bot.
- **Yuksalish Instagram reels**: ilm olishga targ'ib qiluvchi qisqa videolar (`yuksalish_*.mp4`; skriptlar, spetsifikatsiyalar, izohlar `reels/` da).

Quyidagi qoidalar Yuksalish uchun. Foydalanuvchi bilan o'zbek tilida (lotin) gaplashing, ijodiy qarorlarni o'zingiz qabul qiling va tanlovni qisqa tushuntiring.

## Har bir video bilan birga taqdim etiladi (majburiy)

Tayyor ro'yxat: `reels/captions.md`. Video yuborganda xabarda doim:
1. **Yuklash sanasi** `DD.MM.YYYY` + hafta kuni (quyidagi jadval).
2. **Izoh (caption)**: nusxa ko'chirishga tayyor, alohida kod blokida (hook savol, ro'yxat, saqlash/ulashish chaqirig'i, oxirgi qator `Yuksalish ilm bilan boshlanadi.`).
3. **Hashtaglar: roppa-rosa 3 ta**, `#yuksalish` birinchi.
4. **Fon musiqasi**: qaysi trek.

## Holat va yuklash jadvali (1 video = 1 kun)

**Hammasi 8 ta video tayyor, FEM2 ayol ovozida (Chatterbox), foydalanuvchiga yuborilgan.** Jadval o'zgarsa shu yerni yangilang.

| # | Sana | Mavzu | Fayl | Musiqa trek (`reels/music/` da bo'lishi kerak) |
|---|---|---|---|---|
| 1 | 09.10.2026 (juma) | Ilm olishning 5 usuli | `yuksalish_5_usul.mp4` | `6_vlog_echoes_of_lumen.mp3` |
| 2 | 10.10.2026 (shanba) | Diqqatni jamlash | `yuksalish_diqqat.mp4` | `2_fokus_lofi_study.mp3` |
| 3 | 11.10.2026 (yakshanba) | Kitob o'qishni odatga aylantirish | `yuksalish_kitob.mp4` | `3_ertalab_sunny_morning_walk.mp3` |
| 4 | 12.10.2026 (dushanba) | Ertalabki 5 odat | `yuksalish_ertalab.mp4` | `7_ertalab_walking_in_the_park_mixkit.mp3` |
| 5 | 13.10.2026 (seshanba) | Imtihonga tayyorgarlik | `yuksalish_imtihon.mp4` | `2_fokus_lofi_study.mp3` |
| 6 | 14.10.2026 (chorshanba) | Yangi til o'rganish | `yuksalish_til.mp4` | `6_vlog_the_vlog.mp3` |
| 7 | 15.10.2026 (payshanba) | Vaqtni taqsimlash | `yuksalish_vaqt.mp4` | `5_tezkor_business_corporate.mp3` |
| 8 | 16.10.2026 (juma) | Charchaganda ham davom etish | `yuksalish_charchoq.mp4` | `4_sokin_relaxing.mp3` |

Ochiq ishlar: foydalanuvchi Instagram nomini (`@...`) bermagan (CTA'dagi `YUKSALISH` yozuvini almashtiring); FEM2 namunasi haqiqiy odamniki (pastdagi huquqiy eslatma): ixtiyoriy ravishda rozi bergan ayolning 15–20 s yozuviga almashtirish; 8 kundan keyingi videolar uchun yangi mavzular rejasi.

## Kontent uslubi

- Auditoriya 15–40 yosh, **faqat maslahatlar**, yumshoq tavsiya ohangi, buyruq emas.
- 1080×1920, o'zbek lotin, ekrandagi matn + ovoz, ~35 s. Tuzilma: hook, 5 maslahat, CTA.
- Matn pastki-markazda yarim shaffof qora panelda; sarlavha oq, "N-usul"/urg'u oltin (`0xFFD54F`). Instagram interfeysi yopadigan yuqori va pastki ~250 px bo'sh.
- Oxirgi kadr: animatsiyali CTA piktogrammalari (Saqlash/Ulashish/Obuna; maslahat ro'yxatida Saqlash birinchi, hikoyada Ulashish birinchi) va `[Instagram belgisi] YUKSALISH`.
- **Kiyim va tana qoidasi:** ayollarning yelkasi, qo'li, ko'kragi ochiq klip yo'q. Yopiq kiyimdagi odamlar, erkaklar, qo'l/predmet, tabiat, multfilm. 9:16 kesishdan keyin ham kadrni ko'rib tekshiring.
- Ilmiy da'volarni umumiy tavsiya sifatida yozing, manbasiz raqam/foiz yozmang. Oyat/hadisni faqat foydalanuvchi matn va manbani tasdiqlagandagina qo'shing.

## Fon musiqasi

Musiqa fayllari **repodan o'chirilgan** (hajm ~25 MB; git tarixida `reels/music/` bor: `git log --diff-filter=D -- reels/music`, `git checkout <commit>^ -- reels/music`). Spetsifikatsiyalardagi `"music"` yo'li `/home/user/oilaviy-bot/reels/music/<trek>` ga ishora qiladi. Yangi video uchun trekni o'zingiz tanlang: `freepd.com` (CC0) yoki `mixkit.co` + `assets.mixkit.co` (izoh shart emas; mood sahifalarida treklar JSON-LD ichida: nom, janr, davomiylik, `assets.mixkit.co/music/<id>/<id>.mp3`) ochiq. Pixabay Music 403 beradi: foydalanuvchi o'zi yuklab beradi (so'zsiz, kamida 40 s, mp3). Mavzu shablonlari: Ilhom (hikoya), Fokus/lofi (diqqat, imtihon), Ertalab, Sokin (charchoq), Tezkor (vaqt), Vlog (umumiy, til). Men eshita olmayman: foydalanuvchi tasdiqlaydi. `build_reel.py` musiqani boshidan oladi, 1 s da kiritadi, oxirgi 3 s da so'ndiradi (**faqat musiqani**, ovozni emas), ovoz paytida avtomatik pasaytiradi.

## Ovoz: Chatterbox FEM2 (yagona rasmiy usul)

- Model: `UAzimov/Uzbek-tts-chatterbox` LoRA (MIT) + `ResembleAI/chatterbox` (MIT). Namuna ovoz: `reels/voice_ref/candidates/fleurs_female_2.wav` (FLEURS, CC BY 4.0), skript uni `refs/fem1.wav` (24 kHz) ga o'giradi. Natija: CER 0–7%, ovoz o'xshashligi 0.95–0.98, shimmer 7–9. Meta MMS (CC-BY-NC) usuli o'chirilgan (CER ~30%).
- **Bitta buyruq:** `CBWORK=<cbwork> python3 reels/chatterbox/make_video_cb.py reels/specs/videoN.json ISH_PAPKA [--cta-from cta.wav] [--lines s2,s3 | --improve 0.10]`. ISH_PAPKA ichida `clips/<nom>.mp4` (to'liq HD Pixabay klip) va `clips/cta_bg.mp4` (quyosh chiqishi, Pixabay 153821) bo'lsin. U: har gap uchun 4 seed (`NOSPLIT=1`, butun gap bir o'tishda) → ASR+shimmer+ohang bo'yicha tanlash → spetsifikatsiyani yangilash → `build_reel.py`. `--cta-from`: CTA ovozi hamma videoda bir xil, bir marta yaratilib qayta ishlatiladi. CER > 10% gaplar uchun `--lines`/`--improve` (8 yangi seed). Hisobot: `ISH_PAPKA/_sel_report.json`.
- Spetsifikatsiya: sahnalar (`clip`, `dur`, `xfrac`, `start`, `top`, `lines`, `say`), `cta` (`order`, `say`, `bg`), `music`, `voice_delay`, `voice_tail` (0.6). `say` matnida raqamlar so'z bilan, ASCII apostrof; ekrandagi matn ovozdan batafsilroq bo'lishi mumkin. Qiyin so'zni ovozda soddaroq so'z bilan almashtiring ("maqsadingizni" → "orzuingizni"). Gorizontal klipni 9:16 ga kesishda `xfrac` ni sozlang; kalendar klipida qisqa oylar uchun `"start": 3.3`.
- **Saboqlar:** gapni `:.?!` bo'yicha bo'laklash Chatterbox'da ovozni uzadi (ishlatmang); ovoz balandligini siljitmang, `loudnorm` ishlatmang (shimmerni oshirib "bo'g'ilgan" qiladi), faqat statik kuchaytirish; `alimiter=limit=0.89:level=false` (level=false shart); yig'ilgan audio ~ -17…-18 dB o'rtacha, cho'qqi ~ -1 dB; tekshiruv: 0.5 s oynalarda mix/ovoz energiya nisbati ~1.0 (so'nmasin).
- Tekshirish: `reels/hear.py` (ASR `facebook/mms-1b-all`, adapter `uzb-script_latin`, CER; WavLM o'xshashlik; kalibrovka FLEURS CER 6%), `reels/voice_match.py` (Praat shimmer: yaxshi 7–11%, 14%+ "bo'g'ilgan"). Tembr/mfcc taqqoslash noto'g'ri mezon.
- Klip qidirish: `reels/fetch_clips.py` (`Q` ni o'zgartiring, nomzod kadrlar to'ri). Tayyor videoning kadrlarini ko'zdan kechiring, `SendUserFile` bilan yuboring, commit/push qiling.

### Huquqiy eslatma (foydalanuvchiga ayting)
Namuna ovozlar haqiqiy odamlarniki. FLEURS (anonim ko'ngillilar, CC BY 4.0) xavfi kam, lekin nolga teng emas; izohga "Ovoz namunasi: FLEURS (Google), CC BY 4.0" qo'shish mumkin. Abduqayum repodagi `reference_voice.wav` (audiokitob diktori, roziligi noaniq) **ishlatilmasin**. Eng toza yo'l: rozi bergan ayolning 15–20 s yozuvi. Men yurist emasman.

## Yangi sessiyada muhitni tiklash (~20–30 daqiqa, ~13 GB disk, 15 GB RAM)

1. Domenlar ruxsat etilgan bo'lsin: `huggingface.co`, `hf.co`, `us.aws.cdn.hf.co`, `freepd.com`, `mixkit.co`, `assets.mixkit.co`, PyPI; `raw.githubusercontent.com` ochiq, `github.com` yopiq. Pixabay: `PIXABAY_API_KEY` (commit qilmang; `urllib` 403 beradi, `curl` ishlating).
2. Har doim `export HF_HUB_DISABLE_XET=1`.
3. Sistema Python: `pip install torch transformers scipy numpy librosa praat-parselmouth soundfile pillow` (ASR/tahlil/yig'ish), `ffmpeg` bor.
4. Chatterbox: `uv venv --python 3.11 cbenv`; `uv pip install chatterbox-tts silero-vad "peft==0.17.1" num2words "setuptools<81" "transformers==4.46.3" "tokenizers<0.21"`; `cbwork/` ichida `python3 reels/chatterbox/crawl_toolkit.py` (toolkitni `raw.githubusercontent.com` dan oladi) va `reels/chatterbox/download_models.sh` (asos vaznlar + UAzimov adapteri `uz_uaz/`). VAD yuklash xatosi zararsiz.
5. Bir vaqtda faqat bitta og'ir jarayon (ikkitasi xotirani to'ldirib 3 s/token gacha sekinlashtiradi). Fonda ishga tushiring; tugashini `pgrep -f` bilan emas, log/flag fayl bilan kuting. Disk cheklangan: ish tugagach `cand/`, oraliq wav va eski mp4 nusxalarni o'chiring.
6. Proksi CA: `/root/.ccr/ca-bundle.crt`; TLS tekshiruvini o'chirmang. `ffmpeg` drawtext uchun DejaVu Sans Bold.
