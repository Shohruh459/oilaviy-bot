# Loyiha qoidalari

Bu repoda ikki narsa bor:
- **Telegram bot** (`bot.py`, `database.py`, `questions.py`): oilaviy bot.
- **Yuksalish Instagram reels**: ilm olishga targ'ib qiluvchi qisqa videolar (`yuksalish_*.mp4`, skriptlar va ma'lumotlar `reels/` papkasida).

Quyidagi qoidalar Yuksalish videolari uchun. Foydalanuvchi bilan o'zbek tilida (lotin) gaplashing, ijodiy qarorlarni o'zingiz qabul qiling va tanlovni qisqa tushuntiring.

## Har bir video bilan birga taqdim etiladi (majburiy)

Video faylni yuborganda xabarda doim shular bo'lsin (tayyor ro'yxat: `reels/captions.md`):

1. **Yuklash sanasi**: `DD.MM.YYYY` va hafta kuni (quyidagi jadvaldan).
2. **Izoh (caption)**: nusxa ko'chirishga tayyor, alohida kod blokida (hook savol, ro'yxat, saqlash/ulashish chaqirig'i, oxirgi qator `Yuksalish ilm bilan boshlanadi.`).
3. **Hashtaglar: roppa-rosa 3 ta**, `#yuksalish` birinchi.
4. **Fon musiqasi**: qaysi shablon ishlatilgani.

## Yuklash jadvali (kunlik, 1 video = 1 kun)

| # | Sana | Mavzu | Fayl | Musiqa |
|---|---|---|---|---|
| 1 | 09.10.2026 (juma) | Ilm olishning 5 ta samarali usuli | `yuksalish_5_usul.mp4` | 6 (Echoes of Lumen) |
| 2 | 10.10.2026 (shanba) | Diqqatni jamlashning 5 yo'li | `yuksalish_diqqat.mp4` | 2 |
| 3 | 11.10.2026 (yakshanba) | Kitob o'qishni odatga aylantirish | `yuksalish_kitob.mp4` | 3 |
| 4 | 12.10.2026 (dushanba) | Ertalabki 5 ta odat | `yuksalish_ertalab.mp4` | Mixkit "Walking in the Park" (7) |
| 5 | 13.10.2026 (seshanba) | Imtihonga tayyorgarlik | `yuksalish_imtihon.mp4` | 2 |
| 6 | 14.10.2026 (chorshanba) | Yangi til o'rganish | `yuksalish_til.mp4` | 6 (The Vlog) |
| 7 | 15.10.2026 (payshanba) | Vaqtni to'g'ri taqsimlash | `yuksalish_vaqt.mp4` | 5 |
| 8 | 16.10.2026 (juma) | Charchaganda ham davom etish | `yuksalish_charchoq.mp4` | 4 |

Holat: 8 ta video ovozli (Meta MMS ovozi) tayyor. **Foydalanuvchi FEM2 ayol ovozini tanladi** (`reels/voice_ref/candidates/fleurs_female_2.wav`, Chatterbox UAzimov). **1-video shu ovozda qayta yig'ildi** (`yuksalish_5_usul.mp4`, 39 s); 2–8-videolar hali Meta ovozida: foydalanuvchi 1-videoni tasdiqlagach qolganlarini ham shu usulda qayta yig'ing (pastdagi "Chatterbox jarayoni").

## Kontent uslubi

