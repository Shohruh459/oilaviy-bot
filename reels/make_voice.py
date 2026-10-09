"""Spetsifikatsiyadagi "say" matnlaridan ovoz fayllarini yaratadi (reels/tts_uz.py orqali).

Ishlatish:  python3 -I make_voice.py spec.json
Har sahna uchun  scenes[i]["say"] -> scenes[i]["voice"] (wav), CTA uchun cta["say"] -> cta["voice"].
Natija: har fayl uchun kirill matn va davomiylik chop etiladi (talaffuzni tekshirish uchun).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_uz

spec = json.load(open(sys.argv[1]))
items = [(f"scene {i}", sc) for i, sc in enumerate(spec['scenes'])] + [("cta", spec['cta'])]
for name, it in items:
    if it.get('say') and it.get('voice'):
        os.makedirs(os.path.dirname(it['voice']) or '.', exist_ok=True)
        cyr, dur = tts_uz.synth(it['say'], it['voice'], speaking_rate=spec.get('speaking_rate', 1.0))
        print(f"{name}: {dur:.1f}s | {cyr}")
