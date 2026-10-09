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
| 1 | 09.10.2026 (juma) | Ilm olishning 5 ta samarali usuli | OVOZLI tayyor: `yuksalish_5_usul.mp4` |
| 2 | 10.10.2026 (shanba) | Diqqatni jamlashning 5 yo'li | OVOZLI tayyor: `yuksalish_diqqat.mp4` |
| 3 | 11.10.2026 (yakshanba) | Kitob o'qishni odatga aylantirish | OVOZLI tayyor: `yuksalish_kitob.mp4` |
| 4 | 12.10.2026 (dushanba) | Ertalabki 5 ta odat (ilm uchun) | OVOZLI tayyor: `yuksalish_ertalab.mp4` |
| 5 | 13.10.2026 (seshanba) | Imtihonga tayyorgarlik: 5 ta maslahat | OVOZLI tayyor: `yuksalish_imtihon.mp4` |
| 6 | 14.10.2026 (chorshanba) | Yangi til o'rganish: 5 ta sodda usul | OVOZLI tayyor: `yuksalish_til.mp4` |
| 7 | 15.10.2026 (payshanba) | Vaqtni to'g'ri taqsimlash | OVOZLI tayyor: `yuksalish_vaqt.mp4` |
| 8 | 16.10.2026 (juma) | Charchaganda ham o'qishni davom ettirish | OVOZLI tayyor: `yuksalish_charchoq.mp4` |

Eslatma: `yuksalish_ilm.mp4` va `yuksalish_ilm_v2.mp4` — oyat/hadis bilan eski tajriba variantlari, jadvalga kirmaydi.

## Kontent uslubi

- Auditoriya: 15–40 yosh. **Faqat maslahatlar** formati.
- Ohang: yumshoq tavsiya ("shu usullar ko'proq samara beradi"), buyruq ohangi emas.
- Format: 1080×1920 (9:16), 25–35 soniya, o'zbek lotin, ekrandagi matn. Rasmiy videolar OVOZLI (TTS, A varianti, pastdagi "Ovoz (TTS)" bo'limi), foydalanuvchi tasdiqlagan. Davomiylik ovozga qarab ~35–40 soniya. Tayyor izoh/sana/hashtag/musiqa jadvali: `reels/captions.md`.
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

