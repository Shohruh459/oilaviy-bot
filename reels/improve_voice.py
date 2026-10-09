"""Ovozli gaplarni yaxshilash: ASR bo'yicha eng yomon (CER yuqori) gaplarni ASR-yordamli tanlash bilan qayta yaratadi.

Ishlatish:  python3 -I improve_voice.py spec.json [chegara=0.40] [--only cta|scene3,...] [--skip cta,...]
Faqat yangisi aniqroq (CER kamida 0.04 kam) bo'lsa fayl almashtiriladi. Qat'iy "seed" li gaplar tegilmaydi.
Keyin build_reel.py ni qayta ishga tushiring. HF_HUB_DISABLE_XET=1 kerak.
"""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hear, voice_match

spec = json.load(open(sys.argv[1]))
thr = float(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 0.40
only = None
if '--only' in sys.argv:
    only = set(sys.argv[sys.argv.index('--only') + 1].split(','))
skip = set(sys.argv[sys.argv.index('--skip') + 1].split(',')) if '--skip' in sys.argv else set()
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voice_ref', 'ref_tavsiya.wav')
rate = spec.get('speaking_rate', 1.1)
kw = spec.get('tts', {})
items = [(f'scene{i}', sc) for i, sc in enumerate(spec['scenes'])] + [('cta', spec['cta'])]
for name, it in items:
    if not (it.get('say') and it.get('voice') and os.path.exists(it['voice'])):
        continue
    if 'seed' in it or name in skip or (only and name not in only):
        continue
    t, _, _ = hear.transcribe(it['voice'])
    base = hear.cer(hear.norm(it['say']), hear.norm(t))
    if base < thr and not only:
        print(f'{name}: CER {base*100:.0f}% (yaxshi, o`zgarmadi)', flush=True)
        continue
    tmp = it['voice'] + '.try.wav'
    sd, score, fin = voice_match.synth_matched(it['say'], tmp, REF, speaking_rate=rate, verbose=False, use_asr=True,
                                               seeds=range(1, 25), **kw)
    if fin['cer'] is not None and fin['cer'] < base - 0.04:
        shutil.move(tmp, it['voice'])
        print(f"{name}: CER {base*100:.0f}% -> {fin['cer']*100:.0f}% (seed {sd}, shimmer {fin['shimmer']:.1f})", flush=True)
    else:
        os.remove(tmp)
        print(f"{name}: CER {base*100:.0f}% yaxshilanmadi (eng yaxshi nomzod {fin['cer']*100:.0f}%), o`zgarmadi", flush=True)
print('IMPROVE_DONE', flush=True)
