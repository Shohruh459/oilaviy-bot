#!/usr/bin/env python3
"""Yakuniy sifat tekshiruvi. Ishlatish: qc.py <video.mp4> [--silent]. Xato bo'lsa exit 1."""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
V = sys.argv[1]; silent = '--silent' in sys.argv
tl = json.load(open(f'{R}/build/timeline.json')); T = tl['total']
res = []
def chk(name, ok, info=''): res.append(ok); print(f"[{'OK ' if ok else 'XATO'}] {name} {info}")
pr = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',V]))
v = next(s for s in pr['streams'] if s['codec_type']=='video'); a = [s for s in pr['streams'] if s['codec_type']=='audio']
chk('video ochiladi', True)
chk('o\'lcham 1080x1920', (v['width'], v['height']) == (1080, 1920), f"{v['width']}x{v['height']}")
chk('aspect 9:16', v['width']*16 == v['height']*9)
n, d = map(int, v['r_frame_rate'].split('/')); chk('FPS = 30', n/d == 30, f'{n/d}')
chk('video kodek H.264', v['codec_name'] == 'h264' and v.get('pix_fmt') == 'yuv420p', f"{v['codec_name']} {v.get('pix_fmt')}")
dur = float(pr['format']['duration']); chk('davomiylik 35–50 s', 35 <= dur <= 50, f'{dur:.2f}s')
chk('davomiylik rejaga mos', abs(dur - T) < 0.15, f'reja {T:.2f}s')
if not silent:
    chk('audio mavjud', bool(a)); 
    if a:
        chk('audio kodek AAC', a[0]['codec_name'] == 'aac', f"{a[0]['codec_name']} {a[0]['sample_rate']}Hz {a[0]['channels']}ch")
        ad = float(a[0].get('duration', dur)); chk('audio/video uzunligi mos', abs(ad - dur) < 0.15, f'{ad:.2f}s')
        r = subprocess.run(['ffmpeg','-v','info','-i',V,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json,astats=measure_perchannel=none','-f','null','-'],capture_output=True,text=True).stderr
        m = json.loads(r[r.index('{'):r.index('}')+1]); I, TP = float(m['input_i']), float(m['input_tp'])
        chk('loudness ≈ -16 LUFS (±1.5)', abs(I + 16) <= 1.5, f'{I:.1f} LUFS')
        chk('true peak ≤ -1.5 dB', TP <= -1.5, f'{TP:.2f} dBTP')
        pk = max(float(x) for x in re.findall(r'Peak level dB:\s*(-?[\d.]+)', r)); chk('clipping yo\'q (sample peak < -1 dBFS)', pk < -1.0, f'{pk:.2f} dBFS')
        nc = re.findall(r'Number of clipped samples:\s*(\d+)', r); chk('clipped sample = 0', not nc or int(nc[-1]) == 0)
else: chk('(preview) audio yo\'q — kutilgan', not a)
# kadrlar
def frame(t):
    p = f'{R}/build/qc_{t:.2f}.png'; subprocess.run(['ffmpeg','-y','-v','error','-ss',f'{t:.3f}','-i',V,'-frames:v','1',p],check=True)
    im = np.asarray(Image.open(p).convert('RGB')).astype(int); os.remove(p); return im
# qora/bo'sh kadr: fade zonalaridan tashqarida
bl = subprocess.run(['ffmpeg','-v','info','-i',V,'-vf','blackdetect=d=0.1:pix_th=0.10','-an','-f','null','-'],capture_output=True,text=True).stderr
bad = [(float(a_), float(b_)) for a_, b_ in re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', bl) if float(b_) > 0.6 and float(a_) < T - 0.9]
chk('qora/bo\'sh kadr yo\'q (fade-dan tashqari)', not bad, str(bad) if bad else '')
for s in tl['scenes']:
    t = s['start'] + s['dur']/2; im = frame(t); chk(f"{s['id']} kadr bo'sh emas (std>12)", im.std() > 12, f'std={im.std():.1f}')
# subtitr mavjudligi va xavfsiz zona
ass = open(f'{R}/subtitles/subtitles.ass').read()
ev = [(float(re.sub(r'^(\d+):(\d+):([\d.]+)$', lambda m: str(int(m[1])*3600+int(m[2])*60+float(m[3])), m_[0])),
       float(re.sub(r'^(\d+):(\d+):([\d.]+)$', lambda m: str(int(m[1])*3600+int(m[2])*60+float(m[3])), m_[1])))
      for m_ in re.findall(r'Dialogue: 0,([\d:.]+),([\d:.]+)', ass)]
vis = off = 0
for a_, b_ in ev:
    im = frame((a_ + b_) / 2)
    band = im[1380:1700]; white = (band.min(axis=2) > 235)
    if white.sum() > 400: vis += 1
    ys, xs = np.where(white)
    if len(xs) and (xs.min() < 60 or xs.max() > 1020): off += 1
chk('subtitr ko\'rinadi', vis >= len(ev) * 0.9, f'{vis}/{len(ev)} qator')
chk('subtitr ekrandan chiqmagan (L/R 60 px)', off == 0, f'{off} muammo')
chk('subtitr xavfsiz zonada (pastki 220 px bo\'sh)', all((frame((a_+b_)/2)[1700:1920].min(axis=2) > 235).sum() < 50 for a_, b_ in ev[::3]))
# oxirgi kadr
last = frame(T - 0.12); mid = frame(T - 1.2)
chk('oxirgi kadr fade-to-black bilan tugaydi', last.mean() < 25, f'mean={last.mean():.1f}')
chk('yakuniy matn oxirgacha ko\'rinadi', mid.std() > 12, f'std={mid.std():.1f}')
if not all(res): print('\nTEKSHIRUV O\'TMADI'); sys.exit(1)
print('\nBARCHA TEKSHIRUVLAR O\'TDI')
