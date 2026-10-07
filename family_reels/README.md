# Oilaviy baxtli yashash siri — Instagram Reels (9:16, ≈41 s)

## HOLAT (muhim)
| Qism | Holat |
|---|---|
| Pipeline (HTML kartalar, sahna renderi, xfade, ASS subtitr, audio mix, loudnorm, H.264/AAC) | ✅ tayyor, sinalgan |
| `renders/preview_silent.mp4` | ✅ tovushsiz, **placeholder fon** bilan; to‘liq format/vaqt sinovi uchun |
| `final/family_happiness_reels.mp4` | ❌ **hali yaratilmagan** — 2 narsa yetishmaydi (pastda) |

### Nima yetishmaydi
1. **O‘zbekcha TTS / voiceover.** Muhitda espeak/piper/edge-tts yo‘q; Higgsfield TTS modellari o‘zbek tilini qo‘llamaydi va hisobda 0 kredit (free plan). Sifatsiz audio yaratilmadi.
   → `voiceover.txt` dagi har sahna matnini o‘zbekcha TTS (yoki diktor) bilan o‘qitib, `audio/vo_S1.wav … vo_S6.wav` deb saqlang (sahnaga bitta fayl, jumlalar orasida tabiiy pauza bilan).
2. **Oilaviy rasmlar.** Lokal material yo‘q. `assets/image_prompts.md` da 6 ta 9:16 AI-prompt bor → `assets/images/s1.jpg … s6.jpg`.

Keyin: `./render.sh` — sahna davomiyligi audio uzunligidan avtomatik olinadi, subtitr qayta hisoblanadi, final fayl `final/family_happiness_reels.mp4` ga chiqadi (-16 LUFS, TP -1.5 dB).
Bitta sahnani almashtirish: `./render.sh S4`.

## Hadis (o‘zingizcha to‘qilmagan, tekshirilgan)
- Arabcha: «لا يفرك مؤمن مؤمنة، إن كره منها خلقًا رضي منها آخر»
- Mazmuni: Mo‘min erkak mo‘mina ayolni yomon ko‘rmasin. Agar uning bir xulqini yoqtirmasa, boshqasidan rozi bo‘ladi.
- Manba: **Sahih Muslim, 1469** (Abu Hurayra r.a.). Hadis raqami va "sahih" hukmi dorar.net / hadeethenc.com orqali tekshirildi.
- Videoda hadis "yagona sir" sifatida emas, Rasululloh ﷺ nasihati sifatida beriladi (karta sarlavhasi: "Rasululloh ﷺ nasihati"). S4 foni AI'siz, lokal HTML/SVG (`assets/images/s4.png`, avtomatik yaratiladi) — s4.jpg QO‘YMANG. O‘zbekcha — so‘zma-so‘z emas, mazmuniy tarjima. Nashrdan oldin bilimdor shaxsga ko‘rsatish tavsiya etiladi.

## Papkalar
`assets/` (images, cards) · `audio/` · `subtitles/` (SRT+ASS) · `scenes/shotlist.md` · `renders/` (sahnalar) · `final/` · `scripts/` · `build/` (vaqt jadvali, gitignore)

## Subtitr sinxroni
Hozir vaqtlar jumla uzunligiga proporsional (taxminiy). Haqiqiy audio kelgach, aniq sinxron uchun forced alignment (masalan Whisper) bilan `subtitles.ass` ni tuzatish tavsiya etiladi; hech bo‘lmasa final'ni ko‘rib, `scripts/scenes.json` dagi `subs` bo‘linishini moslang.

## Texnologiyalar
FFmpeg 6.1 (zoompan, xfade, libass, loudnorm, libx264, aac) · Chromium/Playwright (HTML/CSS → PNG kartalar) · Python (Pillow, numpy) · Inter shrifti.

## Audio/rasmlarni qayerga qo‘yish
- `audio/vo_S1.wav … vo_S6.wav` (har sahnaga bitta fayl; matn: `voiceover.txt`)
- `assets/images/s1.jpg, s2.jpg, s3.jpg, s5.jpg, s6.jpg` (S4 uchun rasm kerak emas)

## Tekshiruvlar (render.sh ichida avtomatik)
- `scripts/check_audio.py` — kanal, sample rate, davomiylik, clipping, jimlik.
- Audio: 2 o‘tishli loudnorm (-16 LUFS, TP ≤ -1.5 dB) + limiter.
- `scripts/qc.py` — 1080x1920, 9:16, 30 FPS, H.264/AAC, 35–50 s, qora kadr, subtitr ko‘rinishi/xavfsiz zona, loudness, clipping, oxirgi kadr. Audio bo‘lsa natija `build/candidate.mp4` ga yoziladi va faqat QC o‘tgach `final/family_happiness_reels.mp4` ga ko‘chiriladi.
- Arabcha shrift: tizimda faqat FreeSerif/DejaVu bor (ishlatilgan: FreeSerif). Yaxshiroq: Amiri yoki Noto Naskh Arabic.
- Whisper/faster-whisper o‘rnatilmagan; boshqa STT vositasi ham yo‘q. Audio kelgach o‘rnatish ko‘riladi; aks holda subtitr jumla uzunligiga proporsional.
