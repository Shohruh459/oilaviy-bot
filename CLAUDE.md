# CLAUDE.md

Repo ikki qismdan iborat:
- Telegram bot (`bot.py`, `database.py`, `questions.py`) — bu loyihaga tegmang, agar so‘ralmasa.
- `family_reels/` — 1-Reels (oilaviy baxt, Madina ovozi, tayyor). `children_reels/` — 2-Reels (farzand tarbiyasi, Sardor ovozi, final: `final/family_children_mercy_reels.mp4`). Ikkalasida bir xil pipeline; qoidalar ikkalasiga tegishli (yo‘llarni `family_reels/` o‘rniga mos papka bilan almashtiring).

## Loyiha
- Hammasi loyiha papkasi (`family_reels/` yoki `children_reels/`) ichida: `scripts/scenes.json` (yagona haqiqat manbai: matn, subtitr, kartalar, kamera), `render.sh` (to‘liq pipeline).
- Pipeline tartibi: `render_cards.js` → `make_timeline.py` → `make_placeholders.py` → `check_audio.py` → `render_scenes.py` → `assemble.py` → `qc.py`.
- Final fayl (`final/family_happiness_reels.mp4` yoki `final/family_children_mercy_reels.mp4`) ga FAQAT `qc.py` o‘tgach ko‘chiriladi (`build/candidate.mp4` orqali). QC'ni chetlab o‘tmang.
- Pipeline tuzilmasini o‘zgartirmang; kontentni `scenes.json` va `render_cards.js` orqali o‘zgartiring.
- `build/` gitignore'da (vaqtinchalik fayllar).
- Sahna foni: `assets/images/sN.jpg|png` (rasm, Ken Burns) YOKI `sN.mp4|mov|webm|m4v` (video, ustuvor; 9:16 ga cover-crop, qisqa bo‘lsa loop, ovozi ishlatilmaydi). `scenes.json` sahnasida ixtiyoriy: `vstart` (boshlanish soniyasi), `vfocus` (0..1, gorizontal crop markazi). Pixabay uchun: muhit tarmog‘iga `pixabay.com`, `cdn.pixabay.com` ruxsati va `PIXABAY_API_KEY` secret kerak; klip litsenziyasi/mosligini tekshiring, stock'da oila har kadrda boshqa bo‘ladi.

## Audio / TTS
- Ovoz: `uz-UZ-MadinaNeural` (Edge TTS), `python3 scripts/make_voiceover.py [S2 ...]` — bitta sahnani qayta yaratish mumkin.
- Yozuv: `oʻ`/`gʻ` (U+02BB), `eʼ` (U+02BC). Oddiy `'` va ayniqsa kirill ishlamaydi/yomon.
- Proksi: `edge-tts` uchun `scripts/tts_edge.py` ishlating (CA bundle `/root/.ccr/ca-bundle.crt`). TLS tekshiruvini hech qachon o‘chirmang.
- Ovozni men eshita olmayman — talaffuzni foydalanuvchi tekshiradi. Bu haqda ochiq ayting.

## Hadis qoidasi
- Hadisni o‘zingizdan to‘qimang. Hozirgi: Sahih Muslim 1469. Boshqa hadis kerak bo‘lsa, manbasini tekshirib (WebSearch) oling; ishonchingiz komil bo‘lmasa ishlatmang va foydalanuvchiga ayting.
- Hadisni "yagona sir" sifatida emas, Rasululloh ﷺ nasihati sifatida bering. O‘zbekcha qism — mazmuniy tarjima, so‘zma-so‘z deb ko‘rsatmang.

## Dizayn
- Karta matni yuzlar ustiga tushmasin: har sahna uchun `scenes.json` dagi `y` (karta tepa koordinatasi) rasmga qarab tanlanadi. Rasm almashsa, kadrni ko‘rib qayta tekshiring.
- Subtitr pastki xavfsiz zonada (ASS MarginV=340). Hadis kartasida ortiqcha animatsiya yo‘q.

## Limit/vaqtni tejash (MUHIM)
- `sleep` bilan kutmang (bloklanadi va behuda). Uzoq buyruqni `run_in_background: true` bilan ishga tushiring, tugashini xabar kelguncha kuting yoki bitta `until` sikli bilan Monitor/yagona buyruq ishlating. Polling qilmang.
- Bir xil narsani kutish uchun bir nechta monitor/fon vazifa ochmang; bittasi yetadi. Eski, keraksiz fon vazifalarni qayta kutmang.
- Bog‘liq amallarni bir vaqtda (parallel) chaqirmang: masalan fayl yaratish va uni yuborish bitta blokda bo‘lsa, fayl hali yo‘q bo‘lishi mumkin. Avval yarating va tekshiring, keyin yuboring.
- To‘liq renderni faqat zarur bo‘lganda ishga tushiring (≈3–4 min). Bitta sahna o‘zgarsa: `./render.sh S4`. Faqat matn/kartalar o‘zgarsa ham sahna renderi kerak; faqat subtitr/audio o‘zgarsa `assemble.py` yetarli.
- Avval kichik sinov (bitta sahna, bitta TTS jumla, bitta kadr), keyin to‘liq run. Sinovni `REELS_AUDIO` / `REELS_OUT` env bilan scratchpad'ga yo‘naltiring — `final/` ga tegmasin.
- Kadrlarni tekshirishda bitta contact sheet (bir nechta kadr bitta rasmda) yarating, har kadrni alohida o‘qimang.
- Foydalanuvchi hali qaror qilmagan narsani (ovoz tanlash, rasm almashtirish) oldindan qilib, keyin qaytadan renderlamang — avval so‘rang.
- Foydalanuvchi "hozircha final qilma" desa, `final/` ni yaratmang.

## Git
- Branch: `ccr-c3b95ce4-bxiz7a`. Commit + push (`git push -u origin <branch>`). PR faqat so‘ralsa.
- Commit xabarlari oxirida attribution qatorlari.
