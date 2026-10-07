#!/usr/bin/env python3
"""Har sahnani alohida renderlaydi (renders/S*.mp4): fon (Ken Burns) + HTML kartalar (fade)."""
import json, os, subprocess, sys, glob
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
tl = json.load(open(f'{R}/build/timeline.json')); fps = tl['fps']
only = sys.argv[1:]  # masalan: render_scenes.py S4  (faqat bitta sahnani qayta render)
def bg_for(n):
    for e in ('jpg','jpeg','png'):
        p = f'{R}/assets/images/s{n}.{e}'
        if os.path.exists(p): return p, False
    return f'{R}/assets/images/placeholder_s{n}.jpg', True
for k, s in enumerate(tl['scenes'], 1):
    if only and s['id'] not in only: continue
    d = s['dur']; N = int(round(d * fps))
    bg, ph = bg_for(k)
    zp = {'in':   f"z='1.0+0.10*on/{N}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
          'out':  f"z='1.10-0.10*on/{N}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
          'left': f"z='1.08':x='(iw-iw/zoom)*(1-on/{N})':y='ih/2-(ih/zoom/2)'",
          'right':f"z='1.08':x='(iw-iw/zoom)*(on/{N})':y='ih/2-(ih/zoom/2)'"}[s['cam']]
    cmd = ['ffmpeg','-y','-v','error','-loop','1','-t',str(d),'-i',bg]
    cards = sorted(glob.glob(f"{R}/assets/cards/{s['id']}_*.png"))
    for c in cards: cmd += ['-loop','1','-t',str(d),'-i',c]
    f = (f"[0:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
         f"zoompan={zp}:d={N}:s=1080x1920:fps={fps},format=yuv420p[bg0];")
    last = 'bg0'
    for i, (c, cd) in enumerate(zip(cards, s['cards']), 1):
        a, b = cd['a'] * d, cd['b'] * d
        a += 0.25 if i == 1 else 0; b = min(b, d) - (0.0 if i == len(cards) else 0.0)
        f += (f"[{i}:v]format=rgba,fade=t=in:st={a:.2f}:d=0.4:alpha=1,"
              f"fade=t=out:st={max(a+0.5,b-0.35):.2f}:d=0.35:alpha=1[c{i}];"
              f"[{last}][c{i}]overlay=0:0:format=auto[v{i}];")
        last = f'v{i}'
    f = f.rstrip(';')
    cmd += ['-filter_complex', f, '-map', f'[{last}]', '-t', str(d), '-r', str(fps),
            '-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p', f"{R}/renders/{s['id']}.mp4"]
    print('render', s['id'], '(placeholder fon)' if ph else '', flush=True)
    subprocess.run(cmd, check=True)
