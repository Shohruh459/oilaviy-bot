#!/usr/bin/env python3
"""Har sahnani alohida renderlaydi (renders/S*.mp4): fon + HTML kartalar (fade).
Fon: assets/images/sN.{mp4,mov,webm,m4v} (video, ustuvor) yoki sN.{jpg,jpeg,png} (rasm, Ken Burns).
Video: 9:16 ga markazdan "cover" crop; qisqa bo'lsa loop; ovozi ishlatilmaydi. scenes.json'dagi ixtiyoriy kalitlar:
  "vstart": klip boshlanish soniyasi (default 0), "vfocus": gorizontal crop markazi 0..1 (default 0.5; 0=chap, 1=o'ng)."""
import json, os, subprocess, sys, glob
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
tl = json.load(open(f'{R}/build/timeline.json')); fps = tl['fps']
only = sys.argv[1:]  # masalan: render_scenes.py S4  (faqat bitta sahnani qayta render)
VIDEO_EXT = ('mp4','mov','webm','m4v')
def bg_for(n):
    for e in VIDEO_EXT + ('jpg','jpeg','png'):
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
    is_video = bg.rsplit('.', 1)[-1].lower() in VIDEO_EXT
    if is_video:
        cmd = ['ffmpeg','-y','-v','error','-ss',str(s.get('vstart', 0)),'-stream_loop','-1','-t',str(d),'-i',bg]
    else:
        cmd = ['ffmpeg','-y','-v','error','-loop','1','-t',str(d),'-i',bg]
    cards = sorted(glob.glob(f"{R}/assets/cards/{s['id']}_*.png"))
    for c in cards: cmd += ['-loop','1','-t',str(d),'-i',c]
    if is_video:
        fx = min(max(float(s.get('vfocus', 0.5)), 0), 1)
        f = (f"[0:v]fps={fps},scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
             f"crop=1080:1920:x='(iw-1080)*{fx}':y='(ih-1920)/2',setsar=1,format=yuv420p[bg0];")
    else:
        f = (f"[0:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
             f"zoompan={zp}:d={N}:s=1080x1920:fps={fps},format=yuv420p[bg0];")
    last = 'bg0'
    for i, (c, cd) in enumerate(zip(cards, s['cards']), 1):
        a, b = cd['a'] * d, cd['b'] * d
        a += 0.25 if i == 1 else 0; b = min(b, d) - (0.0 if i == len(cards) else 0.0)
        # yengil "settle" scale (1.04 -> 1.0, 0.6 s); hadis kartasida ortiqcha animatsiya yo'q
        sc = (f"scale=w='trunc(1080*(1.04-0.04*min(max(t-{a:.2f},0)/0.6,1))/2)*2':h=-2:eval=frame,"
              if cd.get('scale', True) else '')
        f += (f"[{i}:v]format=rgba,{sc}fade=t=in:st={a:.2f}:d=0.4:alpha=1,"
              f"fade=t=out:st={max(a+0.5,b-0.35):.2f}:d=0.35:alpha=1[c{i}];"
              f"[{last}][c{i}]overlay=x=(W-w)/2:y=(H-h)/2:format=auto[v{i}];")
        last = f'v{i}'
    f = f.rstrip(';')
    cmd += ['-filter_complex', f, '-map', f'[{last}]', '-t', str(d), '-r', str(fps),
            '-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p', f"{R}/renders/{s['id']}.mp4"]
    print('render', s['id'], '(placeholder fon)' if ph else '(video)' if is_video else '', flush=True)
    subprocess.run(cmd, check=True)