### Ovoz birligi (foydalanuvchi fikri bo'yicha)
- Birinchi testda foydalanuvchi: 4-gap ("To'rtinchi: o'n daqiqa kitob o'qing.", seed 555, tezlik 1.1) eng yoqdi; boshqa gaplar unga o'xshamadi ("hammasi bir xil ovoz emas"), 4-gap "haddan tashqari professional" eshitildi. Shu gap **standart ovoz** deb qabul qilindi: `reels/voice_ref/ref_tavsiya.wav`.
- Sababi: VITS tasodifiy (seed) va gap matniga qarab ohang beradi; gaplar orasida ~2 yarim ton balandlik farqi bor (tasodifdan emas, matn naqshidan).
- 2-test fikri: 3 va 5-usul "tomog'ini ataylab bo'g'ib gapirgan odamdek" eshitildi; 1, 2, 4-usul bir-biriga yaqin. Praat o'lchovi (parselmouth) buni tasdiqladi: yomon gaplarda **shimmer 14–15%**, yaxshilarida 10–11%.
- **Sabab (mening xatoyim):** balandlikni siljitish (`rubberband`, formant saqlangan variant ham) shimmerni 2–5 punktga oshirib, ovozni "bo'g'ilgan" qildi (xom sintezda shimmer hamma gapda 10–12% edi). **Balandlikni siljitmang. `loudnorm` ham ishlatmang** (dinamik kuchaytirish). Faqat statik kuchaytirish (RMS tenglash).
- Hozirgi usul (`reels/voice_match.py`, `make_voice.py` avtomatik qo'llaydi): har gapdan 16 ta seed yaratiladi, **shimmer (asosiy)** va ohang balandligi/o'zgarishi namunaga eng yaqini tanlanadi, siljitishsiz; ovoz balandligi statik kuchaytirish bilan tenglanadi. Namuna gap uchun spetsifikatsiyada `"seed": 555`. Natija: hamma gapda shimmer 9.5–10.5%.
- Cheklov: bu obyektiv o'lchov; men eshita olmayman, so'nggi hukm foydalanuvchiniki. Tembr harflar tarkibiga bog'liq (mfcc/spektral markaz bilan taqqoslash noto'g'ri mezon, ishlatmang). Shimmer yagona tasdiqlangan ajratuvchi o'lchov (jitter ajratmadi).

### Ovozni "eshitish" (ASR) va aniqlangan muammolar
- `reels/hear.py`: ovoz faylni ASR (Meta `facebook/mms-1b-all`, adapter `uzb-script_latin`, ~4 GB, CC-BY-NC) bilan matnga aylantirib, aytilishi kerak matn bilan solishtiradi (harf xatosi CER, so'z farqlari), WavLM x-vector (`microsoft/wavlm-base-plus-sv`) bilan gaplarning bir odamga o'xshashligini o'lchaydi. `HF_HUB_DISABLE_XET=1` shart; model yuklash ~10 daqiqa. Ishlatish: `python3 reels/hear.py spec.json`.
- **ASR kalibrovkasi:** tabiiy o'zbek nutqida (FLEURS, 20 ta) CER **6.4%**, unlilar saqlanishi **96.8%**. Shuning uchun TTS natijasidagi katta CER/unli yo'qotishi haqiqiy kamchilik (ASR xatosi emas).
- **Asosiy Meta TTS modeli (kirill):** CER ~30–35%, unlilarning ~54% i xolos saqlanadi, ya'ni "harflarni yutib o'qiydi" (foydalanuvchi shuni sezgan). Ovoz egasi bo'yicha hamma gaplar bir odam (x-vector 0.87–0.98); "boshqa-boshqa odam" tuyulishi ritm/ohang uslubi farqidan.
- **Tinish belgilari:** TTS tokenizatorida vergul, nuqta, so'roq, ikki nuqta YO'Q (faqat harflar, bo'shliq, `–`, `—`, raqamlar 0–6). Shu sabab pauza va so'roq ohangi bo'lmagan, hamma gap tekis pasayib tugagan ("buyruq bergandek"). `tts_uz.synth(pauses=True)` matnni tinish belgilari bo'yicha bo'laklarga bo'lib, orasiga jimlik qo'yadi; `chunk_words=3` yana mayda bo'laklaydi. Unlilar saqlanishi 54% -> 68–72%.
- **Qo'shimcha sozlamalar:** `noise_scale`, `noise_scale_duration`, `lowpass_hz` (`tts_uz.synth` parametrlari). Tezlik/shovqin sozlamalari asosiy modelda deyarli ta'sir qilmadi.
- **Hamjamiyat modeli** `MuzaffarSharofitdinov/mms-tts-uzbek-finetuned` (asos: Meta modeli, Common Voice o'zbek ma'lumotida fine-tune; litsenziyasi ko'rsatilmagan, asos NC bo'lgani uchun tijoratga ishlatmang): tavsiya sozlamalari `noise_scale=0.1`, `noise_scale_duration=0.5`, `length_scale 1.2`, `lowpass 7000 Hz`. CER **9–13%**, unlilar **95–98%** (tabiiy nutqqa yaqin), lekin **shimmer 16–18%** (asosiy modelda 9–10%). Shimmer yuqori bo'lsa ovoz "bo'g'ilgan" eshitilishi mumkin: A/B/C tinglash natijasini foydalanuvchi hal qiladi.
- **Variantlar (A tanlandi, quyidagi bo'limga qarang):** A) asosiy model + bo'laklash (toza ovoz, lekin harflar yutiladi); C) fine-tune model (harflar aniq, lekin ovoz sifati pastroq bo'lishi mumkin); D) Azure AI Speech Sardor/Madina (eng ishonchli, kalit kerak). CTA matni buyruq ohangini yumshatish uchun shartli shaklda yozildi: "Foydali bo'ldimi? Saqlab qo'ysangiz, keyin kerak bo'ladi. Obuna bo'lsangiz, xursand bo'lamiz."

### Qaror va "Nchi" pauzasi (foydalanuvchi qarori)
- **Qaror:** foydalanuvchi karta qo'shmaydi (Azure yo'q). A/B/C tinglashdan **A variantini** tanladi: asosiy Meta modeli (`facebook/mms-tts-uzb-script_cyrillic`), standart shovqin sozlamalari, `speaking_rate` 1.1, `chunk_words` yo'q, namuna ovoz bo'yicha seed tanlash (`voice_match.py`). B (qisqartirilgan shovqin + 3 so'zlik bo'laklash) va C (fine-tune) tanlanmadi.
- **Kamchilik (foydalanuvchi sezgan):** "Birinchi", "Ikkinchi" kabi tartib so'zi va undan keyingi gap orasida pauza yo'q, ular bitta so'zdek o'qilgan (ikki nuqta tokenizatorda yo'q). **Yechim:** spetsifikatsiyada `"tts": {"split_on": ":.?!"}`; matn shu belgilar bo'yicha bo'linadi, bo'laklar alohida o'qiladi, chetidagi jimlik kesiladi (`_trim_silence`), orasiga aniq pauza qo'yiladi (`:` 0.28s, `.` `!` 0.38s, `?` 0.42s). Vergul bo'yicha bo'linmaydi (A ovozi saqlanishi uchun). O'lchangan natija: "Nchi" dan keyin ~0.31–0.33s pauza.
- ASR bo'yicha (A + pauza): unlilar saqlanishi yaxshilandi (1 va 2-usul CER 14%), lekin 3, 4, 5-usul 26–32%, kirish va CTA 43–45%: asosiy Meta modeli harflarni yutishi saqlanib qoladi (bu uning chegarasi, Azure bo'lmasa yaxshilab bo'lmaydi). Gaplar orasidagi ovoz egasi o'xshashligi 0.93–0.99.
- Sinov/yig'ish: `make_voice.py` va `build_reel.py` ni spetsifikatsiya bilan ishga tushirish; tugash kutish uchun `pgrep -f` ishlatmang (o'zini topadi): log faylga `FINISHED` yozdirib, `grep -q` bilan kuting.

### Ovozni yaxshilash jarayoni (rasmiy videolar uchun qo'llangan)
- Birinchi o'tish: `make_voice.py` (shimmer/ohang bo'yicha seed). Ikkinchi o'tish: `reels/improve_voice.py spec.json 0.40 --skip cta`: ASR bo'yicha CER >= 40% gaplar uchun 24 seed sinab, ASR-yordamli (kam CER + ovoz oynasi) tanlash; CTA matni barcha videolarda bir xil (CER 43%, o'zgartirilmadi).
- Qiyin so'zlarni ovozda soddaroq so'z bilan almashtirish ASR'ni 50–80% dan 17–32% gacha tushiradi (masalan "maqsadingizni" -> "orzuingizni", "tekshiring" -> "sinang"). Ekrandagi matn ovozdan boshqacha bo'lishi mumkin, lekin ma'no mos tushsin.
- Ovoz egasi chetga chiqqan gap (x-vector o'rtacha < 0.85) uchun: 30 seed sinab, boshqa gaplar markaziga o'xshashlik va CER bo'yicha tanlash (6-video 2-usul misolida 0.82 -> 0.94).
- Audio: `alimiter=limit=0.89:level=false` (level=false shart; aks holda cho'qqi 0 dB ga ko'tariladi). O'rtacha ovoz balandligi ~ -18 dB, cho'qqi ~ -1.4 dB; eski videolarda audio keyin `volume=-1.5dB` bilan tuzatilgan.
- Yakuniy ASR (8 video): o'rtacha CER 25–34% (tabiiy nutqda 6%), eng yomon gap CER ~43% (CTA). Bu asosiy Meta modelining chegarasi.

### Boshqa bepul o'zbek TTS nomzodlari (tadqiq, hali sinalmagan)
- **Chatterbox o'zbek LoRA** (MIT; kod PyPI `chatterbox-tts`, asos `ResembleAI/chatterbox` HF, MIT): `UAzimov/Uzbek-tts-chatterbox` (111 soat ko'p ovozli ruxsatli korpus, lotin yozuv, CPU'da ishlaydi, nomukammal ravonlik), `Abduqayum/uzbek-tts-natural-speech-chatterbox` (30 soat bitta diktor audiokitob, birlashtirilgan T3 vazni + `inference.py`, ovoz klonlash). Qo'shimcha domen kerak emas (HF + PyPI). Audiokitob diktori ovozi/huquqlari noaniq: ehtiyot bo'ling.
- **Navoiy TTS** (`aisha-org/navoiy-tts`, Apache-2.0, CosyVoice2-0.5B asosida, 600 soat neytral + 40 soat ifodali, ovoz klonlash): faqat LLM checkpoint (1.88 GiB), ishlashi uchun `github.com/FunAudioLLM/CosyVoice` kodi kerak (`github.com` va `codeload.github.com` hozir 403; `raw.githubusercontent.com` ochiq) va `FunAudioLLM/CosyVoice2-0.5B` (HF).
- Coqui XTTS va Piper'da tayyor o'zbek ovozi topilmadi. Ma'lumotlar: ISSAI USC (CC BY 4.0, 105 soat), `aisha-org/uzbek-tts-corpus-v1`.
- Sinash usuli: shu hujjatdagi ASR (`hear.py`) o'lchovlari (CER, unlilar, shimmer, ovoz egasi) bilan A variantiga solishtirish.

### Chatterbox o'zbek (yangi nomzod, sinovdan o'tgan; qaror kutilmoqda)
- **Natija (ASR, 7 gap):** A (Meta) CER 28%, unlilar 69%; `ABD` (Abduqayum) CER 13%, unlilar 97%; `UAZ` (UAzimov LoRA) CER **10%**, unlilar **99%**, shimmer 9.0, ovoz o'xshashligi 0.96. Namuna ovozga qarab: diktor namunasi (audiokitob) ohang ~12 yarim ton (yuqori, ayol ovozi), FLEURS erkak namuna CER 17% shimmer 11.9, **standart ovoz (namunasiz, `conds.pt`, MIT) CER 8%, shimmer 11.1, ohang 5.7** (A ovozi ~4.4). Hozirgi Meta ovozini namuna qilib klonlash aniqlikni pasaytiradi (CER 20–33%).
- **Litsenziya:** Chatterbox va ikkala o'zbek LoRA MIT (tijoratga ruxsat). Namuna ovozlar: audiokitob diktori va FLEURS ovozlari haqiqiy odamlarniki, ularning roziligi/shartlari noaniq: **standart ovoz (namunasiz)** yoki o'zi rozi bergan odam ovozi afzal.
- **Sozlash (`reels/chatterbox/`):** Python 3.11 venv (`uv venv --python 3.11 cbenv`), `uv pip install chatterbox-tts silero-vad "peft==0.17.1" num2words "setuptools<81"`, so'ng **`transformers==4.46.3` va `tokenizers<0.21`** (toolkit eski transformers uchun yozilgan). `github.com` bloklangan, lekin `raw.githubusercontent.com` ochiq: `crawl_toolkit.py` `gokhaneraslan/chatterbox-finetuning` fayllarini import zanjiri bo'yicha yuklaydi (`src/`). `download_models.sh` asos Chatterbox vaznlari (`ResembleAI/chatterbox`: ve, t3_cfg, s3gen, conds, tokenizer=`grapheme_mtl_merged_expanded_v1.json`) va o'zbek fayllarni (`UAzimov/Uzbek-tts-chatterbox` adapter, `Abduqayum/...` merged T3 + reference_voice.wav) yuklaydi. Disk ~10 GB kerak (venv 6 GB + vaznlar 4 GB).
- **Ishlatish:** `gen_refs.py <ref.wav|none[,...]> lines.json outdir` (UAzimov adapteri `uz_uaz/`, `PeftModel.merge_and_unload`). Matnda ASCII apostrof (`'`), raqamlarni so'z bilan. Bir vaqtda ikkita generatsiya jarayonini ishga tushirmang (xotira 15 GB, to'xtab qoladi: 3 s/token). Bir gap ~5–10 s CPU'da. `VAD` yuklash xatosi (silero torch.hub, github) zararsiz.

### Talaffuz tuzatishlari
(hozircha bo'sh; foydalanuvchi talaffuz xatolarini aytgach to'ldiriladi)

## Texnik eslatmalar

- Klip manbai: Pixabay Videos API. Kalit `PIXABAY_API_KEY` muhit o'zgaruvchisida (hech qachon commit qilmang).
- Python `urllib` Pixabay'da 403 beradi; `curl` ishlaydi.
- Yig'ish: `ffmpeg` (drawtext, DejaVu Sans Bold — `'` va `–` belgilari to'g'ri chiqadi) + Pillow (CTA animatsiyasi). Skriptlar: `reels/fetch_clips.py` (nomzod klip qidirish va ko'rinishlar to'ri; `Q` lug'atidagi qidiruv so'zlarini mavzuga qarab o'zgartiring), `reels/build_reel.py` (umumiy yig'uvchi, matnli sahnalar + animatsiyali CTA + Instagram belgisi). Yangi video uchun `reels/specs/` ga JSON spetsifikatsiya yozing (`video2_diqqat.json` namunasi), klipni to'liq HD sifatda `clips/<nom>.mp4` ga yuklang, so'ng `python3 -I reels/build_reel.py reels/specs/<fayl>.json`. Oxirgi kadr fon klipi `clips/cta_bg.mp4` (quyosh chiqishi, Pixabay 153821).
- Gorizontal klipni 9:16 ga kesishda `crop x` ulushini klipga qarab sozlang (markaz ko'pincha kerakli obyektni kesib tashlaydi). Tayyor kadrni ko'rib tekshiring.
- Proksi CA: `/root/.ccr/ca-bundle.crt`. TLS tekshiruvini o'chirmang.
- Tayyor videoni yuborishdan oldin kamida bir nechta kadrni ko'zdan kechiring; faylni `SendUserFile` bilan yuboring va branchga commit/push qiling.
