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
REF_WAV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voice_ref', 'ref_tavsiya.wav')
REF_TXT = open(os.path.join(os.path.dirname(REF_WAV), 'ref_tavsiya.txt')).read()
rate = spec.get('speaking_rate', 1.1)
for name, it in items:
    if it.get('say') and it.get('voice'):
        os.makedirs(os.path.dirname(it['voice']) or '.', exist_ok=True)
        if 'seed' in it:  # qat'iy seed: moslashtirishsiz
            import voice_match
            raw = it['voice'] + '.raw.wav'
            cyr, dur = tts_uz.synth(it['say'], raw, speaking_rate=rate, seed=it['seed'])
            voice_match._postprocess(raw, it['voice'], voice_match.features(REF_WAV)['rms'])  # faqat ovoz balandligini tenglash
            os.remove(raw)
            print(f"{name}: seed {it['seed']} (qat'iy) {dur:.1f}s | {cyr}")
        else:  # namuna ovozga eng yaqin variantni tanlash
            import voice_match
            sd, d, fin = voice_match.synth_matched(it['say'], it['voice'], REF_WAV, speaking_rate=rate, verbose=False)
            print(f"{name}: seed {sd} (masofa {d:.2f}), shimmer {fin['shimmer']:.1f}, f0 {fin['f0']:.1f} | {tts_uz.lat2cyr(it['say'])}")
