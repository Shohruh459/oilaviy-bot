#!/usr/bin/env bash
# Ishlatish: ./render.sh            - hammasini renderlaydi
#            ./render.sh S4         - faqat S4 sahnani qayta renderlab, qayta yig'adi
set -euo pipefail
cd "$(dirname "$0")"
node scripts/render_cards.js            # 1) HTML/CSS -> PNG kartalar
python3 scripts/make_timeline.py        # 2) vaqt jadvali + SRT/ASS + voiceover.txt
python3 scripts/make_placeholders.py    # 3) rasm yo'q sahnalar uchun vaqtinchalik fon
python3 scripts/check_audio.py          # 3b) WAV tekshiruvi (audio bo'lsa)
python3 scripts/render_scenes.py "$@"   # 4) har sahna alohida
python3 scripts/assemble.py             # 5) birlashtirish (+audio, loudnorm, subtitr)
if ls audio/vo_S*.wav >/dev/null 2>&1; then
  python3 scripts/qc.py build/candidate.mp4 || { echo "QC o'tmadi — final yaratilmadi (build/candidate.mp4 ni ko'ring)"; exit 1; }
  mv build/candidate.mp4 final/family_happiness_reels.mp4     # 7) faqat QC o'tgach
  echo "FINAL tayyor: final/family_happiness_reels.mp4"
else
  python3 scripts/qc.py renders/preview_silent.mp4 --silent   # 6) preview QC
fi
