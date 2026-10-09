import sys, os, json, re, random, numpy as np, torch, soundfile as sf
sys.path.insert(0, '.')
from src.chatterbox_.tts import ChatterboxTTS
from src.chatterbox_.models.t3.t3 import T3
from src.model import resize_and_load_t3_weights
from peft import PeftModel
refs=sys.argv[1].split(','); lines=json.load(open(sys.argv[2])); outroot=sys.argv[3]; seed=42
def set_seed(s): random.seed(s); np.random.seed(s); torch.manual_seed(s)
eng = ChatterboxTTS.from_local('pretrained_models', device='cpu')
hp = eng.t3.hp; hp.text_tokens_dict_size = 2454
if hasattr(hp,'use_cache'): hp.use_cache=False
base = resize_and_load_t3_weights(T3(hp=hp), eng.t3.state_dict())
t3 = PeftModel.from_pretrained(base,'uz_uaz',is_trainable=False).merge_and_unload()
eng.t3=t3.eval(); eng.s3gen.eval(); eng.ve.eval()
norm=lambda t: re.sub("[ʻʼ‘’`]","'",t)
for r in refs:
    name=('default' if r=='none' else os.path.splitext(os.path.basename(r))[0]); os.makedirs(f'{outroot}/{name}',exist_ok=True)
    for i,t in enumerate(lines):
        set_seed(seed+i)
        with torch.no_grad():
            wav=eng.generate(text=norm(t),audio_prompt_path=(None if r=='none' else r),exaggeration=0.5,cfg_weight=0.5,repetition_penalty=2.0,temperature=0.8)
        if isinstance(wav,tuple): wav=wav[0]
        w=wav.squeeze().cpu().numpy().astype(np.float32); sf.write(f'{outroot}/{name}/{i}.wav',w,eng.sr)
        print('SAVED',name,i,round(len(w)/eng.sr,2),flush=True)
print('GEN_DONE',flush=True)
