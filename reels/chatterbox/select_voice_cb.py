"""Chatterbox nomzodlaridan har gap uchun eng yaxshisini tanlaydi (ASR + ovoz sifati + ohang birligi).

Ishlatish (sistema Python, HF_HUB_DISABLE_XET=1):
    python3 select_voice_cb.py spec.json nomzodlar_papkasi chiqish_papkasi yangi_spec.json
- Ball = 10*CER + max(0, shimmer-10.5) + 0.3*|ohang - maqsad ohang| (kam bo'lsa yaxshi)
- Tanlangani 24 kHz da, statik kuchaytirish bilan namuna ovoz (ref_tavsiya.wav) balandligiga tenglanadi.
- yangi_spec.json: "voice" yo'llari chiqish papkasiga ko'rsatadi (build_reel.py uchun tayyor).
"""
import glob, json, os, re, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import hear, voice_match as vm

spec_path, cand_dir, out_dir, new_spec = sys.argv[1:5]
spec = json.load(open(spec_path))
os.makedirs(out_dir, exist_ok=True)
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice_ref', 'ref_tavsiya.wav')
ref_rms = vm.features(REF)['rms']
items = [(f's{i}', sc) for i, sc in enumerate(spec['scenes'])] + [('cta', spec['cta'])]

cands = {}
for name, it in items:
    if not it.get('say'): continue
    rows = []
    for p in sorted(glob.glob(f'{cand_dir}/{name}_s*.wav')):
        h, _, _ = hear.transcribe(p)
        cer = hear.cer(hear.norm(it['say']), hear.norm(h))
        f = vm.features(p)
        rows.append(dict(path=p, cer=cer, shimmer=f['shimmer'], f0=f['f0'], rms=f['rms'], dur=f['dur']))
    cands[name] = rows
target_f0 = float(np.median([r['f0'] for rows in cands.values() for r in rows]))
print(f'maqsad ohang: {target_f0:.1f} yarim ton')
chosen = {}
report_path = os.path.join(os.path.dirname(os.path.abspath(new_spec)), '_sel_report.json')
report = json.load(open(report_path)) if os.path.exists(report_path) else {}
for name, rows in cands.items():
    if not rows:
        continue
    for r in rows:
        r['score'] = 10 * r['cer'] + max(0, r['shimmer'] - 10.5) + 0.3 * abs(r['f0'] - target_f0)
    best = min(rows, key=lambda r: r['score'])
    chosen[name] = best
    report[name] = {'cer': best['cer'], 'file': os.path.basename(best['path'])}
    allc = ' '.join(f"{r['cer']*100:.0f}%" for r in rows)
    print(f"{name}: tanlandi {os.path.basename(best['path'])} CER {best['cer']*100:.0f}% shimmer {best['shimmer']:.1f} f0 {best['f0']:.1f} dur {best['dur']:.1f}s  (barcha CER: {allc})", flush=True)
    w, sr = sf.read(best['path'])
    w = w * (ref_rms / best['rms'])
    peak = float(np.abs(w).max())
    if peak > 0.97: w = w * (0.97 / peak)
    sf.write(f'{out_dir}/{name}.wav', w.astype(np.float32), sr)

for i, sc in enumerate(spec['scenes']):
    if sc.get('say'): sc['voice'] = f'{out_dir}/s{i}.wav'
spec['cta']['voice'] = f'{out_dir}/cta.wav'
json.dump(spec, open(new_spec, 'w'), ensure_ascii=False, indent=1)

json.dump(report, open(report_path, 'w'), ensure_ascii=False, indent=1)
paths = [f'{out_dir}/{n}.wav' for n in chosen]
M = hear.speaker_similarity(paths); iu = np.triu_indices(len(paths), 1)
print(f"ovoz o'xshashligi: o'rt {M[iu].mean():.2f} min {M[iu].min():.2f}")
print('SELECT_DONE', flush=True)