- Auditoriya 15–40 yosh. **Faqat maslahatlar.** Ohang yumshoq tavsiya, buyruq emas.
- Format: 1080×1920 (9:16), o'zbek lotin, ekrandagi matn + ovoz. Davomiylik ovozga qarab ~35–38 soniya. Tuzilma: hook, 5 maslahat, CTA.
- Matn paneli ekran pastki-markazida, yarim shaffof qora; sarlavha oq, "N-usul" va urg'u oltin (`0xFFD54F`). Instagram interfeysi yopadigan yuqori va pastki ~250 px bo'sh.
- Oxirgi kadr: animatsiyali CTA piktogrammalari (Saqlash, Ulashish, Obuna; maslahat ro'yxatida Saqlash birinchi, hikoyada Ulashish birinchi) va `[Instagram belgisi] YUKSALISH`. Foydalanuvchi Instagram nomini (`@...`) bersa, yozuvni shunga almashtiring (hali bermagan).
- **Kiyim va tana qoidasi:** ayollarning yelkasi, qo'li, ko'kragi ochiq klip yo'q. Yopiq kiyimdagi odamlar, erkaklar, qo'l/predmet, tabiat, multfilm kadrlarni tanlang. 9:16 kesishdan keyin ham kadrni ko'rib tekshiring.
- Ilmiy da'volarni umumiy tavsiya sifatida yozing, manbasiz raqam/foiz yozmang. Oyat va hadisni faqat foydalanuvchi matn va manbani tasdiqlagandagina qo'shing (manbani kichik yozuv bilan).

## Fon musiqasi

6 shablon (Pixabay Music, foydalanuvchi yuklagan) `reels/music/` da: 1 Ilhom, 2 Fokus (lofi), 3 Ertalab, 4 Sokin, 5 Tezkor, 6 Vlog (2 ta), 7 Mixkit "Walking in the Park". Mavzuga mos shablonni o'zingiz tanlang. Musiqani internetdan ham topa olasiz: `freepd.com` (CC0) va `mixkit.co` (+`assets.mixkit.co`, izoh shart emas) ochiq; Mixkit mood sahifalarida (masalan `/free-stock-music/mood/calm/`) treklar JSON-LD ichida (nom, janr, davomiylik, `assets.mixkit.co/music/<id>/<id>.mp3`). Pixabay Music sahifalari 403 beradi. Men eshita olmayman: foydalanuvchi musiqani tasdiqlaydi. Yig'ishda musiqa boshidan olinadi, 1 s da kiradi, oxirgi 3 s da so'nadi, ovoz paytida avtomatik pasayadi.

## Ovoz (TTS)

### Hozirgi rasmiy videolar: Meta MMS ("A varianti")
- Model `facebook/mms-tts-uzb-script_cyrillic` (CC-BY-NC 4.0: tijoratga emas), faqat kirill biladi; lotin matnni `reels/tts_uz.py` kirillga o'giradi. Tokenizatorda tinish belgilari yo'q, shuning uchun matn `:.?!` bo'yicha bo'laklanib, orasiga aniq pauza qo'yiladi (`"tts": {"split_on": ":.?!"}` spetsifikatsiyada).
- Seed tanlash: `reels/make_voice.py` + `voice_match.py` (shimmer/ohang bo'yicha namuna `reels/voice_ref/ref_tavsiya.wav` ga yaqin), `improve_voice.py` (ASR yordamida eng yomon gaplar). **Balandlikni siljitmang va `loudnorm` ishlatmang**: shimmerni oshirib, ovozni "bo'g'ilgan" qiladi. Faqat statik kuchaytirish.
- Chegarasi: harf xatosi o'rtacha 25–34%, unlilarning ~35% i yutiladi (tabiiy nutqda 6%). Qiyin so'zni ovozda soddaroq so'z bilan almashtirish yordam beradi ("maqsadingizni" -> "orzuingizni").

### Yangi yo'nalish: Chatterbox o'zbek (MIT), sinovdan o'tgan
- Modellar: `UAzimov/Uzbek-tts-chatterbox` (LoRA, 111 soat ko'p ovozli ruxsatli korpus; **tavsiya**), `Abduqayum/uzbek-tts-natural-speech-chatterbox` (30 soat bitta diktor). Asos `ResembleAI/chatterbox` (MIT).
- ASR natijasi (7 gap): Meta A CER 28% / unlilar 69%; UAzimov CER 10% / 99%. **FLEURS ayol namunasi** (`reels/voice_ref/candidates/fleurs_female_2.wav`) bilan CER ~1%, shimmer 7.6, ohang ~14 yarim ton (ayol ovozi). Namunasiz standart ovoz CER 8%; Meta ovozini namuna qilib klonlash aniqlikni pasaytiradi.
- **Foydalanuvchi ayol ovozini afzal ko'rdi.** Nomzod namunalar `reels/voice_ref/candidates/` (README: asl fayl ID, litsenziya). Tanlov foydalanuvchi tinglab tasdiqlashini kutadi.
- Ishga tushirish: `reels/chatterbox/` (`crawl_toolkit.py` toolkitni `raw.githubusercontent.com` dan oladi, `download_models.sh`, `gen_refs.py <namuna.wav|none[,...]> lines.json chiqish_papkasi`). Python 3.11 venv: `uv venv --python 3.11 cbenv`; `uv pip install chatterbox-tts silero-vad "peft==0.17.1" num2words "setuptools<81"`, so'ng `transformers==4.46.3` va `tokenizers<0.21` (toolkit eski transformers uchun). Matnda ASCII apostrof, raqamlarni so'z bilan. Bir gap CPU'da 5–10 s. VAD yuklash xatosi zararsiz.
- **Chatterbox jarayoni (rasmiy, FEM2 ovozi), 1-videoda sinalgan:** (1) cbwork papkasida venv ichida `python gen_voice_cb.py spec.json refs/fem1.wav cand_vN 4` (har gap 4 seed, matn `:.?!` bo'yicha bo'laklanib orasiga pauza qo'yiladi); (2) sistema Python'da `python3 reels/chatterbox/select_voice_cb.py spec.json cand_vN voice_cb yangi_spec.json` (ASR + shimmer + ohang birligi bo'yicha tanlash; natija 1-videoda CER 0–4%, ovoz o'xshashligi 0.97); (3) ovozni `ffmpeg -af atempo=1.1` bilan tezlashtirish (`voice_cb_fast/`; CER ~3.5%, shimmer o'zgarmaydi), spetsifikatsiyada `"voice_tail": 0.6`; (4) `build_reel.py yangi_spec.json`. Natija ~39 s. `say` matnlari Meta uchun soddalashtirilgan edi: Chatterbox'da asl (ekrandagi matnga yaqin) so'zlarni ishlatish mumkin. Spetsifikatsiya namunasi: `reels/specs/video1_5_usul_cb.json`.
- Izohga ixtiyoriy manba: "Ovoz namunasi: FLEURS (Google), CC BY 4.0": foydalanuvchi hal qiladi.
- Tez-tez uchraydigan xato: ikkita generatsiya jarayoni bir vaqtda (xotira 15 GB) 3 s/token gacha sekinlashadi. Bittadan ishga tushiring.

### Huquqiy eslatmalar (foydalanuvchiga ayting)
- Meta MMS: CC-BY-NC (tijorat emas). Chatterbox, UAzimov, Abduqayum: MIT. Mixkit/FreePD: erkin litsenziya.
- **Namuna ovozlar haqiqiy odamlarniki.** Tanilgan yoki aniq odam ovozini roziligisiz klonlash (hatto foydali kontent bo'lsa ham) shaxsiy huquqlarga tegishi mumkin. Abduqayum repodagi `reference_voice.wav` audiokitob diktorining ovozi: roziligi noaniq, **ishlatmang**. FLEURS (CC BY 4.0, anonim ko'ngillilar) xavfi kam, lekin nolga teng emas va mualliflik ("FLEURS, Google, CC BY 4.0") ko'rsatilishi kerak. Eng toza yo'l: o'zi rozi bergan odam (masalan foydalanuvchining yaqini) 15–20 soniya yozib berishi, yoki namunasiz standart ovoz. Men yurist emasman: katta rejalar bo'lsa mutaxassisga murojaat qiling.

### ASR bilan tekshirish (eshitish o'rniga)
- `reels/hear.py spec.json`: Meta `mms-1b-all` (uzb-script_latin adapteri, ~4 GB) ovozni matnga aylantirib CER va unlilar saqlanishini, WavLM (`wavlm-base-plus-sv`) bilan gaplarning bir odamga o'xshashligini o'lchaydi. Kalibrovka: tabiiy o'zbek nutqi (FLEURS) CER 6%, unlilar 97%. Ovoz egasi o'xshashligi < 0.85 bo'lgan gap chetga chiqqan.
- Shimmer (Praat) ovoz "bo'g'ilganligi"ning ishonchli ko'rsatkichi: yaxshi 9–11%, bo'g'ilgan 14%+. Tembr/mfcc taqqoslash noto'g'ri mezon.

## Videoni yig'ish (Meta A jarayoni)

`reels/specs/*.json` (sahnalar, matn, `say`/`voice`, musiqa, CTA tartibi). Ishchi papkada `clips/<nom>.mp4` (to'liq HD Pixabay klip, `clips/cta_bg.mp4` = quyosh chiqishi, Pixabay 153821):
1. `python3 -I reels/make_voice.py spec.json` (ovozlar, `voice/`).
2. `python3 -I reels/improve_voice.py spec.json 0.40 --skip cta` (ixtiyoriy, ASR bilan yomon gaplarni yaxshilash).
3. `python3 -I reels/build_reel.py spec.json` (video; `NOVOICE=1` ovozsiz). Audio `alimiter=limit=0.89:level=false`; yig'ishdan keyin o'rtacha ovoz ~ -18 dB, cho'qqi ~ -1.4 dB bo'lsin.

Klip qidirish: `reels/fetch_clips.py` (`Q` ni o'zgartiring; nomzod kadrlar to'ri). Gorizontal klipni 9:16 ga kesishda `xfrac` ni klipga qarab sozlang. Kalendar klipida oy nomi har soniya almashadi: qisqa oylar uchun `"start": 3.3`. Tayyor kadrlarni ko'zdan kechiring, so'ng `SendUserFile` bilan yuboring va commit/push qiling.

## Server va muhit

- Pixabay kaliti `PIXABAY_API_KEY` (hech qachon commit qilmang). Python `urllib` Pixabay'da 403 beradi: `curl` ishlating. Ruxsat etilgan domenlar: `huggingface.co`, `hf.co`, `us.aws.cdn.hf.co`, `freepd.com`, `mixkit.co`, `assets.mixkit.co`, PyPI; `raw.githubusercontent.com` ochiq, `github.com` yopiq. Edge TTS (`speech.platform.bing.com`) 403; Azure TTS karta talab qiladi (foydalanuvchi xohlamaydi).
- Hugging Face yuklashda **`export HF_HUB_DISABLE_XET=1`** shart.
- Sistema Python'da: `torch transformers scipy numpy librosa praat-parselmouth soundfile` (Meta TTS, ASR, tahlil). Yangi sessiyada qayta o'rnatish ~10 daqiqa, ~6 GB; fonda ishga tushiring, tugashini `pgrep -f` bilan emas, log/`done` fayl bilan kuting (pgrep buyruqning o'zini topadi).
- Disk cheklangan (~10–15 GB bo'sh): venv (6 GB), Chatterbox vaznlari (4 GB), `mms-1b-all` (3.9 GB). Ish tugagach oraliq fayllarni (`ov/`, `seg/`, `txt/`, arxivlar) o'chiring.
- Proksi CA: `/root/.ccr/ca-bundle.crt`; TLS tekshiruvini o'chirmang. `ffmpeg` drawtext uchun DejaVu Sans Bold ishlating.
