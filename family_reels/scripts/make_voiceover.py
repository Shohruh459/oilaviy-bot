#!/usr/bin/env python3
"""scenes.json 'vo' -> uz-UZ-MadinaNeural -> audio/vo_S*.wav (mono 48 kHz).
Jumlalar orasiga tabiiy pauza qo'shiladi. Yozuv: oʻ/gʻ (U+02BB), eʼ (U+02BC) — Madina shu shaklni to'g'ri o'qiydi."""
import json, os, re, subprocess, sys, tempfile
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VOICE = 'uz-UZ-MadinaNeural'; RATE = os.environ.get('TTS_RATE', '-4%')
def norm(t):
    t = re.sub(r"([oOgG])'", "\\1\u02bb", t); t = re.sub(r"([eE])'", "\\1\u02bc", t); return t
def parts(t):
    segs = re.split(r'(?<=[.?!:])\s+', t.strip()); return [(s, 0.35 if s.endswith(':') else 0.5) for s in segs if s]
only = sys.argv[1:]
cfg = json.load(open(f'{R}/scripts/scenes.json')); lines = []
for s in cfg['scenes']:
    if only and s['id'] not in only: continue
    tmp = tempfile.mkdtemp(); lst = []
    for i, (txt, gap) in enumerate(parts(s['vo'])):
        mp3 = f'{tmp}/p{i}.mp3'; wav = f'{tmp}/p{i}.wav'; txt = norm(txt)
        subprocess.run(['python3', f'{R}/scripts/tts_edge.py', VOICE, txt, mp3, RATE], check=True)
        subprocess.run(['ffmpeg','-y','-v','error','-i',mp3,'-ar','48000','-ac','1','-af','silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08,areverse',wav], check=True)
        lst.append(wav); lines.append(f"[{s['id']}] {txt}")
        sil = f'{tmp}/s{i}.wav'
        subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','anullsrc=r=48000:cl=mono','-t',str(gap),sil], check=True); lst.append(sil)
    lst = lst[:-1]  # oxirgi pauza kerak emas
    open(f'{tmp}/l.txt','w').write(''.join(f"file '{x}'\n" for x in lst))
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',f'{tmp}/l.txt','-c','copy',f"{R}/audio/vo_{s['id']}.wav"], check=True)
    print('tayyor', s['id'])
open(f'{R}/voiceover_tts.txt','a' if only else 'w').write('\n'.join(lines)+'\n')
