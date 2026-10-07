#!/usr/bin/env bash
# Ishlatish: ./render.sh            - hammasini renderlaydi
#            ./render.sh S4         - faqat S4 sahnani qayta renderlab, qayta yig'adi
set -euo pipefail
cd "$(dirname "$0")"
node scripts/render_cards.js            # 1) HTML/CSS -> PNG kartalar
python3 scripts/make_timeline.py        # 2) vaqt jadvali + SRT/ASS + voiceover.txt
python3 scripts/make_placeholders.py    # 3) rasm yo'q sahnalar uchun vaqtinchalik fon
python3 scripts/render_scenes.py "$@"   # 4) har sahna alohida
python3 scripts/assemble.py             # 5) birlashtirish (+audio, loudnorm, subtitr)
