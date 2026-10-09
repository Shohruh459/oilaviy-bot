"""Spetsifikatsiyadagi har bir gap (say) uchun Chatterbox (UAzimov LoRA) bilan bir necha seed variantini yaratadi.

Ishlatish (cbwork papkasida, venv ichida; ixtiyoriy muhit: NOSPLIT=1, ONLY=s2,s3, SEED_START=5):
    python gen_voice_cb.py spec.json namuna.wav chiqish_papkasi [seed_soni=4]
Chiqish: <papka>/<nom>_s<seed>.wav, nom = s0..s5, cta (24 kHz).
Matn `:.?!` bo'yicha bo'laklanadi, har bo'lak alohida o'qiladi, chetidagi jimlik kesiladi, orasiga aniq pauza qo'yiladi
(ordinal so'z "Birinchi" va keyingi gap bir so'zdek qo'shilib ketmasligi uchun).
Tanlash (ASR + ohang bo'yicha) `select_voice_cb.py` da.
"""
import json, os, random, re, sys
import numpy as np, soundfile as sf, torch

sys.path.insert(0, '.')
from src.chatterbox_.tts import ChatterboxTTS
from src.model import resize_and_load_t3_weights
from src.chatterbox_.models.t3.t3 import T3
from peft import PeftModel

spec = json.load(open(sys.argv[1]))
ref = None if sys.argv[2] == 'none' else sys.argv[2]
outdir = sys.argv[3]
nseeds = int(sys.argv[4]) if len(sys.argv) > 4 else 4
PAUSE = {',': 0.22, ':': 0.28, ';': 0.28, '.': 0.38, '?': 0.42, '!': 0.38}
os.makedirs(outdir, exist_ok=True)


def set_seed(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)


eng = ChatterboxTTS.from_local('pretrained_models', device='cpu')
hp = eng.t3.hp; hp.text_tokens_dict_size = 2454
if hasattr(hp, 'use_cache'): hp.use_cache = False
base = resize_and_load_t3_weights(T3(hp=hp), eng.t3.state_dict())
eng.t3 = PeftModel.from_pretrained(base, 'uz_uaz', is_trainable=False).merge_and_unload().eval()
eng.s3gen.eval(); eng.ve.eval()
sr = eng.sr


def norm(t):
    return re.sub("[ʻʼ‘’`]", "'", t)


def trim(w, thr=0.03, keep=0.04):
    a = np.abs(w); idx = np.where(a > thr * a.max())[0]
    if len(idx) == 0: return w
    k = int(keep * sr)
    return w[max(0, idx[0] - k): idx[-1] + k]


def synth_line(text, seed):
    parts = [norm(text)] if os.environ.get('NOSPLIT') else [p for p in re.split(r'([.:?!;]+)', norm(text)) if p.strip()]
    pieces = []; have = False
    for j, p in enumerate(parts):
        if re.fullmatch(r'[.:?!;]+', p.strip()):
            if have: pieces.append(np.zeros(int(sr * PAUSE.get(p.strip()[0], 0.3)), dtype=np.float32))
            continue
        set_seed(seed * 100 + j)
        with torch.no_grad():
            wav = eng.generate(text=p.strip(), audio_prompt_path=ref, exaggeration=0.5,
                               cfg_weight=0.5, repetition_penalty=2.0, temperature=0.8)
        if isinstance(wav, tuple): wav = wav[0]
        w = trim(wav.squeeze().cpu().numpy().astype(np.float32))
        w = w / max(1e-9, float(np.sqrt(np.mean(w ** 2)))) * 0.1
        pieces.append(w); have = True
    w = np.concatenate(pieces)
    return (w / max(1e-9, np.abs(w).max()) * 0.9).astype(np.float32)


items = [(f's{i}', sc) for i, sc in enumerate(spec['scenes'])] + [('cta', spec['cta'])]
only = set(os.environ['ONLY'].split(',')) if os.environ.get('ONLY') else None
seed_start = int(os.environ.get('SEED_START', '1'))
for name, it in items:
    if not it.get('say') or (only and name not in only): continue
    for sd in range(seed_start, seed_start + nseeds):
        w = synth_line(it['say'], sd)
        sf.write(f'{outdir}/{name}_s{sd}.wav', w, sr)
        print('SAVED', name, sd, round(len(w) / sr, 2), flush=True)
print('GEN_DONE', flush=True)
