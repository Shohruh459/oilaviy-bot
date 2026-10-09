"""Bitta videoni Chatterbox ayol ovozi (FEM2) bilan boshidan oxirigacha yig'adi.

Ishlatish (sistema Python, repo ildizidan):
    CBWORK=/yo'l/cbwork python3 reels/chatterbox/make_video_cb.py reels/specs/videoN_nom.json ISH_PAPKA [--cta-from fayl.wav]

ISH_PAPKA ichida `clips/<nom>.mp4` (to'liq HD klip + `clips/cta_bg.mp4`) bo'lishi kerak.
Qadamlar: (1) har gap uchun 4 seed (butun gap bir o'tishda, venv'dagi Chatterbox), (2) ASR + shimmer + ohang bo'yicha tanlash,
(3) spetsifikatsiyani Chatterbox ovozi uchun yangilash (voice_cb/, voice_tail 0.6), (4) video yig'ish.
CTA gapi hamma videoda bir xil: `--cta-from` berilsa, qayta generatsiya qilinmaydi (tezroq va bir xil ovoz).

Qo'shimcha: `--improve 0.10` (CER > 10% bo'lgan gaplar uchun 8 ta yangi seed, qayta tanlash, qayta yig'ish; nomzodlar `ISH_PAPKA/cand` da saqlanadi),
`--lines s2,s3` (aniq gaplar uchun shuni majburlash).
Muhit: CBWORK = papka (src/, pretrained_models/, uz_uaz/, refs/ ), CBPY = venv python (standart $CBWORK/../cbenv/bin/python).
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REELS = os.path.dirname(HERE)
spec_path = os.path.abspath(sys.argv[1])
work = os.path.abspath(sys.argv[2])
cta_from = sys.argv[sys.argv.index('--cta-from') + 1] if '--cta-from' in sys.argv else None
improve = float(sys.argv[sys.argv.index('--improve') + 1]) if '--improve' in sys.argv else None
force_lines = sys.argv[sys.argv.index('--lines') + 1] if '--lines' in sys.argv else None
CBWORK = os.environ['CBWORK']
CBPY = os.environ.get('CBPY', os.path.join(CBWORK, '..', 'cbenv', 'bin', 'python'))
os.makedirs(work, exist_ok=True)
spec = json.load(open(spec_path))

# 1) namuna ovoz va generatsiya skripti CBWORK ichida
os.makedirs(os.path.join(CBWORK, 'refs'), exist_ok=True)
ref = os.path.join(CBWORK, 'refs', 'fem1.wav')
if not os.path.exists(ref):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(REELS, 'voice_ref', 'candidates', 'fleurs_female_2.wav'),
                    '-ar', '24000', '-ac', '1', ref], check=True)
shutil.copy(os.path.join(HERE, 'gen_voice_cb.py'), os.path.join(CBWORK, 'gen_voice_cb.py'))

# 2) vaqtinchalik spetsifikatsiya (CTA matnisiz, agar tayyor CTA berilgan bo'lsa)
tmp = json.loads(json.dumps(spec))
if cta_from:
    tmp['cta']['say'] = ''
tmp_path = os.path.join(work, '_gen_spec.json')
json.dump(tmp, open(tmp_path, 'w'), ensure_ascii=False)
cand = os.path.join(work, 'cand')
env = dict(os.environ, NOSPLIT='1', HF_HUB_DISABLE_XET='1', OMP_NUM_THREADS='4')
if improve is None and not force_lines:
    shutil.rmtree(cand, ignore_errors=True)
    subprocess.run([CBPY, 'gen_voice_cb.py', tmp_path, 'refs/fem1.wav', cand, '4'], cwd=CBWORK, env=env, check=True)
else:
    # zaif gaplar uchun qo'shimcha seed'lar (mavjud nomzodlar saqlanadi)
    rep_path = os.path.join(work, '_sel_report.json')
    weak = force_lines.split(',') if force_lines else [n for n, v in json.load(open(rep_path)).items() if v['cer'] > improve]
    print('zaif gaplar:', weak, flush=True)
    if weak:
        os.makedirs(cand, exist_ok=True)
        start = 1 + max([int(f.rsplit('_s', 1)[1].split('.')[0]) for f in os.listdir(cand) if f.startswith(weak[0] + '_s')] or [0])
        env.update(ONLY=','.join(weak), SEED_START=str(start))
        subprocess.run([CBPY, 'gen_voice_cb.py', tmp_path, 'refs/fem1.wav', cand, '8'], cwd=CBWORK, env=env, check=True)

# 3) tanlash
env2 = dict(os.environ, HF_HUB_DISABLE_XET='1', OMP_NUM_THREADS='4')
if improve is None and not force_lines:
    shutil.rmtree(os.path.join(work, 'voice_cb'), ignore_errors=True)
os.makedirs(os.path.join(work, 'voice_cb'), exist_ok=True)
subprocess.run([sys.executable, os.path.join(HERE, 'select_voice_cb.py'), tmp_path, cand, 'voice_cb',
                os.path.join(work, '_sel_spec.json')], cwd=work, env=env2, check=True)
if cta_from:
    shutil.copy(cta_from, os.path.join(work, 'voice_cb', 'cta.wav'))

# 4) yakuniy spetsifikatsiya (asl matnlar bilan) va yig'ish
for i, sc in enumerate(spec['scenes']):
    sc['voice'] = f'voice_cb/s{i}.wav'
    sc.pop('seed', None)
spec['cta']['voice'] = 'voice_cb/cta.wav'
spec['voice_tail'] = 0.6
for k in ('tts', 'speaking_rate'):
    spec.pop(k, None)
json.dump(spec, open(spec_path, 'w'), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, '-I', os.path.join(REELS, 'build_reel.py'), spec_path], cwd=work, env=env2, check=True)
print('VIDEO_DONE', spec['out'], flush=True)
