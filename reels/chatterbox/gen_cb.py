"""Chatterbox o'zbek modellari bilan gaplarni yaratish. Ishlatish: python gen_cb.py abd|uaz lines.json outdir [seed]"""
import sys, os, json, re, random, numpy as np, torch, soundfile as sf
sys.path.insert(0, '.')
from safetensors.torch import load_file
from src.chatterbox_.tts import ChatterboxTTS
from src.chatterbox_.models.t3.t3 import T3
kind, lines_path, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 42
REF = os.environ.get('REF', 'uz_abd/reference_voice.wav')
os.makedirs(outdir, exist_ok=True)
def set_seed(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)
NEW_VOCAB = 2454
eng = ChatterboxTTS.from_local('pretrained_models', device='cpu')
hp = eng.t3.hp; hp.text_tokens_dict_size = NEW_VOCAB
if kind == 'abd':
    t3 = T3(hp=hp); t3.load_state_dict(load_file('uz_abd/t3_finetuned_merged.safetensors'), strict=False)
else:
    from src.model import resize_and_load_t3_weights
    from peft import PeftModel
    if hasattr(hp, 'use_cache'): hp.use_cache = False
    base = resize_and_load_t3_weights(T3(hp=hp), eng.t3.state_dict())
    pm = PeftModel.from_pretrained(base, 'uz_uaz', is_trainable=False)
    t3 = pm.merge_and_unload()
eng.t3 = t3.eval(); eng.s3gen.eval(); eng.ve.eval()
def norm(t): return re.sub("[ʻʼ‘’`]", "'", t)
lines = json.load(open(lines_path))
for i, t in enumerate(lines):
    set_seed(seed + i)
    with torch.no_grad():
        wav = eng.generate(text=norm(t), audio_prompt_path=REF, exaggeration=0.5, cfg_weight=0.5, repetition_penalty=2.0, temperature=0.8)
    if isinstance(wav, tuple): wav = wav[0]
    w = wav.squeeze().cpu().numpy().astype(np.float32)
    sf.write(f'{outdir}/{i}.wav', w, eng.sr); print('SAVED', i, round(len(w)/eng.sr, 2), 's', flush=True)
print('GEN_DONE', flush=True)
